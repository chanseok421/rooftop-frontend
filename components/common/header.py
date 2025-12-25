import streamlit as st
import streamlit.components.v1 as components

def get_header_css():
    """헤더 CSS 반환"""
    return """
    .app-header {
        background: #0b3b5b;
        color: #fff;
        width: 100%;
        position: relative;
        z-index: 9999;
    }
    .container-1320 {
        width: 100%;
        max-width: 1320px;
        margin: 0 auto;
        padding: 0 20px;
    }
    .header-inner {
        height: 64px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
    }
    .logo {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 800;
        cursor: pointer;
    }
    .logo-mark {
        width: 24px;
        height: 24px;
        border-radius: 999px;
        background: linear-gradient(135deg, #48bb78, #2f855a);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
    }
    .logo-text { font-size: 18px; }
    .nav {
        display: flex;
        align-items: center;
        gap: 22px;
        font-size: 13px;
    }
    .nav-link {
        opacity: 0.9;
        text-decoration: none;
        color: inherit;
        cursor: pointer;
    }
    .nav-link:hover { opacity: 1; }
    .nav-link.active {
        opacity: 1;
        font-weight: 600;
    }
    """

def get_header_html(active_page: str = None):
    """
    헤더 HTML 문자열을 반환합니다.
    다른 섹션과 합쳐서 하나의 components.html()로 렌더링할 때 사용합니다.
    
    Args:
        active_page: 현재 활성화된 페이지 ("intro", "data", "gseed", "contact" 중 하나)
    
    Returns:
        str: 헤더 HTML 문자열
    """
    
    def get_class(page_name):
        return "nav-link active" if active_page == page_name else "nav-link"
    
    return f"""
    <header class="app-header">
      <div class="container-1320 header-inner">
        <div class="logo">
          <div class="logo-mark">옥</div>
          <span class="logo-text">옥상이몽</span>
        </div>
        <nav class="nav">
          <a class="{get_class('intro')}" href="#">서비스 소개</a>
          <a class="{get_class('data')}" href="#">데이터 근거</a>
          <a class="{get_class('gseed')}" href="/gseed" target="_top">G-SEED란?</a>
          <a class="{get_class('contact')}" href="#">문의하기</a>
        </nav>
      </div>
    </header>
    """

def render_header(active_page: str = None):
    """
    공통 헤더를 단독으로 렌더링합니다.
    헤더만 따로 표시할 때 사용합니다.
    """
    css = get_header_css()
    html = get_header_html(active_page)
    
    full_html = f"""
    <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ 
        font-family: -apple-system, BlinkMacSystemFont, "Noto Sans KR", system-ui, sans-serif;
        margin: 0; padding: 0; background: #0b3b5b; height: 100%;
    }}
    {css}
    </style>
    {html}
    """
    st.html(full_html)


def get_stepper_css():
    """스테퍼 CSS 반환"""
    return """
    .stepper-container {
        background: #f8fafc;
        padding: 16px 0;
        border-bottom: 1px solid #e2e8f0;
    }
    .stepper {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
    }
    .step {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .step-dot {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: 600;
    }
    .step-dot.active {
        background: #48bb78;
        color: white;
    }
    .step-dot.done {
        background: #48bb78;
        color: white;
    }
    .step-dot.pending {
        background: #e2e8f0;
        color: #a0aec0;
    }
    .step-label {
        font-size: 12px;
        color: #718096;
    }
    .step-label.active {
        color: #2f855a;
        font-weight: 600;
    }
    .step-line {
        width: 40px;
        height: 2px;
        background: #e2e8f0;
    }
    .step-line.done {
        background: #48bb78;
    }
    """

def get_stepper_html(current_step: int = 1):
    """스테퍼 HTML 문자열을 반환합니다."""
    steps = [
        {"num": 1, "label": "주소입력", "icon": "📍"},
        {"num": 2, "label": "면적확인", "icon": "📐"},
        {"num": 3, "label": "녹화계획", "icon": "🌿"},
        {"num": 4, "label": "결과확인", "icon": "📊"},
        {"num": 5, "label": "리포트", "icon": "📄"},
    ]
    
    steps_html = ""
    for i, step in enumerate(steps):
        if step["num"] < current_step:
            dot_class, label_class, dot_content = "done", "", "✓"
        elif step["num"] == current_step:
            dot_class, label_class, dot_content = "active", "active", step["icon"]
        else:
            dot_class, label_class, dot_content = "pending", "", step["num"]
        
        steps_html += f"""
        <div class="step">
            <div class="step-dot {dot_class}">{dot_content}</div>
            <span class="step-label {label_class}">{step['label']}</span>
        </div>
        """
        
        if i < len(steps) - 1:
            line_class = "done" if step["num"] < current_step else ""
            steps_html += f'<div class="step-line {line_class}"></div>'
    
    return f"""
    <div class="stepper-container">
      <div class="container-1320">
        <div class="stepper">
          {steps_html}
        </div>
      </div>
    </div>
    """

def render_header_with_stepper(current_step: int = 1):
    """헤더 + 스텝 진행바를 함께 렌더링합니다."""
    css = get_header_css() + get_stepper_css()
    header_html = get_header_html()
    stepper_html = get_stepper_html(current_step)
    
    full_html = f"""
    <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ 
        font-family: -apple-system, BlinkMacSystemFont, "Noto Sans KR", system-ui, sans-serif;
        margin: 0; padding: 0; background: #f8fafc; height: 100%;
    }}
    {css}
    </style>
    {header_html}
    {stepper_html}
    """
    st.html(full_html)
