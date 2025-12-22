import streamlit as st
import streamlit.components.v1 as components

def get_footer_css():
    """푸터 CSS 반환"""
    return """
    .footer {
        border-top: 1px solid #e2e8f0;
        padding: 22px 0 30px;
        font-size: 12px;
        color: #a0aec0;
        background: #f4f6f9;
    }
    .footer-inner {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 14px;
        flex-wrap: wrap;
    }
    .footer-links {
        display: flex;
        gap: 16px;
    }
    .footer-links a:hover {
        color: #718096;
    }
    """

def get_footer_html():
    """
    푸터 HTML 문자열을 반환합니다.
    다른 섹션과 합쳐서 하나의 components.html()로 렌더링할 때 사용합니다.
    
    Returns:
        str: 푸터 HTML 문자열
    """
    return """
    <footer class="footer">
      <div class="container-1320 footer-inner">
        <div>© 2025 옥상이몽 · Rooftop Greening Effect Simulator</div>
        <div class="footer-links">
          <a href="#">개인정보처리방침</a>
          <a href="#">문의하기</a>
        </div>
      </div>
    </footer>
    """

def render_footer():
    """
    공통 푸터를 단독으로 렌더링합니다.
    푸터만 따로 표시할 때 사용합니다.
    """
    css = get_footer_css()
    html = get_footer_html()
    
    full_html = f"""
    <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ 
        font-family: -apple-system, BlinkMacSystemFont, "Noto Sans KR", system-ui, sans-serif;
        margin: 0; padding: 0; background: #f4f6f9; height: 100%;
    }}
    a {{ text-decoration: none; color: inherit; }}
    .container-1320 {{
        width: 100%;
        max-width: 1320px;
        margin: 0 auto;
        padding: 0 20px;
    }}
    {css}
    </style>
    {html}
    """
    components.html(full_html, height=80, scrolling=False)
