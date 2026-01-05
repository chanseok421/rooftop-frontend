from __future__ import annotations

import math
import os
import time
from typing import Iterable, Optional

import requests

VWORLD_WFS_URL = "https://api.vworld.kr/req/wfs"


def _bbox_from_point(lat: float, lon: float, radius_m: float) -> tuple[float, float, float, float]:
    meters_per_deg_lat = 111320.0
    meters_per_deg_lon = 111320.0 * math.cos(math.radians(lat))
    dlat = radius_m / meters_per_deg_lat
    dlon = radius_m / meters_per_deg_lon if meters_per_deg_lon else radius_m / meters_per_deg_lat
    return (lon - dlon, lat - dlat, lon + dlon, lat + dlat)  # (minLon, minLat, maxLon, maxLat)


def _point_in_polygon(point: tuple[float, float], polygon: Iterable[tuple[float, float]]) -> bool:
    x, y = point
    inside = False
    pts = list(polygon)
    if len(pts) < 3:
        return False
    j = len(pts) - 1
    for i in range(len(pts)):
        xi, yi = pts[i]
        xj, yj = pts[j]
        intersects = ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi
        )
        if intersects:
            inside = not inside
        j = i
    return inside


def _extract_polygons(geometry: dict) -> list[list[tuple[float, float]]]:
    if not geometry:
        return []
    geom_type = geometry.get("type")
    coords = geometry.get("coordinates") or []
    polygons: list[list[tuple[float, float]]] = []
    if geom_type == "Polygon":
        if coords:
            polygons.append([(float(x), float(y)) for x, y in coords[0]])
    elif geom_type == "MultiPolygon":
        for poly in coords:
            if poly:
                polygons.append([(float(x), float(y)) for x, y in poly[0]])
    return polygons


def _fetch_polygon_once(
    *,
    lat: float,
    lon: float,
    api_key: str,
    radius_m: float,
    timeout_s: float,
    domain: Optional[str],
) -> Optional[list[tuple[float, float]]]:
    min_lon, min_lat, max_lon, max_lat = _bbox_from_point(lat, lon, radius_m)

    # EPSG:4326 bbox 순서: (ymin,xmin,ymax,xmax) = (minLat,minLon,maxLat,maxLon)
    bbox_str = f"{min_lat},{min_lon},{max_lat},{max_lon}"

    params = {
        "service": "WFS",
        "request": "GetFeature",
        "version": "1.1.0",
        "typename": "lt_c_bldginfo",
        "bbox": bbox_str,
        "srsname": "EPSG:4326",
        "output": "application/json",
        "key": api_key,
    }
    if domain:
        params["domain"] = domain

    resp = requests.get(VWORLD_WFS_URL, params=params, timeout=timeout_s)
    ctype = resp.headers.get("Content-Type", "")

    # HTTP 에러
    if resp.status_code != 200:
        # 필요하면 print 대신 logging으로 교체 추천
        print("[VWORLD WFS] HTTP", resp.status_code, "| URL:", resp.url)
        print("[VWORLD WFS] CT:", ctype)
        print("[VWORLD WFS] BODY:", resp.text[:500])
        return None

    # JSON이 아닌 경우(XML ServiceExceptionReport 등)
    if "json" not in ctype.lower():
        if "<ServiceException" in resp.text or "<ServiceExceptionReport" in resp.text:
            print("[VWORLD WFS] ServiceExceptionReport returned")
            print("[VWORLD WFS] URL:", resp.url)
            print("[VWORLD WFS] CT:", ctype)
            print("[VWORLD WFS] BODY:", resp.text[:500])
            return None
        print("[VWORLD WFS] Non-JSON response | URL:", resp.url)
        print("[VWORLD WFS] CT:", ctype)
        print("[VWORLD WFS] BODY:", resp.text[:500])
        return None

    data = resp.json()
    features = data.get("features") or []
    if not features:
        # 0건이면 그냥 None
        return None

    polygons: list[list[tuple[float, float]]] = []
    for f in features:
        polygons.extend(_extract_polygons(f.get("geometry") or {}))

    if not polygons:
        return None

    # 점 포함 폴리곤 우선
    point = (lon, lat)
    for poly in polygons:
        if _point_in_polygon(point, poly):
            return poly

    return polygons[0]


def get_building_polygon(
    coords: tuple[float, float],
    api_key: str,
    radius_m: float = 30.0,
    timeout_s: float = 10.0,
    domain: Optional[str] = None,
    *,
    max_attempts: int = 3,
) -> Optional[list[tuple[float, float]]]:
    """
    coords는 (lat, lon)로 들어온다고 가정.
    (lon, lat)가 들어오는 경우가 많아서 대한민국 범위 기준 자동 보정.
    또한 radius를 늘려가며 재시도해서 "가끔 안 잡히는" 케이스를 줄임.
    """
    lat, lon = coords

    # (lon,lat) 입력 자동 교정(대한민국 범위 기준)
    if not (33.0 <= lat <= 39.5 and 124.0 <= lon <= 132.5) and (33.0 <= lon <= 39.5 and 124.0 <= lat <= 132.5):
        lat, lon = lon, lat

    domain = domain or os.getenv("VWORLD_DOMAIN")

    # radius escalation: 30m -> 60m -> 120m (기본)
    radii = [radius_m, radius_m * 2, radius_m * 4]

    for attempt in range(max_attempts):
        r = radii[min(attempt, len(radii) - 1)]
        try:
            poly = _fetch_polygon_once(
                lat=lat,
                lon=lon,
                api_key=api_key,
                radius_m=r,
                timeout_s=timeout_s,
                domain=domain,
            )
            if poly:
                return poly
        except requests.RequestException as e:
            print("[VWORLD WFS] RequestException:", str(e))

        # backoff
        time.sleep(0.2 * (2**attempt))

    return None