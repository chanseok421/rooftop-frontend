from __future__ import annotations

from core.models import RooftopAreaEstimate
from core.data_access.repositories import get_roof_area_from_candidate
from core.config import settings
from core.utils.geometry import polygon_area_m2
from api.vworld_wfs import get_building_polygon
from core.utils.availability import compute_availability_ratio


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _get_float_setting(possible_names: tuple[str, ...], default: float) -> float:
    """
    settings에 키가 프로젝트마다 다를 수 있어서,
    가능한 이름들을 순서대로 조회해서 float로 변환 가능한 값을 반환.
    """
    for name in possible_names:
        v = getattr(settings, name, None)
        if v is None:
            continue
        try:
            return float(v)
        except (TypeError, ValueError):
            continue
    return float(default)


def _get_alpha() -> float:
    """
    α: 물리 옥상면적/바닥면적 계수 (flat roof coefficient)
    - 평지붕 가정: 1.0
    - 경사지붕이면 0.6~0.8 등으로 settings에서 조정 가능
    """
    alpha = _get_float_setting(
        possible_names=(
            "roof_alpha",
            "rooftop_alpha",
            "flat_roof_coeff",
            "flat_roof_coefficient",
            "roof_area_alpha",
        ),
        default=1.0,
    )
    # 옥상계수는 보통 0~1 범위로 가정 (이상치 방지)
    return _clamp(alpha, 0.0, 1.0)


def _get_beta() -> float:
    """
    β: 옥상 녹화/활용 가능비율 (ARAR 성격의 제약 반영 비율)
    - 문헌 기반 예시값: 0.55
    """
    beta = _get_float_setting(
        possible_names=(
            "roof_beta",
            "rooftop_beta",
            "roof_greenable_ratio",
            "available_roof_area_ratio",
            "arar_beta",
        ),
        default=0.55,
    )
    return _clamp(beta, 0.0, 1.0)


def estimate_roof_area_m2_from_floor(floor_area_m2: float, *, alpha: float) -> float:
    """A_roof = α × A_floor"""
    return max(0.0, float(alpha) * float(floor_area_m2))


def estimate_greenable_roof_area_m2_from_roof(roof_area_m2: float, *, beta: float) -> float:
    """A_greenable = β × A_roof"""
    return max(0.0, float(beta) * float(roof_area_m2))


def estimate_greenable_roof_area_m2_from_floor(floor_area_m2: float, *, alpha: float, beta: float) -> float:
    """A_greenable = α × β × A_floor"""
    roof_area = estimate_roof_area_m2_from_floor(floor_area_m2, alpha=alpha)
    return estimate_greenable_roof_area_m2_from_roof(roof_area, beta=beta)


class RooftopService:
    def estimate_area(self, candidates, lat: float | None = None, lon: float | None = None) -> RooftopAreaEstimate:
        """
        옥상 녹화/활용 가능면적(Available/Greenable Roof Area) 추정.

        우선순위:
        1) candidates에서 roof_area_m2(물리 옥상면적)를 찾으면:
           A_greenable = β × A_roof
        2) 없으면 VWorld 폴리곤으로 바닥면적(A_floor) 추정 후:
           A_greenable = α × β × A_floor
        3) 둘 다 없으면 suggested=None (사용자 입력 유도)
        """
        alpha = _get_alpha()
        beta = _get_beta()

        # 내부적으로 물리 옥상면적(있으면)도 같이 들고 가지만, 모델에는 suggested만 반환
        roof_area_m2_raw: float | None = None

        suggested: float | None = None          # 최종 제안값: "녹화/활용 가능면적" (m²)
        floor_area_m2: float | None = None      # VWorld 폴리곤 기반 바닥면적(footprint) (m²)
        confidence = "low"
        note = "면적 데이터가 없으면 사용자가 직접 입력하도록 유도합니다."

        # 1) 후보 데이터(테이블) 기반: roof_area_m2를 '물리 옥상면적'으로 보고 β 적용
        for c in candidates or []:
            v = get_roof_area_from_candidate(c)
            if v and v > 0:
                roof_area_m2_raw = float(v)
                suggested = estimate_greenable_roof_area_m2_from_roof(roof_area_m2_raw, beta=beta)

                confidence = "medium"
                note = (
                    "데이터 테이블의 roof_area_m2(물리 옥상면적) 값을 기반으로 추정했습니다. "
                    f"녹화/활용 가능면적은 A_greenable=β×A_roof 로 변환 적용했습니다 (β={beta}). "
                    "정확도를 위해 확인이 필요합니다."
                )
                break

        # 2) VWorld WFS 폴리곤 기반 바닥면적 추정 (가능한 경우)
        polygon = None
        if lat is not None and lon is not None and settings.vworld_api_key:
            try:
                polygon = get_building_polygon((lat, lon), api_key=settings.vworld_api_key)
            except Exception:
                polygon = None

            if polygon:
                area = polygon_area_m2(polygon)
                if area and area > 0:
                    floor_area_m2 = float(area)

                    # candidates가 없어서 suggested가 비어있다면, α×β×A_floor 로 greenable 추정
                    if suggested is None:
                        suggested = estimate_greenable_roof_area_m2_from_floor(
                            floor_area_m2=floor_area_m2,
                            alpha=alpha,
                            beta=beta,
                        )
                        confidence = "low"
                        note = (
                            "VWorld 건물 폴리곤(WFS)으로 바닥면적(A_floor)을 추정했습니다. "
                            f"옥상 녹화/활용 가능면적은 A_greenable=α×β×A_floor 로 추정했습니다 (α={alpha}, β={beta}). "
                            "참고용으로 확인이 필요합니다."
                        )
                    else:
                        # candidates로 suggested를 이미 만들었지만, 바닥면적을 얻었으니 정보 보강
                        # (원하면 implied alpha 같은 것도 note에 추가 가능)
                        note = note + " 또한 VWorld 폴리곤(WFS)으로 바닥면적(A_floor)도 함께 추정했습니다."

        return RooftopAreaEstimate(
            roof_area_m2_suggested=suggested,
            floor_area_m2=floor_area_m2,
            availability_ratio=compute_availability_ratio(suggested, floor_area_m2),
            confidence=confidence,
            note=note,
            candidates=candidates or [],
        )
