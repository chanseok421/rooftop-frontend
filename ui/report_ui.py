from __future__ import annotations

import base64
import html

import streamlit as st


GREENING_LABELS = {
    "grass": "잔디",
    "sedum": "세덤",
    "shrub": "관목",
    "tree": "나무",
}


def _format_number(value: float, *, decimals: int = 0, default: str = "—") -> str:
    if value is None:
        return default
    fmt = f"{{:,.{decimals}f}}" if decimals > 0 else "{:,}"  # noqa: P103
    return fmt.format(value)


def _format_percent(ratio: float | None) -> str:
    if ratio is None:
        return "—"
    return _format_number(ratio * 100, decimals=0) + "%"


def _escape(text: str) -> str:
    return html.escape(text or "")


def _build_data_href(data: bytes, mime: str) -> str:
    encoded = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def render_report_ui(
    *,
    address_title: str,
    address_caption: str,
    greening_type_code: str,
    coverage_ratio: float,
    green_area_m2: float,
    co2_absorption_kg: float,
    temp_reduction_c: float,
    tree_equivalent_count: int,
    pdf_bytes: bytes,
    pdf_filename: str,
    excel_bytes: bytes,
    excel_filename: str,
) -> dict:
    coverage_percent = _format_percent(coverage_ratio)
    green_area_display = _format_number(green_area_m2, decimals=0)
    co2_display = _format_number(co2_absorption_kg, decimals=1)
    temp_display = f"-{_format_number(abs(temp_reduction_c), decimals=1)}"
    tree_display = _format_number(tree_equivalent_count, decimals=0)
    greening_label = GREENING_LABELS.get(greening_type_code, greening_type_code)

    pdf_href = _build_data_href(pdf_bytes, "application/pdf")
    excel_href = _build_data_href(
        excel_bytes, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.html(
        """
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{
  font-family:-apple-system,BlinkMacSystemFont,"Noto Sans KR",system-ui,sans-serif;
  background:#f4f6f9;
  color:#1a202c;
  line-height:1.5;
}
a{text-decoration:none;color:inherit}
button,input{font:inherit}
.page{padding:28px 0 44px}

.container-1320{width:100%;max-width:1320px;margin:0 auto;padding:0 20px}
.content-1120{width:100%;max-width:1120px;margin:0 auto}

.section-header{padding:6px 0 10px}
.eyebrow{font-size:12px;color:#2f855a;font-weight:800;letter-spacing:.08em}
.h2{font-size:28px;font-weight:900;margin-top:6px}
.subtitle{font-size:14px;color:#718096;margin-top:6px}

.stepper{width:100%;background:#fff;border-radius:16px;box-shadow:0 10px 30px rgba(15,23,42,.08);padding:14px 16px;display:flex;align-items:center;gap:10px;margin:16px 0 18px}
.step{display:flex;align-items:center;gap:8px;min-width:0}
.step .dot{width:10px;height:10px;border-radius:999px;background:#cbd5e0}
.step .label{font-size:12px;color:#4a5568;font-weight:900;white-space:nowrap}
.step.active .dot{background:#48bb78}
.step.active .label{color:#1a202c}
.step.done .dot{background:#2f855a}
.step.done .label{color:#1a202c}
.line{flex:1;height:1px;background:#e2e8f0}

.complete-banner{text-align:center;padding:24px 16px;margin-bottom:18px}
.complete-icon{width:56px;height:56px;border-radius:999px;background:linear-gradient(135deg,#48bb78,#2f855a);color:#fff;font-size:28px;display:inline-flex;align-items:center;justify-content:center;margin-bottom:12px;box-shadow:0 10px 30px rgba(72,187,120,.3)}
.complete-title{font-size:22px;font-weight:900;margin-bottom:6px;color:#1a202c}
.complete-desc{font-size:13px;color:#718096}

.grid{display:grid;grid-template-columns:1fr 300px;gap:20px;align-items:start}
.stack{display:flex;flex-direction:column;gap:16px}
.side{display:flex;flex-direction:column;gap:16px}

.card{background:#fff;border-radius:20px;padding:20px;box-shadow:0 10px 30px rgba(15,23,42,.08)}
.card-title{font-size:15px;font-weight:900;margin-bottom:14px}

.card-header-bar{display:flex;align-items:center;gap:12px;padding:14px;background:linear-gradient(135deg,#0b3b5b,#1a5276);border-radius:14px;margin-bottom:14px}
.building-icon{width:40px;height:40px;background:rgba(255,255,255,.15);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px}
.building-info{color:#fff}
.building-name{font-size:15px;font-weight:900;margin-bottom:2px}
.building-meta{font-size:11px;opacity:.85}

.result-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
.result-item{padding:14px 12px;background:#f7fafc;border:1px solid #e2e8f0;border-radius:14px;text-align:center}
.result-icon{font-size:22px;margin-bottom:6px}
.result-value{font-size:20px;font-weight:900;color:#1a202c}
.result-unit{font-size:11px;color:#718096;font-weight:700}
.result-label{font-size:10px;color:#718096;font-weight:700;margin-top:4px}

.download-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-bottom:10px}
.download-btn{display:flex;flex-direction:column;align-items:center;gap:4px;padding:16px 12px;border-radius:14px;border:none;font-weight:700;color:#fff;cursor:pointer;transition:transform .1s ease}
.download-btn:hover{transform:translateY(-2px)}
.download-btn.pdf{background:linear-gradient(135deg,#e53e3e,#c53030)}
.download-btn.excel{background:linear-gradient(135deg,#48bb78,#2f855a)}
.download-icon{font-size:22px}
.download-text{font-size:13px}
.download-desc{font-size:10px;opacity:.85;font-weight:600}

.share-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
.share-grid .stButton>button{display:flex;align-items:center;justify-content:center;gap:6px;padding:10px;background:#edf2f7;border:1px solid #e2e8f0;border-radius:10px;font-size:12px;font-weight:700;color:#4a5568;cursor:pointer;width:100%}
.share-grid .stButton>button:hover{background:#e2e8f0}
.share-icon{font-size:14px}

.feedback-card{background:#f0fff4;border-radius:14px;padding:14px;text-align:center}
.feedback-title{font-size:12px;font-weight:700;color:#2d3748;margin-bottom:10px}
.feedback-btns{display:flex;gap:8px;justify-content:center}
.feedback-btns .stButton>button{padding:8px 14px;border-radius:999px;font-size:12px;font-weight:700;border:1px solid transparent;cursor:pointer;width:100%}
.feedback-btns .stButton>button:hover{background:#f7fafc}
.feedback-btns .positive>button{background:#48bb78;color:#fff}
.feedback-btns .positive>button:hover{background:#2f855a}
.feedback-btns .negative>button{background:#fff;border-color:#e2e8f0;color:#4a5568}
.feedback-btns .negative>button:hover{background:#f7fafc}

.info-list{display:flex;flex-direction:column;gap:8px}
.info-item{display:flex;align-items:center;gap:10px;padding:12px;background:#f7fafc;border:1px solid #e2e8f0;border-radius:12px}
.info-item:hover{background:#fff;border-color:#48bb78}
.info-icon{width:32px;height:32px;background:#e6fffa;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0}
.info-content{flex:1;min-width:0}
.info-name{font-size:12px;font-weight:900;color:#1a202c;margin-bottom:2px}
.info-desc{font-size:10px;color:#718096}
.info-arrow{font-size:12px;color:#a0aec0;font-weight:700}

.cta-row{display:flex;justify-content:space-between;align-items:center;gap:10px}
.cta-row .stButton>button{width:100%;border-radius:999px;padding:10px 18px;font-size:13px;font-weight:700;border:1px solid #e2e8f0;background:transparent;color:#1a202c}
.cta-row .stButton.next>button{background:#48bb78;color:#fff;border-color:transparent}
.cta-row .stButton.next>button:hover{background:#2f855a}
.cta-row .stButton.prev>button:hover{background:#fff}

.bullets{padding-left:16px;color:#4a5568;font-size:11px}
.bullets li{margin-bottom:6px;line-height:1.5}
.divider{height:1px;background:#e2e8f0;margin:14px 0}
.link{font-size:11px;color:#0b3b5b;font-weight:900}

.footer{border-top:1px solid #e2e8f0;padding:22px 0 30px;font-size:12px;color:#a0aec0}
.footer-inner{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap}
.footer-links{display:flex;gap:16px}

@media (max-width:900px){
  .grid{grid-template-columns:1fr}
  .result-grid{grid-template-columns:repeat(2,1fr)}
}
@media (max-width:640px){
  .result-grid{grid-template-columns:1fr}
  .download-grid{grid-template-columns:1fr}
  .share-grid{grid-template-columns:1fr}
  .feedback-btns{flex-direction:column}
  .cta-row{flex-direction:column}
  .cta-row .stButton>button{width:100%}
}
</style>
"""
    )

    st.html('<main class="page">')
    st.html('<div class="container-1320">')
    st.html('<div class="content-1120">')

    st.html(
        """
<section class="section-header">
  <div class="eyebrow">SIMULATION · STEP 4</div>
  <h1 class="h2">리포트 다운로드</h1>
  <p class="subtitle">시뮬레이션 결과를 PDF, Excel 등 다양한 형식으로 저장하세요.</p>
</section>
"""
    )

    st.html(
        """
<section class="stepper" aria-label="simulation steps">
  <div class="step done">
    <div class="dot"></div>
    <div class="label">조건확인</div>
  </div>
  <div class="line"></div>
  <div class="step done">
    <div class="dot"></div>
    <div class="label">계획</div>
  </div>
  <div class="line"></div>
  <div class="step done">
    <div class="dot"></div>
    <div class="label">결과</div>
  </div>
  <div class="line"></div>
  <div class="step active">
    <div class="dot"></div>
    <div class="label">리포트</div>
  </div>
</section>
"""
    )

    st.html(
        """
<section class="complete-banner">
  <div class="complete-icon">✓</div>
  <h2 class="complete-title">시뮬레이션 완료!</h2>
  <p class="complete-desc">결과 리포트를 다운로드하고 활용하세요.</p>
</section>
"""
    )

    st.html('<section class="grid">')
    st.html('<div class="stack">')

    st.html(
        f"""
<div class="card">
  <div class="card-header-bar">
    <div class="building-icon">🏢</div>
    <div class="building-info">
      <div class="building-name">{_escape(address_title)}</div>
      <div class="building-meta">{_escape(address_caption)} · {_escape(greening_label)} · 녹화 {coverage_percent}</div>
    </div>
  </div>

  <div class="result-grid">
    <div class="result-item">
      <div class="result-icon">🌿</div>
      <div class="result-value">{green_area_display} <span class="result-unit">㎡</span></div>
      <div class="result-label">녹화 면적</div>
    </div>
    <div class="result-item">
      <div class="result-icon">💨</div>
      <div class="result-value">{co2_display} <span class="result-unit">kg/년</span></div>
      <div class="result-label">CO₂ 흡수량</div>
    </div>
    <div class="result-item">
      <div class="result-icon">🌡️</div>
      <div class="result-value">{temp_display} <span class="result-unit">℃</span></div>
      <div class="result-label">온도 저감</div>
    </div>
    <div class="result-item">
      <div class="result-icon">🌲</div>
      <div class="result-value">{tree_display} <span class="result-unit">그루</span></div>
      <div class="result-label">소나무 환산</div>
    </div>
  </div>
</div>
"""
    )

    st.html('<div class="card">')
    st.html('<div class="card-title">📥 리포트 다운로드</div>')
    st.html(
        f"""
<div class="download-grid">
  <a class="download-btn pdf" href="{pdf_href}" download="{_escape(pdf_filename)}">
    <span class="download-icon">📄</span>
    <span class="download-text">PDF 리포트</span>
    <span class="download-desc">정책 제안용</span>
  </a>
  <a class="download-btn excel" href="{excel_href}" download="{_escape(excel_filename)}">
    <span class="download-icon">📊</span>
    <span class="download-text">Excel 데이터</span>
    <span class="download-desc">상세 데이터</span>
  </a>
</div>
"""
    )

    st.html('<div class="share-grid">')
    share_image_col, share_link_col = st.columns(2, gap="small")
    with share_image_col:
        share_image_clicked = st.button("🖼️ 이미지 저장", key="report_share_image")
    with share_link_col:
        share_link_clicked = st.button("🔗 링크 공유", key="report_share_link")
    st.html("</div>")
    st.html("</div>")

    st.html('<div class="feedback-card">')
    st.html(
        '<div class="feedback-title">이 시뮬레이터가 도움이 되셨나요?</div>'
    )
    st.html('<div class="feedback-btns">')
    feedback_pos_col, feedback_neg_col = st.columns(2, gap="small")
    with feedback_pos_col:
        feedback_positive_clicked = st.button("👍 도움이 됐어요", key="report_feedback_positive")
    with feedback_neg_col:
        feedback_negative_clicked = st.button("💬 개선이 필요해요", key="report_feedback_negative")
    st.html("</div>")
    st.html("</div>")

    st.html('<div class="cta-row">')
    prev_col, home_col = st.columns([1, 1], gap="small")
    with prev_col:
        prev_clicked = st.button("← 이전: 결과 보기", key="report_prev")
    with home_col:
        home_clicked = st.button("🏠 처음으로 돌아가기", key="report_home")
    st.html("</div>")

    st.html("</div>")

    st.html('<aside class="side">')
    st.html(
        """
<div class="card">
  <div class="card-title">📚 관련 정보</div>

  <div class="info-list">
    <a class="info-item" href="#">
      <div class="info-icon">🏛️</div>
      <div class="info-content">
        <div class="info-name">G-SEED 녹색건축인증 안내</div>
        <div class="info-desc">인증 절차 및 혜택 확인</div>
      </div>
      <div class="info-arrow">→</div>
    </a>
    <a class="info-item" href="#">
      <div class="info-icon">🏢</div>
      <div class="info-content">
        <div class="info-name">서울시 옥상녹화 지원사업</div>
        <div class="info-desc">보조금 및 지원 조건 확인</div>
      </div>
      <div class="info-arrow">→</div>
    </a>
    <a class="info-item" href="#">
      <div class="info-icon">📖</div>
      <div class="info-content">
        <div class="info-name">옥상녹화 시공 가이드</div>
        <div class="info-desc">녹화 유형별 시공 안내</div>
      </div>
      <div class="info-arrow">→</div>
    </a>
  </div>

  <div class="divider"></div>
  <a class="link" href="#">데이터 근거 보기 →</a>
</div>
"""
    )

    st.html(
        """
<div class="card">
  <div class="card-title">💡 활용 팁</div>
  <ul class="bullets">
    <li><strong>정책 담당자:</strong> PDF 리포트를 G-SEED 개정 근거 자료로 활용하세요.</li>
    <li><strong>건물주:</strong> Excel 데이터로 상세 비용-효과 분석이 가능합니다.</li>
    <li><strong>공유:</strong> 링크를 통해 동료에게 결과를 공유하세요.</li>
  </ul>
</div>
"""
    )

    st.html("</aside>")
    st.html("</section>")
    st.html("</div></div></main>")


    return {
        "prev_clicked": prev_clicked,
        "home_clicked": home_clicked,
        "share_image_clicked": share_image_clicked,
        "share_link_clicked": share_link_clicked,
        "feedback_positive_clicked": feedback_positive_clicked,
        "feedback_negative_clicked": feedback_negative_clicked,
    }