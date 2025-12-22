import streamlit as st

from core.services.analyze_service import AnalyzeService
from core.models import ScenarioInput
from components.common.header import render_header
from core.state import get_state, set_state

st.set_page_config(page_title="녹화계획 | 옥상이몽", page_icon="🌿", layout="wide")
render_header(active="simulate")

st.header("🌿 녹화 계획 설정")
state = get_state()
if not state.get("roof_area_m2_confirmed"):
    st.warning("먼저 '면적확인' 페이지에서 면적을 확정하세요.")
    st.stop()

roof_area = float(state["roof_area_m2_confirmed"])
st.metric("확정 옥상면적(㎡)", roof_area)

greening_type = st.selectbox("녹화 유형", options=["grass", "sedum", "shrub"], index=1)
coverage_ratio = st.slider("녹화 비율(%)", min_value=0, max_value=100, value=65, step=5) / 100.0

if st.button("계획 저장", type="primary"):
    scenario = ScenarioInput(greening_type=greening_type, coverage_ratio=coverage_ratio)
    svc = AnalyzeService()
    svc.set_scenario(scenario)
    set_state("scenario", scenario.model_dump())
    st.success("녹화 계획을 저장했습니다.")

st.divider()
st.subheader("현재 세션 상태")
st.json(get_state(), expanded=False)
