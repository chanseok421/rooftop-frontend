from __future__ import annotations

import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from core.models import LocationResult


class VWorldGeocodingProvider:
    """VWorld geocoding (address -> point).

    - 배포 환경에서 domain 검증/프록시/WAF 이슈가 있을 수 있어
      include_domain=True/False로 A/B 재시도한다.
    - 5xx/비JSON 응답이 자주 발생할 수 있으므로 최소한의 진단 로그를 남긴다.
    """

    BASE_URL = "https://api.vworld.kr/req/address"

    def __init__(self, api_key: str, timeout_s: float = 8.0, domain: str | None = None):
        self.api_key = api_key
        self.timeout_s = timeout_s
        # VWorld는 발급키에 허용 도메인이 묶여 있을 수 있으므로 domain을 옵션으로 둔다.
        self.domain = domain or os.getenv("VWORLD_DOMAIN")

        self.base_headers: dict[str, str] = {
            "User-Agent": "RooftopGreening/1.0",
            "Accept": "application/json",
        }

        # Session 설정 (Retry)
        self.session = requests.Session()

        retries = Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=0.8,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=frozenset(["GET"]),
            raise_on_status=False,
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

        # 공통 Header 설정
        self.session.headers.update(self.base_headers)

    def _build_params(self, address: str, include_domain: bool) -> dict[str, str]:
        # ✅ 대소문자 이슈 방지를 위해 예제 형태(소문자)로 통일
        params: dict[str, str] = {
            "service": "address",
            "request": "getcoord",   # ✅ 안전: getcoord
            "format": "json",
            "crs": "epsg:4326",      # ✅ 소문자
            "type": "road",          # ✅ 소문자
            "address": address,
            "key": self.api_key,
        }
        # domain 파라미터는 환경에 따라 필요/불필요가 갈려서 옵션화
        if include_domain and self.domain:
            params["domain"] = self.domain
        return params

    def _build_headers(self, include_domain: bool) -> dict[str, str]:
        headers = dict(self.base_headers)
        # Referer는 domain 검증이 필요한 환경에서만 의미가 있을 수 있어 옵션화
        if include_domain and self.domain:
            d = self.domain.replace("https://", "").replace("http://", "").rstrip("/")
            headers["Referer"] = f"https://{d}/"
        return headers

    def _request(self, address: str, include_domain: bool) -> requests.Response:
        params = self._build_params(address, include_domain)
        headers = self._build_headers(include_domain)
        return self.session.get(self.BASE_URL, params=params, headers=headers, timeout=self.timeout_s)

    @staticmethod
    def _debug_response(prefix: str, resp: requests.Response) -> None:
        # Streamlit Cloud에서 가장 확실하게 보이는 건 print
        # (너무 길게 찍지 않도록 일부만)
        try:
            body_preview = (resp.text or "")[:300]
        except Exception:
            body_preview = "<unreadable>"
        print(f"{prefix} HTTP={resp.status_code}")
        print(f"{prefix} URL={resp.url}")
        print(f"{prefix} CT={resp.headers.get('Content-Type')}")
        print(f"{prefix} BODY={body_preview}")

    def geocode(self, address: str) -> LocationResult | None:
        address = (address or "").strip()
        if not address:
            return None

        # domain이 있으면: (포함) -> (미포함) 순으로 시도
        # domain이 없으면: (미포함) 1회만
        attempts = [True, False] if self.domain else [False]
        last_error: Exception | None = None

        for include_domain in attempts:
            try:
                resp = self._request(address, include_domain)

                # 200이 아니면 JSON 파싱 전에 로그를 남기고 다음 시도 or 실패 처리
                if resp.status_code != 200:
                    self._debug_response(
                        prefix=f"[VWORLD][include_domain={include_domain}]",
                        resp=resp,
                    )
                    # domain 포함 시도에서 실패하면 domain 없이 한 번 더 시도
                    if include_domain and self.domain:
                        last_error = RuntimeError(f"VWorld geocoding HTTP {resp.status_code} (with domain).")
                        continue
                    raise RuntimeError(f"VWorld geocoding failed: HTTP {resp.status_code}")

                # JSON 파싱
                try:
                    data = resp.json()
                except ValueError as exc:
                    # 응답이 XML/HTML 등일 수 있음
                    self._debug_response(
                        prefix=f"[VWORLD][include_domain={include_domain}][non-json]",
                        resp=resp,
                    )
                    if include_domain and self.domain:
                        last_error = exc
                        continue
                    raise RuntimeError("VWorld geocoding response is not JSON.") from exc

            except requests.RequestException as exc:
                # 네트워크/타임아웃 등
                last_error = exc
                print(f"[VWORLD][include_domain={include_domain}] RequestException={repr(exc)}")
                if include_domain and self.domain:
                    continue
                raise RuntimeError("VWorld geocoding network error.") from exc

            # 방어적으로 파싱
            resp_obj = (data or {}).get("response") or {}
            if resp_obj.get("status") != "OK":
                # status: NOT_FOUND / ERROR 등
                last_error = RuntimeError(f"VWorld response status != OK: {resp_obj.get('status')}")
                print(f"[VWORLD][include_domain={include_domain}] status={resp_obj.get('status')}")
                if include_domain and self.domain:
                    continue
                return None

            point = ((resp_obj.get("result") or {}).get("point") or {})
            try:
                lon = float(point.get("x"))
                lat = float(point.get("y"))
            except (TypeError, ValueError) as exc:
                last_error = exc
                print(f"[VWORLD][include_domain={include_domain}] invalid point={point}")
                if include_domain and self.domain:
                    continue
                return None

            normalized = ((resp_obj.get("refined") or {}).get("text") or address)

            return LocationResult(
                input_address=address,
                normalized_address=normalized,
                point={"lat": lat, "lon": lon},
                provider="vworld",
                extra={"raw": data},
            )

        # 모든 시도 실패
        if last_error:
            raise RuntimeError("VWorld geocoding failed after retries (domain on/off).") from last_error
        return None
