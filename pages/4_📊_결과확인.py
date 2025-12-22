import streamlit as st

from core.services.analyze_service import AnalyzeService
from components.common.header import render_header
from core.state import get_state, set_state

st.set_page_config(page_title="결과확인 | 옥상이몽", page_icon="📊", layout="wide")
render_header(active="simulate")

st.header("📊 시뮬레이션 결과")
state = get_state()
if not state.get("scenario"):
    st.warning("먼저 '녹화계획' 페이지에서 계획을 저장하세요.")
    st.stop()

svc = AnalyzeService()
result = svc.compute()

set_state("result", result.model_dump())
st.success("계산 완료")

col1, col2, col3 = st.columns(3)
col1.metric("녹화 면적(㎡)", f"{result.green_area_m2:,.1f}")
col2.metric("연 CO₂ 흡수(kg)", f"{result.co2_absorption_kg_per_year:,.1f}")
col3.metric("온도 저감(℃)", f"{result.temp_reduction_c:,.2f}")

st.divider()
st.subheader("원본 결과(JSON)")
st.json(result.model_dump(), expanded=False)
