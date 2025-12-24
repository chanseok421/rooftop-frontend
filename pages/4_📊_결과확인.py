import streamlit as st

from core.services.analyze_service import AnalyzeService
from components.common.footer import render_footer
from components.common.header import render_header
from core.constants import DEFAULT_PINE_FACTOR_KG_PER_YEAR, DEFAULT_BASELINE_SURFACE_TEMP_C, DEFAULT_GREENING_COEFFS
from core.models import ScenarioInput
from core.services.analyze_service import AnalyzeService
from core.state import get_state, set_state
from ui.result_ui import render_result_ui


st.set_page_config(page_title="결과확인 | 옥상이몽", page_icon="📊", layout="wide")

render_header("simulate")

state = get_state()
scenario_dict = state.get("scenario")
roof_area = state.get("roof_area_m2_confirmed")

if not scenario_dict or not roof_area:
    st.warning("먼저 '녹화계획' 페이지에서 계획을 저장하세요.")
    st.stop()
    
scenario = ScenarioInput(**scenario_dict)
svc = AnalyzeService()
result = svc.compute()

set_state("result", result.model_dump())
address_title = state.get("location", {}).get("input_address", "선택한 주소")
address_caption = state.get("location", {}).get("normalized_address", address_title)

ui_state = render_result_ui(
    address_title=address_title,
    address_caption=address_caption,
    greening_type_code=result.greening_type,
    coverage_ratio=result.coverage_ratio,
    roof_area_m2=result.roof_area_m2,
    green_area_m2=result.green_area_m2,
    co2_absorption_kg=result.co2_absorption_kg_per_year,
    temp_reduction_c=result.temp_reduction_c,
    baseline_surface_temp_c=result.baseline_surface_temp_c or DEFAULT_BASELINE_SURFACE_TEMP_C,
    after_surface_temp_c=result.after_surface_temp_c,
    tree_equivalent_count=result.tree_equivalent_count,
    co2_coefficient=DEFAULT_GREENING_COEFFS.get(result.greening_type, DEFAULT_GREENING_COEFFS.get("sedum")).co2_kg_m2_y,
    temp_coefficient=DEFAULT_GREENING_COEFFS.get(result.greening_type, DEFAULT_GREENING_COEFFS.get("sedum")).temp_reduction_c_at_100,
    pine_factor_kg_per_year=DEFAULT_PINE_FACTOR_KG_PER_YEAR,
)

if ui_state.get("prev_clicked"):
    st.switch_page("pages/3_🌿_녹화계획.py")

if ui_state.get("next_clicked"):
    st.switch_page("pages/5_📄_리포트.py")
    
render_footer()
