import streamlit as st

from components.common.header import render_header
from components.common.footer import render_footer
from components.common.style import apply_common_styles
from ui.data_reference_ui import render_data_reference_ui

st.set_page_config(page_title="데이터 근거 | 옥상이몽", page_icon="📊", layout="wide")

apply_common_styles()

# Header (active_page="data")
render_header(active_page="data")

# Main UI
render_data_reference_ui()

# Footer
render_footer()
