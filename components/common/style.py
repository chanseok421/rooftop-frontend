import streamlit as st

def apply_common_styles():
    """
    모든 페이지에 공통적으로 적용되는 CSS 스타일을 주입합니다.
    - 메인 컨테이너 너비 제한 (1120px)
    - 상단/하단 패딩 조정
    - 전체 배경색 설정
    """
    st.markdown("""
        <style>
        /* Streamlit 기본 앱 컨테이너 (배경색) */
        [data-testid="stApp"] {
            background-color: #F4F6F9;
        }
        
        /* 메인 블록 컨테이너 (전체 너비 허용) */
        [data-testid="stMainBlockContainer"] {
            width: 100%;
            max-width: none;
            padding-top: 40px !important;
            padding-bottom: 100px;
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        
        /* 모든 직계 자식 요소를 1120px로 제한 및 중앙 정렬 (모바일 여백 포함) */
        [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] > div {
            max-width: 1120px;
            margin: 0 auto;
            width: 100%;
            padding-left: 20px;
            padding-right: 20px;
        }
        
        /* 헤더(Iframe)는 전체 너비 및 여백 없음 */
        [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] > div:has(iframe),
        [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] > div:has(.app-header),
        [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] > div:has(.stepper-container) {
            max-width: none;
            width: 100%;
            padding-left: 0;
            padding-right: 0;
        }
        
        /* Streamlit 기본 헤더 숨김 (선택사항, 커스텀 헤더 사용 시 유용) */
        /* header[data-testid="stHeader"] { display: none; } */
        
        /* 폰트 설정 (선택사항) */
        * {
            font-family: -apple-system, BlinkMacSystemFont, "Noto Sans KR", system-ui, sans-serif;
        }
        </style>
    """, unsafe_allow_html=True)
