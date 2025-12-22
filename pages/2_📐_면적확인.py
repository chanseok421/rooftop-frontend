import streamlit as st

from core.services.analyze_service import AnalyzeService
from components.common.header import render_header
from core.state import get_state, set_state

st.set_page_config(page_title="면적확인 | 옥상이몽", page_icon="📐", layout="wide")
render_header(active="simulate")

st.header("📐 면적 확인")
st.write("좌표/건물 후보를 기반으로 옥상(또는 대상) 면적을 추정하고, 사용자가 확정합니다.")

state = get_state()
loc = state.get("location")
if not loc:
    st.warning("먼저 '주소입력' 페이지에서 주소를 입력하세요.")
    st.stop()

svc = AnalyzeService()
estimate = svc.estimate_rooftop_area(loc)

st.subheader("추천(추정) 면적")
st.metric("추정 옥상면적(㎡)", value=estimate.roof_area_m2_suggested or "N/A")
st.write(estimate.note or "")

st.subheader("확정 면적 입력")
default_area = float(estimate.roof_area_m2_suggested or 0.0)
confirmed = st.number_input("옥상 면적(㎡)", min_value=0.0, value=default_area, step=10.0)

if st.button("면적 확정", type="primary"):
    svc.confirm_area(confirmed)
    set_state("roof_area_m2_confirmed", confirmed)
    st.success("면적을 확정했습니다.")

st.divider()
st.subheader("현재 세션 상태")
st.json(get_state(), expanded=False)
