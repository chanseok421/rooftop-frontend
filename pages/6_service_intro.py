import streamlit as st

from components.common.header import render_header
from components.common.footer import render_footer
from components.common.style import apply_common_styles
from ui.service_intro_ui import render_service_intro_ui

st.set_page_config(page_title="서비스 소개 | 옥상이몽", page_icon="🌿", layout="wide")

apply_common_styles()

# Header (intro actively selected)
render_header("intro")

# Main UI
render_service_intro_ui()

# Footer
render_footer()
