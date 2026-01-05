from __future__ import annotations

import requests
from core.models import LocationResult

class VWorldGeocodingProvider:
    """VWorld geocoding (address -> point).

    VWorld API는 파라미터/응답 형식이 자주 바뀔 수 있으므로
    실제 적용 시 공식 문서/샘플에 맞춰 조정하세요.
    """

    BASE_URL = "https://api.vworld.kr/req/address"

    def __init__(self, api_key: str, timeout_s: float = 5.0):
        self.api_key = api_key
        self.timeout_s = timeout_s

    def geocode(self, address: str) -> LocationResult | None:
        address = (address or "").strip()
        if not address:
            return None

        params = {
            "service": "address",
            "request": "getcoord",
            "format": "json",
            "crs": "EPSG:4326",
            "type": "ROAD",
            "address": address,
            "key": self.api_key,
        }
        resp = requests.get(self.BASE_URL, params=params, timeout=self.timeout_s)
        resp.raise_for_status()
        data = resp.json()

        # 방어적으로 파싱
        resp_obj = (data or {}).get("response") or {}
        if resp_obj.get("status") != "OK":
            return None

        point = ((resp_obj.get("result") or {}).get("point") or {})
        lon = float(point.get("x"))
        lat = float(point.get("y"))

        normalized = ((resp_obj.get("refined") or {}).get("text") or address)

        return LocationResult(
            input_address=address,
            normalized_address=normalized,
            point={"lat": lat, "lon": lon},
            provider="vworld",
            extra={"raw": data},
        )