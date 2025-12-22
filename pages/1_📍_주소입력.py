import streamlit as st

from core.services.analyze_service import AnalyzeService
from components.forms import address_input_form
from components.common.header import render_header
from core.state import get_state, set_state

st.set_page_config(page_title="주소입력 | 옥상이몽", page_icon="📍", layout="wide")

render_header(active="simulate")

st.header("📍 주소 입력")
st.write("주소를 입력하면 좌표/정규화 주소를 조회합니다. (외부 API가 없으면 더미 동작)")

address = address_input_form()

if address:
    svc = AnalyzeService()
    try:
        loc = svc.set_address(address)
        set_state("location", loc.model_dump())
        st.success("주소를 설정했습니다.")
        st.json(loc.model_dump(), expanded=False)
    except Exception as e:
        st.error(f"주소 처리 실패: {e}")

st.divider()
st.subheader("현재 세션 상태")
st.json(get_state(), expanded=False)
