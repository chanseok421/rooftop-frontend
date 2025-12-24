import streamlit as st

from components.common.footer import render_footer
from components.common.header import render_header
from core.models import ScenarioInput
from core.services.analyze_service import AnalyzeService
from core.services.scenario_service import ScenarioService
from core.state import get_state, set_state
from ui.planning_ui import render_planning_ui

st.set_page_config(page_title="녹화계획 | 옥상이몽", page_icon="🌿", layout="wide")
render_header("simulate")

state = get_state()
if not state.get("roof_area_m2_confirmed"):
    st.warning("먼저 '면적확인' 페이지에서 면적을 확정하세요.")
    st.stop()

roof_area = float(state["roof_area_m2_confirmed"])
existing_scenario = state.get("scenario") or {}
default_type = existing_scenario.get("greening_type", "sedum")
default_ratio = float(existing_scenario.get("coverage_ratio", 0.65))

if "planning_selected_type" not in st.session_state:
    st.session_state["planning_selected_type"] = default_type

active_type = st.session_state.get("planning_selected_type", default_type)
slider_default = int(round(default_ratio * 100))
active_ratio = (st.session_state.get("planning_slider", slider_default) or 0) / 100

scenario_service = ScenarioService()
preview_scenario = ScenarioInput(greening_type=active_type, coverage_ratio=active_ratio)
preview_result = scenario_service.compute(roof_area_m2=roof_area, scenario=preview_scenario)

ui_state = render_planning_ui(
    roof_area=roof_area,
    selected_type=active_type,
    coverage_ratio=active_ratio,
    green_area_m2=preview_result.green_area_m2,
    co2_absorption_kg=preview_result.co2_absorption_kg_per_year,
    temp_reduction_c=preview_result.temp_reduction_c,
)

selected_type = ui_state["selected_type"]
coverage_ratio = ui_state["coverage_ratio"]

scenario = ScenarioInput(greening_type=selected_type, coverage_ratio=coverage_ratio)

svc = AnalyzeService()

if ui_state["save_clicked"]:
    svc.set_scenario(scenario)
    set_state("scenario", scenario.model_dump())
    st.success("녹화 계획을 저장했습니다.")


if ui_state["prev_clicked"]:
    st.switch_page("pages/2_📐_면적확인.py")

if ui_state["next_clicked"]:
    svc.set_scenario(scenario)
    set_state("scenario", scenario.model_dump())
    st.switch_page("pages/4_📊_결과확인.py")

render_footer()