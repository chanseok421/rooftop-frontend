from __future__ import annotations

import math
from typing import Iterable, Tuple

# NOTE:
# - 공간데이터(폴리곤)가 들어오면 shapely/pyproj로 확장하세요.
# - MVP 1차는 단순 계산/placeholder로도 충분.

def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in meters."""
    R = 6371000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def _looks_like_korea_lonlat(points: list[Tuple[float, float]]) -> bool:
    if not points:
        return False
    valid = 0
    for lon, lat in points:
        if 33.0 <= lat <= 39.5 and 124.0 <= lon <= 132.5:
            valid += 1
    return valid / len(points) >= 0.6


def _looks_like_korea_latlon(points: list[Tuple[float, float]]) -> bool:
    if not points:
        return False
    valid = 0
    for lat, lon in points:
        if 33.0 <= lat <= 39.5 and 124.0 <= lon <= 132.5:
            valid += 1
    return valid / len(points) >= 0.6


def _normalize_polygon_lonlat(points: list[Tuple[float, float]]) -> list[Tuple[float, float]]:
    if _looks_like_korea_lonlat(points):
        return points
    if _looks_like_korea_latlon(points):
        return [(lon, lat) for lat, lon in points]
    return points

def polygon_area_m2(coords_lonlat: Iterable[Tuple[float, float]]) -> float:
    """Approximate polygon area in square meters from lon/lat coordinates.

    coords_lonlat: [(lon, lat), ...] closed or open polygon.
    NOTE: This uses a simple local projection; replace with shapely/pyproj for accuracy.
    """ 
    pts = list(coords_lonlat)
    if len(pts) < 3:
        return 0.0
    
    pts = _normalize_polygon_lonlat(pts)
    
    lat0 = sum(lat for _, lat in pts) / len(pts)
    meters_per_deg_lat = (
        111132.92 - 559.82 * math.cos(2 * math.radians(lat0)) + 1.175 * math.cos(4 * math.radians(lat0))
    )
    meters_per_deg_lon = 111412.84 * math.cos(math.radians(lat0)) - 93.5 * math.cos(3 * math.radians(lat0))

    projected = [(lon * meters_per_deg_lon, lat * meters_per_deg_lat) for lon, lat in pts]
    
    area = 0.0
    for i in range(len(projected)):
        x1, y1 = projected[i]
        x2, y2 = projected[(i + 1) % len(projected)]
        area += x1 * y2 - x2 * y1
        
    return abs(area) / 2.0
