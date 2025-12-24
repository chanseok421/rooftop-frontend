from __future__ import annotations

import math
from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class GreeningTypeInfo:
    code: str
    label: str
    icon: str
    co2_text: str
    subtext: str
    detail_recommendation: str
    detail_co2: str
    detail_temp: str
    detail_feature: str
    badge: str | None = None


TYPE_INFOS: dict[str, GreeningTypeInfo] = {
    "grass": GreeningTypeInfo(
        code="grass",
        label="잔디",
        icon="🌱",
        co2_text="0.4 kg/㎡/년",
        subtext="관리 용이 · 기본형",
        detail_recommendation="잔디 또는 잔디 혼합",
        detail_co2="0.4 kg/㎡/년 (임시값)",
        detail_temp="약 6~10℃ (임시값)",
        detail_feature="관리 용이 · 기본형",
    ),
    "sedum": GreeningTypeInfo(
        code="sedum",
        label="세덤",
        icon="🍃",
        co2_text="0.7 kg/㎡/년",
        subtext="저관리 · 옥상 적합",
        detail_recommendation="Sedum spp. (예: 돌나물류)",
        detail_co2="0.7 kg/㎡/년 (임시값)",
        detail_temp="약 10~15℃ (임시값)",
        detail_feature="저관리 · 경량 · 옥상 적합",
        badge="추천",
    ),
    "shrub": GreeningTypeInfo(
        code="shrub",
        label="관목",
        icon="🌿",
        co2_text="4.0 kg/㎡/년",
        subtext="집약형 · 고효율",
        detail_recommendation="관목류 · 교목 혼합",
        detail_co2="4.0 kg/㎡/년 (임시값)",
        detail_temp="약 12~18℃ (임시값)",
        detail_feature="집약형 · 고효율",
    ),
    "tree": GreeningTypeInfo(
        code="tree",
        label="나무",
        icon="🌳",
        co2_text="확정 예정",
        subtext="하중·구조 검토 필요",
        detail_recommendation="수종·하중·구조 검토 필요",
        detail_co2="추후 확정 예정",
        detail_temp="추후 확정 예정",
        detail_feature="구조 검토 필요",
    ),
}


def _format_number(value: float) -> str:
    if math.isnan(value):
        return "—"
    return f"{value:,.0f}"


def _format_decimal(value: float) -> str:
    if math.isnan(value):
        return "—"
    return f"{value:,.1f}"


