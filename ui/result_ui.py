from __future__ import annotations

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


def render_result_ui(
    *,
    address_title: str,
    address_caption: str,
    greening_type_code: str,
    coverage_ratio: float,
    roof_area_m2: float,
    green_area_m2: float,
    co2_absorption_kg: float,
    temp_reduction_c: float,
    baseline_surface_temp_c: float,
    after_surface_temp_c: float,
    tree_equivalent_count: int,
    co2_coefficient: float | None = None,
    temp_coefficient: float | None = None,
    pine_factor_kg_per_year: float | None = None,
) -> dict:
    coverage_percent = _format_percent(coverage_ratio)
    green_area_display = _format_number(green_area_m2, decimals=0)
    roof_area_display = _format_number(roof_area_m2, decimals=0)
    co2_display = _format_number(co2_absorption_kg, decimals=1)
    temp_reduction_display = f"-{_format_number(abs(temp_reduction_c), decimals=1)}"
    temp_detail = f"{_format_number(baseline_surface_temp_c, decimals=1)}℃ → {_format_number(after_surface_temp_c, decimals=1)}℃"
    greening_label = GREENING_LABELS.get(greening_type_code, greening_type_code)
    tree_icons = "🌲" * min(tree_equivalent_count, 5)

    co2_coeff_text = _format_number(co2_coefficient, decimals=1) if co2_coefficient is not None else None
    temp_coeff_text = _format_number(temp_coefficient, decimals=1) if temp_coefficient is not None else None
    pine_factor_text = _format_number(pine_factor_kg_per_year, decimals=1) if pine_factor_kg_per_year is not None else None

    st.markdown(
        f"""
        <style>
        *{{box-sizing:border-box;margin:0;padding:0}}
        html,body{{height:100%}}
        body{{
          font-family:-apple-system,BlinkMacSystemFont,"Noto Sans KR",system-ui,sans-serif;
          background:#f4f6f9;
          color:#1a202c;
          line-height:1.5;
        }}
        a{{text-decoration:none;color:inherit}}
        button,input{{font:inherit}}
        .page{{padding:28px 0 44px}}

        .container-1320{{width:100%;max-width:1320px;margin:0 auto;padding:0 20px}}
        .content-1120{{width:100%;max-width:1120px;margin:0 auto}}

        .app-header{{background:#0b3b5b;color:#fff;position:sticky;top:0;z-index:50}}
        .header-inner{{height:64px;display:flex;align-items:center;justify-content:space-between;gap:16px}}
        .logo{{display:flex;align-items:center;gap:10px;font-weight:800}}
        .logo-mark{{width:24px;height:24px;border-radius:999px;background:linear-gradient(135deg,#48bb78,#2f855a);display:flex;align-items:center;justify-content:center;font-size:14px}}
        .logo-text{{font-size:18px}}
        .nav{{display:flex;align-items:center;gap:22px;font-size:13px}}
        .nav-link{{opacity:.9}}
        .nav-link:hover{{opacity:1}}

        .btn{{display:inline-flex;align-items:center;justify-content:center;border-radius:999px;padding:10px 18px;font-size:13px;font-weight:700;border:1px solid transparent;cursor:pointer;white-space:nowrap}}
        .btn-outline{{border-color:rgba(255,255,255,.6);color:#fff;background:transparent;padding:8px 14px}}
        .btn-primary{{background:#48bb78;color:#fff}}
        .btn-primary:hover{{background:#2f855a}}
        .btn-ghost{{background:transparent;color:#1a202c;border-color:#e2e8f0}}
        .btn-ghost:hover{{background:#fff}}

        .section-header{{padding:6px 0 10px}}
        .eyebrow{{font-size:12px;color:#2f855a;font-weight:800;letter-spacing:.08em}}
        .h2{{font-size:28px;font-weight:900;margin-top:6px}}
        .subtitle{{font-size:14px;color:#718096;margin-top:6px}}

        .stepper{{width:100%;background:#fff;border-radius:16px;box-shadow:0 10px 30px rgba(15,23,42,.08);padding:14px 16px;display:flex;align-items:center;gap:10px;margin:16px 0 18px}}
        .step{{display:flex;align-items:center;gap:8px;min-width:0}}
        .step .dot{{width:10px;height:10px;border-radius:999px;background:#cbd5e0}}
        .step .label{{font-size:12px;color:#4a5568;font-weight:900;white-space:nowrap}}
        .step.active .dot{{background:#48bb78}}
        .step.active .label{{color:#1a202c}}
        .step.done .dot{{background:#2f855a}}
        .step.done .label{{color:#1a202c}}
        .line{{flex:1;height:1px;background:#e2e8f0}}

        .summary-bar{{display:flex;align-items:center;gap:14px;background:#fff;border-radius:16px;padding:12px 18px;box-shadow:0 10px 30px rgba(15,23,42,.08);margin-bottom:18px;flex-wrap:wrap}}
        .summary-item{{display:flex;align-items:center;gap:6px}}
        .summary-icon{{font-size:16px}}
        .summary-label{{font-size:13px;font-weight:900;color:#1a202c}}
        .summary-sub{{font-size:11px;color:#718096;font-weight:600}}
        .summary-divider{{width:1px;height:20px;background:#e2e8f0}}

        .grid{{display:grid;grid-template-columns:1fr 300px;gap:20px;align-items:start}}
        .stack{{display:flex;flex-direction:column;gap:16px}}
        .side{{display:flex;flex-direction:column;gap:16px}}

        .card{{background:#fff;border-radius:20px;padding:20px;box-shadow:0 10px 30px rgba(15,23,42,.08)}}
        .card-title{{font-size:15px;font-weight:900;margin-bottom:8px}}
        .card-desc{{font-size:12px;color:#718096;margin-bottom:14px}}

        .viz-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
        .viz-item{{padding:16px 12px;background:#f7fafc;border:1px solid #e2e8f0;border-radius:14px;text-align:center}}
        .viz-icon{{font-size:28px;margin-bottom:8px}}
        .viz-label{{font-size:11px;color:#718096;font-weight:700;margin-bottom:4px}}
        .viz-value{{font-size:20px;font-weight:900;color:#1a202c}}
        .viz-unit{{font-size:11px;color:#718096;font-weight:700}}
        .viz-sub{{font-size:10px;color:#a0aec0;margin-top:4px}}

        .temp-bars{{display:flex;justify-content:center;gap:8px;margin-bottom:8px}}
        .temp-bar{{width:24px;height:50px;border-radius:12px}}
        .temp-bar.hot{{background:linear-gradient(180deg,#fc8181,#e53e3e)}}
        .temp-bar.cool{{background:linear-gradient(180deg,#68d391,#48bb78)}}
        .temp-detail{{font-size:10px;color:#718096;margin-top:4px}}

        .tree-icons{{font-size:16px;margin-bottom:8px;letter-spacing:2px}}

        .highlight-green{{color:#2f855a}}
        .highlight-cool{{color:#3182ce}}

        .compare-grid{{display:grid;grid-template-columns:1fr auto 1fr;gap:14px;align-items:stretch}}
        .compare-card{{padding:14px;border-radius:14px;border:1px solid #e2e8f0;background:#f7fafc}}
        .compare-card.after{{border-color:#48bb78;background:#f0fff4}}
        .compare-badge{{display:inline-block;font-size:10px;font-weight:900;padding:3px 8px;border-radius:999px;background:#edf2f7;color:#4a5568;margin-bottom:4px}}
        .compare-badge.after{{background:#c6f6d5;color:#2f855a}}
        .compare-sub{{font-size:11px;color:#718096;margin-bottom:8px}}
        .compare-icon{{font-size:28px;text-align:center;margin-bottom:10px}}
        .compare-stats{{display:flex;flex-direction:column;gap:6px}}
        .stat-row{{display:flex;justify-content:space-between;font-size:11px;padding:6px 8px;background:#fff;border-radius:8px}}
        .stat-label{{color:#718096;font-weight:700}}
        .stat-value{{font-weight:900;color:#1a202c}}
        .stat-value.green{{color:#2f855a}}
        .stat-value.cool{{color:#3182ce}}
        .stat-value.hot{{color:#e53e3e}}

        .compare-arrow{{display:flex;align-items:center;justify-content:center;width:36px;height:36px;background:#48bb78;color:#fff;border-radius:999px;font-size:16px;font-weight:900;align-self:center}}

        .callout{{display:flex;gap:12px;padding:14px;background:#e6fffa;border-radius:14px}}
        .callout-icon{{font-size:24px}}
        .callout-content{{flex:1}}
        .callout-title{{font-size:13px;font-weight:900;color:#0b7285;margin-bottom:8px}}
        .callout-list{{padding-left:16px;font-size:11px;color:#2d3748}}
        .callout-list li{{margin-bottom:4px}}

        .cta-row{{display:flex;justify-content:space-between;align-items:center;gap:10px}}

        .bullets{{margin-top:8px;padding-left:16px;color:#4a5568;font-size:12px;font-weight:800}}
        .bullets li{{margin-bottom:6px}}
        .divider{{height:1px;background:#e2e8f0;margin:14px 0}}
        .link{{font-size:12px;color:#0b3b5b;font-weight:900}}

        .footer{{border-top:1px solid #e2e8f0;padding:22px 0 30px;font-size:12px;color:#a0aec0}}
        .footer-inner{{display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap}}
        .footer-links{{display:flex;gap:16px}}

        @media (max-width:900px){{
          .grid{{grid-template-columns:1fr}}
          .viz-grid{{grid-template-columns:1fr}}
          .compare-grid{{grid-template-columns:1fr;gap:10px}}
          .compare-arrow{{transform:rotate(90deg);margin:0 auto}}
        }}
        @media (max-width:640px){{
          .nav{{gap:10px;font-size:12px}}
          .summary-bar{{flex-direction:column;align-items:flex-start;gap:8px}}
          .summary-divider{{display:none}}
          .cta-row{{flex-direction:column}}
        }}

        /* Streamlit control styles */
        .cta-row .stButton > button{{
          width:100%;
          border-radius:999px;
          padding:10px 18px;
          font-size:13px;
          font-weight:700;
          border:1px solid #e2e8f0;
          background:transparent;
          color:#1a202c;
        }}
        .cta-row .stButton.next > button{{
          background:#48bb78;
          color:#fff;
          border-color:transparent;
        }}
        .cta-row .stButton.next > button:hover{{background:#2f855a}}
        .cta-row .stButton.prev > button:hover{{background:#fff}}
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
          <div class="eyebrow">SIMULATION · STEP 3</div>
          <h1 class="h2">시뮬레이션 결과</h1>
          <p class="subtitle">옥상녹화 적용 시 예상되는 환경 효과를 확인하세요.</p>
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
          <div class="step done">
            <div class="dot"></div>
            <div class="label">계획</div>
          </div>
          <div class="line"></div>
          <div class="step active">
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

    st.markdown(
        f"""
        <section class=\"summary-bar\">
          <div class=\"summary-item\">
            <span class=\"summary-icon\">📍</span>
            <span class=\"summary-label\">{_escape(address_title)}</span>
            <span class=\"summary-sub\">{_escape(address_caption)}</span>
          </div>
          <div class=\"summary-divider\"></div>
          <div class=\"summary-item\">
            <span class=\"summary-label\">{_escape(greening_label)}</span>
            <span class=\"summary-sub\">녹화 유형</span>
          </div>
          <div class=\"summary-divider\"></div>
          <div class=\"summary-item\">
            <span class=\"summary-label\">{coverage_percent}</span>
            <span class=\"summary-sub\">녹화 비율</span>
          </div>
          <div class=\"summary-divider\"></div>
          <div class=\"summary-item\">
            <span class=\"summary-label\">{green_area_display}㎡</span>
            <span class=\"summary-sub\">녹지 면적</span>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<section class="grid">', unsafe_allow_html=True)

    st.markdown('<div class="stack">', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class=\"card\">
          <div class=\"card-title\">환경 효과 시뮬레이션</div>
          <p class=\"card-desc\">옥상녹화로 기대되는 연간 환경 개선 효과입니다.</p>

          <div class=\"viz-grid\">
            <div class=\"viz-item\">
              <div class=\"viz-icon\">🌿</div>
              <div class=\"viz-label\">CO₂ 흡수량</div>
              <div class=\"viz-value\">{co2_display} <span class=\"viz-unit\">kg/년</span></div>
            </div>

            <div class=\"viz-item\">
              <div class=\"temp-bars\">
                <div class=\"temp-bar hot\"></div>
                <div class=\"temp-bar cool\"></div>
              </div>
              <div class=\"viz-label\">표면 온도 저감</div>
              <div class=\"viz-value highlight-cool\">{temp_reduction_display} <span class=\"viz-unit\">℃</span></div>
              <div class=\"temp-detail\">{temp_detail}</div>
            </div>

            <div class=\"viz-item\">
              <div class=\"tree-icons\">{tree_icons}</div>
              <div class=\"viz-label\">소나무 환산</div>
              <div class=\"viz-value highlight-green\">{_format_number(tree_equivalent_count, decimals=0)} <span class=\"viz-unit\">그루</span></div>
              <div class=\"viz-sub\">30년생 소나무 기준</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class=\"card\">
          <div class=\"card-title\">Before / After 비교</div>

          <div class=\"compare-grid\">
            <div class=\"compare-card before\">
              <div class=\"compare-badge\">Before</div>
              <div class=\"compare-sub\">콘크리트 옥상</div>
              <div class=\"compare-icon\">🏢</div>
              <div class=\"compare-stats\">
                <div class=\"stat-row\">
                  <span class=\"stat-label\">옥상 면적</span>
                  <span class=\"stat-value\">{roof_area_display} ㎡</span>
                </div>
                <div class=\"stat-row\">
                  <span class=\"stat-label\">녹지 면적</span>
                  <span class=\"stat-value\">0 ㎡</span>
                </div>
                <div class=\"stat-row\">
                  <span class=\"stat-label\">CO₂ 흡수량</span>
                  <span class=\"stat-value\">0 kg/년</span>
                </div>
                <div class=\"stat-row\">
                  <span class=\"stat-label\">표면 온도</span>
                  <span class=\"stat-value hot\">{_format_number(baseline_surface_temp_c, decimals=1)}℃</span>
                </div>
              </div>
            </div>

            <div class=\"compare-arrow\">→</div>

            <div class=\"compare-card after\">
              <div class=\"compare-badge after\">After</div>
              <div class=\"compare-sub\">{_escape(greening_label)} {coverage_percent}</div>
              <div class=\"compare-icon\">🌿</div>
              <div class=\"compare-stats\">
                <div class=\"stat-row\">
                  <span class=\"stat-label\">옥상 면적</span>
                  <span class=\"stat-value\">{roof_area_display} ㎡</span>
                </div>
                <div class=\"stat-row\">
                  <span class=\"stat-label\">녹지 면적</span>
                  <span class=\"stat-value green\">{green_area_display} ㎡ ▲</span>
                </div>
                <div class=\"stat-row\">
                  <span class=\"stat-label\">CO₂ 흡수량</span>
                  <span class=\"stat-value green\">{co2_display} kg/년 ▲</span>
                </div>
                <div class=\"stat-row\">
                  <span class=\"stat-label\">표면 온도</span>
                  <span class=\"stat-value cool\">{_format_number(after_surface_temp_c, decimals=1)}℃ ({temp_reduction_display}℃) ▼</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    callout_items = []
    if co2_coeff_text:
        callout_items.append(f"<li><strong>현황:</strong> CO₂ 흡수량은 {_escape(greening_label)} {co2_coeff_text}kg/㎡/년 계수 기준입니다.</li>")
    callout_items.append("<li><strong>제안:</strong> 온도 저감은 녹화 비율에 비례합니다.</li>")
    if pine_factor_text:
        callout_items.append(f"<li><strong>활용:</strong> 소나무 환산은 30년생 기준 {pine_factor_text}kg/년입니다.</li>")
    else:
        callout_items.append("<li><strong>활용:</strong> 이 시뮬레이션 결과를 정책 제안 근거 자료로 사용하세요.</li>")
    callout_html = "".join(callout_items)

    st.markdown(
        f"""
        <div class=\"callout\">
          <div class=\"callout-icon\">🏛️</div>
          <div class=\"callout-content\">
            <div class=\"callout-title\">G-SEED 인증 활용 안내</div>
            <ul class=\"callout-list\">
              {callout_html}
            </ul>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="cta-row">', unsafe_allow_html=True)
    prev_col, next_col = st.columns([1, 1], gap="small")
    with prev_col:
        prev_clicked = st.button("← 이전: 녹화 계획", key="result_prev")
    with next_col:
        next_clicked = st.button("리포트 다운로드 →", key="result_next")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<aside class="side">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class=\"card\">
          <div class=\"card-title\">결과 해석</div>
          <ul class=\"bullets\">
            <li>CO₂ 흡수량은 { _escape(greening_label)} {_format_number(co2_coefficient, decimals=1) if co2_coefficient is not None else '가중치'} 기준입니다.</li>
            <li>온도 저감은 녹화 비율에 비례합니다.</li>
            <li>소나무 환산은 30년생 기준 {_format_number(pine_factor_kg_per_year, decimals=1) if pine_factor_kg_per_year is not None else '계수'}kg/년입니다.</li>
          </ul>
          <div class=\"divider\"></div>
          <a class=\"link\" href=\"#\">데이터 근거 보기 →</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</aside>', unsafe_allow_html=True)

    st.markdown('</section>', unsafe_allow_html=True)

    st.markdown('</div></div></main>', unsafe_allow_html=True)

    return {
        "prev_clicked": prev_clicked,
        "next_clicked": next_clicked,
    }