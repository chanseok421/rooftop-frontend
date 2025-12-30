from __future__ import annotations

import os

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from core.models import LocationResult

class VWorldGeocodingProvider:
    """VWorld geocoding (address -> point).

    VWorld API는 파라미터/응답 형식이 자주 바뀔 수 있으므로
    실제 적용 시 공식 문서/샘플에 맞춰 조정하세요.
    """

    BASE_URL = "https://api.vworld.kr/req/address"


    def __init__(self, api_key: str, timeout_s: float = 5.0, domain: str | None = None):
        self.api_key = api_key
        self.timeout_s = timeout_s
        # VWorld는 발급키에 허용 도메인이 묶여 있을 수 있으므로 domain을 함께 전송한다.
        self.domain = domain or os.getenv("VWORLD_DOMAIN")

        # Session 설정 (Retry, Header 등)
        self.session = requests.Session()
        
        # 1. Retry 설정
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            raise_on_status=False
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

        # 2. 공통 Header 설정 (User-Agent, Referer)
        self.session.headers.update({
            "User-Agent": "RooftopGreening/1.0",
        })
        # VWorld API 키 발급 시 등록한 도메인을 Referer로 보내야 할 수도 있음
        if self.domain:
            self.session.headers.update({"Referer": f"https://{self.domain}"})

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
        if self.domain:
            params["domain"] = self.domain

        # session.get 사용
        resp = self.session.get(self.BASE_URL, params=params, timeout=self.timeout_s)
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