def render_planning_ui(
    *,
    roof_area: float,
    selected_type: str,
    coverage_ratio: float,
    green_area_m2: float,
    co2_absorption_kg: float,
    temp_reduction_c: float,
) -> dict:
    st.markdown(
        """
        <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
          font-family: -apple-system, BlinkMacSystemFont, "Noto Sans KR", system-ui, sans-serif;
          background: #f4f6f9;
          color: #1a202c;
          line-height: 1.5;
        }
        a { text-decoration: none; color: inherit; }
        button, input { font: inherit; }
        .page { padding: 28px 0 44px; }
        .container-1320 { width: 100%; max-width: 1320px; margin: 0 auto; padding: 0 20px; }
        .content-1120 { width: 100%; max-width: 1120px; margin: 0 auto; }

        .section-header { padding: 6px 0 10px; }
        .eyebrow { font-size: 12px; color: #2f855a; font-weight: 800; letter-spacing: .08em; }
        .h2 { font-size: 28px; font-weight: 900; margin-top: 6px; }
        .subtitle { font-size: 14px; color: #718096; margin-top: 6px; }

        .stepper { width: 100%; background: #fff; border-radius: 16px; box-shadow: 0 10px 30px rgba(15,23,42,.08); padding: 14px 16px; display: flex; align-items: center; gap: 10px; margin: 16px 0 18px; }
        .step { display: flex; align-items: center; gap: 8px; min-width: 0; }
        .step .dot { width: 10px; height: 10px; border-radius: 999px; background: #cbd5e0; }
        .step .label { font-size: 12px; color: #4a5568; font-weight: 900; white-space: nowrap; }
        .step.active .dot { background: #48bb78; }
        .step.active .label { color: #1a202c; }
        .step.done .dot { background: #2f855a; }
        .step.done .label { color: #1a202c; }
        .line { flex: 1; height: 1px; background: #e2e8f0; }

        .grid { display: grid; grid-template-columns: 1fr 360px; gap: 20px; align-items: start; }
        .side { display: flex; flex-direction: column; gap: 16px; }
        .stack { min-width: 0; }

        .card { background: #fff; border-radius: 20px; padding: 22px 22px; box-shadow: 0 10px 30px rgba(15,23,42,.08); }
        .card-title { font-size: 16px; font-weight: 900; }
        .card-top { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 14px; }
        .pill { display: inline-flex; align-items: center; gap: 8px; font-size: 12px; background: #edf2f7; color: #1a202c; border-radius: 999px; padding: 6px 10px; font-weight: 800; }

        .block { margin-top: 18px; }
        .block-title { font-size: 12px; font-weight: 900; color: #1a202c; margin-bottom: 10px; }

        /* 타입 카드 */
        .type-container { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
        .type-card { position: relative; border: 1px solid #e2e8f0; border-radius: 16px; background: #fff; padding: 14px 12px; text-align: left; transition: all .08s ease; min-height: 138px; }
        .type-card:hover { transform: translateY(-1px); box-shadow: 0 10px 26px rgba(15,23,42,.10); }
        .type-card.selected { border-color: rgba(72,187,120,.65); box-shadow: 0 14px 36px rgba(72,187,120,.14); }
        .type-badge { position: absolute; top: 10px; right: 10px; font-size: 10px; font-weight: 900; background: #48bb78; color: #fff; border-radius: 999px; padding: 3px 8px; }
        .type-icon { width: 36px; height: 36px; border-radius: 999px; background: #f0fff4; display: flex; align-items: center; justify-content: center; font-size: 18px; margin-bottom: 10px; }
        .type-name { font-size: 14px; font-weight: 900; margin-bottom: 6px; }
        .type-meta { display: flex; gap: 6px; align-items: baseline; font-size: 11px; color: #4a5568; }
        .type-meta strong { font-size: 12px; color: #1a202c; }
        .type-sub { font-size: 11px; color: #a0aec0; margin-top: 8px; font-weight: 800; }

        /* 디테일 */
        .detail-panel { border: 1px solid #e2e8f0; border-radius: 16px; padding: 14px 14px; background: #fff; }
        .detail-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 12px; }
        .detail-title { display: flex; align-items: center; gap: 8px; font-weight: 900; }
        .detail-icon { width: 26px; height: 26px; border-radius: 999px; background: #f0fff4; display: flex; align-items: center; justify-content: center; }
        .detail-tag { font-size: 11px; background: #e6fffa; color: #0b7285; border-radius: 999px; padding: 4px 10px; font-weight: 900; }
        .detail-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
        .detail-item { border: 1px solid #edf2f7; border-radius: 14px; padding: 10px 10px; background: #f7fafc; }
        .detail-item .k { font-size: 11px; color: #718096; font-weight: 900; margin-bottom: 4px; }
        .detail-item .v { font-size: 12px; color: #1a202c; font-weight: 800; }

        /* 슬라이더 */
        .slider-row { display: flex; align-items: center; gap: 10px; }
        .slider-label { font-size: 11px; color: #a0aec0; font-weight: 900; white-space: nowrap; }
        .slider-pill { display: inline-flex; align-items: center; justify-content: center; border-radius: 999px; background: #edf2f7; color: #1a202c; font-size: 12px; font-weight: 900; padding: 6px 10px; }

        /* 프리뷰 */
        .preview { margin-top: 14px; border: 1px solid #e2e8f0; border-radius: 16px; padding: 12px 12px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; background: #fff; }
        .preview-item { border: 1px solid #edf2f7; border-radius: 14px; padding: 10px 10px; background: #f7fafc; }
        .preview-item .k { font-size: 11px; color: #718096; font-weight: 900; margin-bottom: 4px; }
        .preview-item .v { font-size: 14px; color: #1a202c; font-weight: 900; }

        .cta-row { display: flex; justify-content: space-between; gap: 12px; margin-top: 16px; }

        .btn { display: inline-flex; align-items: center; justify-content: center; border-radius: 999px; padding: 10px 18px; font-size: 13px; font-weight: 700; border: 1px solid transparent; cursor: pointer; white-space: nowrap; }
        .btn-primary { background: #48bb78; color: #fff; }
        .btn-primary:hover { background: #2f855a; }
        .btn-secondary { background: #edf2f7; color: #1a202c; border-color: #e2e8f0; }
        .btn-secondary:hover { background: #e2e8f0; }
        .btn-ghost { background: transparent; color: #1a202c; border-color: #e2e8f0; }
        .btn-ghost:hover { background: #fff; }

        .bullets { margin-top: 10px; padding-left: 16px; color: #4a5568; font-size: 12px; font-weight: 800; }
        .bullets li { margin-bottom: 6px; }
        .divider { height: 1px; background: #e2e8f0; margin: 14px 0; }
        .link { font-size: 12px; color: #0b3b5b; font-weight: 900; }

        .mini { margin-top: 10px; }
        .mini-k { font-size: 11px; color: #718096; font-weight: 900; letter-spacing: .06em; text-transform: uppercase; }
        .mini-v { font-size: 13px; color: #1a202c; font-weight: 900; margin-top: 4px; }

        /* Streamlit 위젯 커스터마이즈 */
        .type-buttons .stButton > button {
          width: 100%;
          height: 100%;
          text-align: left;
          padding: 0;
          background: transparent;
          border: none;
        }
        .type-buttons .stButton > button:focus { outline: none; box-shadow: none; }

        .slider-holder .stSlider { width: 100%; }
        .slider-holder [data-baseweb="slider"] { width: 100%; }
        .slider-holder .stSlider > div { padding: 6px 0; }
         .slider-holder [data-baseweb="slider"] > div > div { background: #c6f6d5; }
        .slider-holder [data-baseweb="slider"] > div > div > div { background: #2f855a; }
        .slider-holder .stSlider [role="slider"] { background: #2f855a !important; box-shadow: 0 6px 18px rgba(15,23,42,.18); width: 16px; height: 16px; }
        .slider-holder .stSlider [role="slider"]::before { display: none; }
        .slider-holder .stSlider [data-testid=\"stThumbValue\"], .slider-holder [data-baseweb=\"slider\"] [data-baseweb=\"slider-value\"] { color: #2f855a !important; }
        
        

        .cta-row .stButton > button {
          border-radius: 999px;
          padding: 10px 18px;
          font-size: 13px;
          font-weight: 700;
          border: 1px solid #e2e8f0;
          background: transparent;
          color: #1a202c;
        }
        .cta-row .stButton.primary > button {
          background: #48bb78;
          color: #fff;
          border-color: transparent;
        }
        .cta-row .stButton.primary > button:hover { background: #2f855a; }

        @media (max-width: 1100px) {
          .grid { grid-template-columns: 1fr; }
          .type-container { grid-template-columns: repeat(2, 1fr); }
        }
        @media (max-width: 640px) {
          .type-container { grid-template-columns: 1fr; }
          .detail-grid { grid-template-columns: 1fr; }
          .preview { grid-template-columns: 1fr; }
          .cta-row { flex-direction: column; }
          .cta-row .stButton > button { width: 100%; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<main class="page">', unsafe_allow_html=True)
    st.markdown('<div class="container-1320">', unsafe_allow_html=True)
    st.markdown('<div class="content-1120">', unsafe_allow_html=True)

    st.markdown(
        """
        <section class="section-header">
          <div class="eyebrow">SIMULATION · STEP 2</div>
          <h1 class="h2">녹화 계획 설정</h1>
          <p class="subtitle">녹화 유형과 비율을 선택해 내 건물에 맞는 시나리오를 구성합니다.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <section class="stepper" aria-label="simulation steps">
          <div class="step done">
            <div class="dot"></div>
            <div class="label">조건확인</div>
          </div>
          <div class="line"></div>
          <div class="step active">
            <div class="dot"></div>
            <div class="label">계획</div>
          </div>
          <div class="line"></div>
          <div class="step">
            <div class="dot"></div>
            <div class="label">결과</div>
          </div>
          <div class="line"></div>
          <div class="step">
            <div class="dot"></div>
            <div class="label">리포트</div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns([3, 1], gap="large")

    with left_col:
        st.markdown(
            f"""
            <section class="card">
              <div class="card-top">
                <div class="card-title">분석 대상</div>
                <div class="pill">가용면적 <strong>{_format_number(roof_area)}㎡</strong></div>
              </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="block-title">녹화 유형 선택</div>', unsafe_allow_html=True)
        st.markdown('<div class="type-container type-buttons">', unsafe_allow_html=True)

        cols = st.columns(4, gap="small")
        for idx, (type_code, info) in enumerate(TYPE_INFOS.items()):
            with cols[idx]:
                clicked = st.button(
                    f"{info.icon} {info.label}\nCO₂ {info.co2_text}\n{info.subtext}",
                    key=f"type_{type_code}",
                    use_container_width=True,
                )
                if clicked:
                    st.session_state["planning_selected_type"] = type_code
                is_selected = st.session_state.get("planning_selected_type", selected_type) == type_code
                badge_html = f'<div class="type-badge">{info.badge}</div>' if info.badge else ""
                st.markdown(
                    f"""
                    <div class="type-card {'selected' if is_selected else ''}">
                      {badge_html}
                      <div class="type-icon">{info.icon}</div>
                      <div class="type-name">{info.label}</div>
                      <div class="type-meta"><span>CO₂</span><strong>{info.co2_text}</strong></div>
                      <div class="type-sub">{info.subtext}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        selected_type_code = st.session_state.get("planning_selected_type", selected_type)
        selected_info = TYPE_INFOS.get(selected_type_code, TYPE_INFOS["sedum"])

        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="block-title">선택 유형 상세</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="detail-panel">
              <div class="detail-head">
                <div class="detail-title">
                  <span class="detail-icon">{selected_info.icon}</span>
                  <span>{selected_info.label}</span>
                </div>
                <div class="detail-tag">상세 패널</div>
              </div>
              <div class="detail-grid">
                <div class="detail-item">
                  <div class="k">추천 식물</div>
                  <div class="v">{selected_info.detail_recommendation}</div>
                </div>
                <div class="detail-item">
                  <div class="k">CO₂ 흡수량</div>
                  <div class="v">{selected_info.detail_co2}</div>
                </div>
                <div class="detail-item">
                  <div class="k">온도 저감</div>
                  <div class="v">{selected_info.detail_temp}</div>
                </div>
                <div class="detail-item">
                  <div class="k">특징</div>
                  <div class="v">{selected_info.detail_feature}</div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="block">', unsafe_allow_html=True)
        st.markdown('<div class="block-title">녹화 비율</div>', unsafe_allow_html=True)

        st.markdown('<div class="slider-row slider-holder">', unsafe_allow_html=True)
        slider_col, pct_col = st.columns([9, 1], gap="small")
        with slider_col:
            slider_value = st.slider(
                "녹화 비율(%)",
                min_value=0,
                max_value=100,
                step=5,
                value=int(round(coverage_ratio * 100)),
                label_visibility="collapsed",
                key="planning_slider",
            )
        with pct_col:
            st.markdown(
                f'<div class="slider-pill"><strong>{slider_value}%</strong></div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="preview">
              <div class="preview-item">
                <div class="k">녹지 면적</div>
                <div class="v">{_format_number(green_area_m2)}㎡</div>
              </div>
              <div class="preview-item">
                <div class="k">예상 CO₂ 흡수</div>
                <div class="v">{_format_decimal(co2_absorption_kg)}kg/년</div>
              </div>
              <div class="preview-item">
                <div class="k">예상 온도 저감</div>
                <div class="v">{_format_decimal(temp_reduction_c)}℃</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="cta-row">', unsafe_allow_html=True)
        prev_col, save_col, next_col = st.columns([1, 1, 1], gap="small")
        with prev_col:
            prev_clicked = st.button("이전", key="planning_prev")
        with save_col:
            save_clicked = st.button("계획 저장", key="planning_save")
        with next_col:
            next_clicked = st.button("결과 확인하기 →", key="planning_next")
        st.markdown("</div></section>", unsafe_allow_html=True)

    with right_col:
        st.markdown(
            """
            <section class="card">
              <div class="card-title">도움말</div>
              <ul class="bullets">
                <li>유형별 계수는 데이터 분석 결과로 확정됩니다.</li>
                <li>나무는 구조·하중 검토가 필요합니다.</li>
                <li>선택 값은 리포트(PDF) 근거로 포함됩니다.</li>
              </ul>
              <div class="divider"></div>
              <a class="link" href="#">데이터 근거 보기 →</a>
            </section>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <section class="card">
              <div class="card-title">다음 단계</div>
              <div class="mini">
                <div class="mini-k">STEP 3</div>
                <div class="mini-v">Before/After 결과 비교</div>
              </div>
              <div class="divider"></div>
              <a class="btn btn-secondary" href="#" style="width:100%;">결과 페이지 미리보기</a>
            </section>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div></div></main>", unsafe_allow_html=True)

    active_ratio = st.session_state.get("planning_slider", slider_value) / 100

    return {
        "selected_type": selected_type_code,
        "coverage_ratio": active_ratio,
        "prev_clicked": prev_clicked,
        "save_clicked": save_clicked,
        "next_clicked": next_clicked,
    }