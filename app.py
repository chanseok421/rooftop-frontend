import streamlit as st
from ui.landing_ui import render_landing_page
from core.state import ensure_session

def main():
    st.set_page_config(
        page_title="옥상이몽 · Rooftop Greening Effect Simulator",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="collapsed", # 랜딩 페이지에서는 사이드바가 거슬릴 수 있으므로 닫음
    )
    
    # 전역 세션 상태 초기화 (필요시)
    ensure_session()
    
    # 랜딩 페이지 렌더링
    render_landing_page()

if __name__ == "__main__":
    main()
