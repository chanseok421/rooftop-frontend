import streamlit as st

from components.common.footer import render_footer
from components.common.header import render_header
from core.models import SimulationResult
from core.services.analyze_service import AnalyzeService
from core.state import get_state
from ui.report_ui import render_report_ui

st.set_page_config(page_title="리포트 | 옥상이몽", page_icon="📄", layout="wide")

from components.common.style import apply_common_styles
apply_common_styles()

render_header("simulate")

state = get_state()
result_dict = state.get("result")

if not result_dict:
    st.warning("먼저 '결과확인' 페이지에서 결과를 계산하세요.")
    st.stop()

svc = AnalyzeService()

result = SimulationResult(**result_dict)
address_title = state.get("location", {}).get("input_address", "선택한 주소")
address_caption = state.get("location", {}).get("normalized_address", address_title)
pdf_bytes, pdf_filename = svc.export_pdf()
excel_bytes, excel_filename = svc.export_excel()

actions = render_report_ui(
    address_title=address_title,
    address_caption=address_caption,
    greening_type_code=result.greening_type,
    coverage_ratio=result.coverage_ratio,
    green_area_m2=result.green_area_m2,
    co2_absorption_kg=result.co2_absorption_kg_per_year,
    temp_reduction_c=result.temp_reduction_c,
    tree_equivalent_count=result.tree_equivalent_count,
    pdf_bytes=pdf_bytes,
    pdf_filename=pdf_filename,
    excel_bytes=excel_bytes,
    excel_filename=excel_filename,
)

if actions.get("prev_clicked"):
    st.switch_page("pages/3_step3_result.py")

if actions.get("home_clicked"):
    st.switch_page("app.py")

if actions.get("share_image_clicked"):
    st.toast("이미지 저장 기능은 준비 중입니다.")

if actions.get("share_link_clicked"):
    st.toast("링크 공유 기능은 곧 제공될 예정입니다.")

if actions.get("feedback_positive_clicked"):
    st.toast("소중한 피드백 감사합니다!")

if actions.get("feedback_negative_clicked"):
    st.toast("의견을 보내주셔서 감사합니다. 더 나은 서비스를 준비할게요.")

render_footer()