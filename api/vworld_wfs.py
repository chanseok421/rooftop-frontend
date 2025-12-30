from __future__ import annotations

import math
import os
from typing import Iterable, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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


def get_building_polygon(
    coords: tuple[float, float],
    api_key: str,
    radius_m: float = 30.0,
    timeout_s: float = 10.0,
    domain: Optional[str] = None,
):
    """
    coords는 (lat, lon)로 들어온다고 가정.
    (lon, lat)가 들어오는 경우가 많아서 한국 좌표 범위로 자동 보정도 넣음.
    """

    lat, lon = coords

    # ✅ 흔한 실수: (lon,lat)를 (lat,lon)으로 넣는 경우 자동 교정(대한민국 범위 기준)
    if not (33.0 <= lat <= 39.5 and 124.0 <= lon <= 132.5) and (33.0 <= lon <= 39.5 and 124.0 <= lat <= 132.5):
        lat, lon = lon, lat

    # bbox 계산
    min_lon, min_lat, max_lon, max_lat = _bbox_from_point(lat, lon, radius_m)

    # ✅ VWorld WFS: EPSG:4326이면 bbox 순서가 (ymin,xmin,ymax,xmax)
    bbox_str = f"{min_lat},{min_lon},{max_lat},{max_lon}"

    domain = domain or os.getenv("VWORLD_DOMAIN")  # 필요하면 환경변수로도 주입

    params = {
        "service": "WFS",
        "request": "GetFeature",
        "version": "1.1.0",
        "typename": "lt_c_bldginfo",      # ✅ VWorld 레이어명
        "bbox": bbox_str,
        "srsname": "EPSG:4326",
        "output": "application/json",     # ✅ VWorld WFS JSON
        "key": api_key,
    }
    if domain:
        params["domain"] = domain

    # Session w/ Retry
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        raise_on_status=False
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    
    # Headers
    session.headers.update({
        "User-Agent": "RooftopGreening/1.0",
    })
    if domain:
        session.headers.update({"Referer": f"https://{domain}"})

    resp = session.get(VWORLD_WFS_URL, params=params, timeout=timeout_s)

    # ✅ 여기부터 디버그 핵심: "왜 안 나오는지"를 터미널에서 바로 확인 가능
    ctype = resp.headers.get("Content-Type", "")
    if resp.status_code != 200:
        print("[VWORLD WFS] HTTP", resp.status_code)
        print("[VWORLD WFS] URL:", resp.url)
        print("[VWORLD WFS] CT:", ctype)
        print("[VWORLD WFS] BODY:", resp.text[:800])
        resp.raise_for_status()

    if "json" not in ctype.lower():
        # 인증키 오류(응답이 XML) 등은 조용히 무시하고 폴리곤 없이 진행
        if "<ServiceException" in resp.text:
            return None
        print("[VWORLD WFS] Non-JSON response")
        print("[VWORLD WFS] URL:", resp.url)
        print("[VWORLD WFS] CT:", ctype)
        print("[VWORLD WFS] BODY:", resp.text[:800])
        return None

    data = resp.json()
    features = data.get("features") or []

    if not features:
        print("[VWORLD WFS] 0 features returned")
        print("[VWORLD WFS] URL:", resp.url)
        print("[VWORLD WFS] coords(lat,lon):", (lat, lon))
        print("[VWORLD WFS] bbox:", bbox_str)
        # 서버가 에러를 JSON으로 주는 케이스도 있어서 일부 출력
        print("[VWORLD WFS] JSON keys:", list(data.keys())[:20])
        return None

    polygons: list[list[tuple[float, float]]] = []
    for f in features:
        polygons.extend(_extract_polygons(f.get("geometry") or {}))

    if not polygons:
        print("[VWORLD WFS] features exist but no polygons extracted")
        print("[VWORLD WFS] sample geometry:", (features[0].get("geometry") or {}))
        return None

    # 점 포함 폴리곤 우선
    point = (lon, lat)
    for poly in polygons:
        if _point_in_polygon(point, poly):
            return poly

    return polygons[0]
