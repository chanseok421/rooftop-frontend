import streamlit as st

from core.services.analyze_service import AnalyzeService
from components.common.header import render_header
from core.state import get_state

st.set_page_config(page_title="리포트 | 옥상이몽", page_icon="📄", layout="wide")
render_header(active="simulate")

st.header("📄 리포트")
state = get_state()
if not state.get("result"):
    st.warning("먼저 '결과확인' 페이지에서 결과를 계산하세요.")
    st.stop()

svc = AnalyzeService()

st.subheader("PDF 리포트")
if st.button("PDF 생성"):
    pdf_bytes, filename = svc.export_pdf()
    st.download_button(
        label="PDF 다운로드",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
    )

st.subheader("Excel 데이터")
if st.button("Excel 생성"):
    xlsx_bytes, filename = svc.export_excel()
    st.download_button(
        label="Excel 다운로드",
        data=xlsx_bytes,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
