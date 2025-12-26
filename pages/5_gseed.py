import streamlit as st
from ui.gseed_ui import render_gseed_page
from components.common.header import render_header
from components.common.style import apply_common_styles

# 페이지 설정
st.set_page_config(
    page_title="G-SEED란? | 옥상이몽",
    page_icon="🌱",
    layout="wide"
)

# 공통 스타일 적용
apply_common_styles()

# 1. 헤더 렌더링 (active_page="gseed")
render_header(active_page="gseed")

# 2. G-SEED 페이지 본문 렌더링
render_gseed_page()
