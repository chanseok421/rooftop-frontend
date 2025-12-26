import streamlit as st

from components.common.header import render_header
from components.common.footer import render_footer
from components.common.style import apply_common_styles
from ui.contact_ui import render_contact_ui

st.set_page_config(page_title="문의하기 | 옥상이몽", page_icon="📮", layout="wide")

apply_common_styles()

# Header (active_page="contact")
render_header(active_page="contact")

# Main UI
render_contact_ui()

# Footer
render_footer()
