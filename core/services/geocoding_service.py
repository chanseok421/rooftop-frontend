from __future__ import annotations

from core.exceptions import AddressNotFoundError
from core.models import LocationResult
from api.adapters import GeocodingProvider
from api.kakao_api import KakaoGeocodingProvider
from api.vworld_api import VWorldGeocodingProvider
from core.config import settings

def default_provider() -> GeocodingProvider:
    # 우선순위: Kakao -> VWorld -> Dummy
    if settings.kakao_rest_api_key:
        return KakaoGeocodingProvider(api_key=settings.kakao_rest_api_key)
    if settings.vworld_api_key:
        return VWorldGeocodingProvider(
            api_key=settings.vworld_api_key,
            domain=settings.vworld_domain,
        )
    return _DummyGeocodingProvider()

class GeocodingService:
    def __init__(self, provider: GeocodingProvider | None = None):
        self.provider = provider or default_provider()

    def geocode(self, address: str) -> LocationResult:
        res = self.provider.geocode(address)
        if res is None:
            raise AddressNotFoundError(f"주소를 찾지 못했습니다: {address}")
        return res

class _DummyGeocodingProvider:
    """No external API. Returns a fixed point near Seoul City Hall."""

    def geocode(self, address: str) -> LocationResult | None:
        address = (address or "").strip()
        if not address:
            return None
        return LocationResult(
            input_address=address,
            normalized_address=address,
            point={"lat": 37.5665, "lon": 126.9780},
            provider="dummy",
            extra={"note": "외부 지오코딩 API 미설정: 더미 좌표 반환"},
        )
