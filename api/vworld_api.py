from __future__ import annotations

from urllib.parse import urlparse

import requests
from core.models import LocationResult

def _normalize_domain(domain: str | None) -> str | None:
    if not domain:
        return None
    parsed = urlparse(domain)
    if parsed.scheme:
        return parsed.netloc or None
    # 이미 순수 도메인 문자열인 경우 그대로 사용
    return domain

class VWorldGeocodingProvider:
    """VWorld geocoding (address -> point).

    VWorld API는 파라미터/응답 형식이 자주 바뀔 수 있으므로
    실제 적용 시 공식 문서/샘플에 맞춰 조정하세요.
    """

    BASE_URL = "https://api.vworld.kr/req/address"

    def __init__(self, api_key: str, *, domain: str | None = None, timeout_s: float = 5.0):
        self.api_key = api_key
        self.domain = _normalize_domain(domain)
        self.timeout_s = timeout_s

    def _build_params(self, address: str, *, include_domain: bool = True) -> dict:

        params = {
            "service": "address",
            "request": "getcoord",
            "format": "json",
            "crs": "EPSG:4326",
            "type": "ROAD",
            "address": address,
            "key": self.api_key,
        }
        if include_domain and self.domain:
            params["domain"] = self.domain
        return params

    def _request(self, params: dict) -> dict:
        resp = requests.get(self.BASE_URL, params=params, timeout=self.timeout_s)
        resp.raise_for_status()
        return resp.json()

    def _parse_response(self, data: dict, fallback_address: str) -> LocationResult | None:
        resp_obj = (data or {}).get("response") or {}
        if resp_obj.get("status") != "OK":
            return None

        point = ((resp_obj.get("result") or {}).get("point") or {})
        lon = float(point.get("x"))
        lat = float(point.get("y"))

        normalized = ((resp_obj.get("refined") or {}).get("text") or fallback_address)

        return LocationResult(
            input_address=fallback_address,
            normalized_address=normalized,
            point={"lat": lat, "lon": lon},
            provider="vworld",
            extra={"raw": data},
        )

    def geocode(self, address: str) -> LocationResult | None:
        address = (address or "").strip()
        if not address:
            return None
        # 1차: domain 포함 요청 / 2차: domain 제거 후 재시도 (502 등 대비)
        attempts = [self._build_params(address, include_domain=True)]
        if self.domain:
            attempts.append(self._build_params(address, include_domain=False))

        last_error: Exception | None = None
        for params in attempts:
            try:
                data = self._request(params)
            except requests.RequestException as exc:
                last_error = exc
                continue

            result = self._parse_response(data, address)
            if result:
                return result

        if last_error:
            raise last_error
            
        return None