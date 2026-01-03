from __future__ import annotations

import requests
from core.models import LocationResult


class VWorldGeocodingProvider:
    BASE_URL = "https://api.vworld.kr/req/address"

    def __init__(self, api_key: str, timeout_s: float = 5.0, domain: str | None = None):
        self.api_key = api_key
        self.timeout_s = timeout_s
        self.domain = domain

    def geocode(self, address: str) -> LocationResult | None:
        address = (address or "").strip()
        if not address:
            return None

        params = {
            "service": "address",
            "request": "getCoord",
            "version": "2.0",
            "format": "json",
            "crs": "EPSG:4326",
            "type": "ROAD",
            "address": address,
            "key": self.api_key,
        }
        if self.domain:
            params["domain"] = self.domain  # ✅ 중요

        resp = requests.get(self.BASE_URL, params=params, timeout=self.timeout_s)

        # ✅ 원인 확인용(배포에서 잠깐만)
        # print("[VWORLD GEOCODE] status:", resp.status_code)
        # print("[VWORLD GEOCODE] url:", resp.url)
        # print("[VWORLD GEOCODE] text:", resp.text[:300])

        resp.raise_for_status()
        data = resp.json()

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
