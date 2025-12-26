import streamlit as st


def _format_number(value: float | None) -> str:
    if value is None:
        return "—"
    return f"{value:,.0f}"


def _format_ratio(value: float | None) -> str:
    if value is None:
        return "—"
    return f"{value:.0f}"


def render_area_confirm_ui(
    *,
    address_title: str,
    address_caption: str,
    floor_area: float | None,
    suggested_area: float | None,
    availability_ratio: float | None,
    default_area: float,
) -> dict:
    st.markdown(
        """
        <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        .app-header { position: sticky; top: 0; z-index: 50; }

        .container-1320 {
          width: 100%;
          max-width: 1320px;
          margin: 0 auto;
          padding: 0 20px;
        }
        .content-1120 {
          width: 100%;
          max-width: 1120px;
          margin: 0 auto;
        }

        .btn {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          border-radius: 999px;
          padding: 10px 18px;
          font-size: 13px;
          font-weight: 700;
          border: 1px solid transparent;
          cursor: pointer;
          white-space: nowrap;
        }
        .btn-primary { background: #48bb78; color: #fff; }
        .btn-primary:hover { background: #2f855a; }
        .btn-secondary {
          background: #edf2f7;
          color: #1a202c;
          border-color: #e2e8f0;
        }
        .btn-secondary:hover { background: #e2e8f0; }
        .btn-ghost {
          background: transparent;
          color: #1a202c;
          border-color: #e2e8f0;
        }
        .btn-ghost:hover { background: #fff; }

        .section-header { padding: 6px 0 10px; }
        .eyebrow {
          font-size: 12px;
          color: #2f855a;
          font-weight: 800;
          letter-spacing: 0.08em;
        }
        .h2 { font-size: 28px; font-weight: 900; margin-top: 6px; }
        .subtitle { font-size: 14px; color: #718096; margin-top: 6px; }

        .stepper {
          width: 100%;
          background: #fff;
          border-radius: 16px;
          box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
          padding: 14px 16px;
          display: flex;
          align-items: center;
          gap: 10px;
          margin: 16px 0 18px;
        }
        .step { display: flex; align-items: center; gap: 8px; min-width: 0; }
        .step .dot { width: 10px; height: 10px; border-radius: 999px; background: #cbd5e0; }
        .step .label { font-size: 12px; color: #4a5568; font-weight: 900; white-space: nowrap; }
        .step.active .dot { background: #48bb78; }
        .step.active .label { color: #1a202c; }
        .line { flex: 1; height: 1px; background: #e2e8f0; }

        .grid {
          display: grid;
          grid-template-columns: 1fr 360px;
          gap: 20px;
          align-items: start;
        }

        .card {
          background: #fff;
          border-radius: 20px;
          padding: 22px 22px;
          box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
        }

        .card-header { display: flex; align-items: center; gap: 10px; margin-bottom: 14px; }
        .pin {
          width: 34px; height: 34px; border-radius: 999px;
          background: #f0fff4;
          display: flex; align-items: center; justify-content: center;
        }
        .header-text { display: flex; flex-direction: column; gap: 2px; }
        .card-title { font-size: 16px; font-weight: 900; }
        .card-caption { font-size: 12px; color: #718096; }

        .chips { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 12px; }
        .chip {
          border: 1px solid #e2e8f0;
          border-radius: 14px;
          padding: 12px 12px;
          background: #f9fbff;
        }
        .chip-label { font-size: 11px; color: #718096; font-weight: 900; margin-bottom: 6px; }
        .chip-value { font-size: 16px; font-weight: 900; }
        .unit { font-size: 12px; color: #718096; font-weight: 900; margin-left: 2px; }

        .callout {
          display: flex;
          align-items: flex-start;
          gap: 10px;
          background: #e6fffa;
          border-radius: 14px;
          padding: 12px 12px;
          margin: 10px 0 14px;
        }
        .callout-icon {
          width: 18px; height: 18px; border-radius: 999px;
          background: #0b7285; color: #fff;
          display: flex; align-items: center; justify-content: center;
          font-size: 12px; font-weight: 900;
          flex: 0 0 auto;
        }
        .callout-text { font-size: 12px; color: #2d3748; font-weight: 800; }

        .edit { display: flex; flex-direction: column; gap: 8px; margin-top: 2px; }
        .edit-title { font-size: 12px; color: #2d3748; font-weight: 900; }
        .edit-row { display: flex; gap: 10px; align-items: flex-end; }
        .input { display: flex; flex-direction: column; gap: 6px; flex: 1; }
        .input-label { font-size: 11px; color: #718096; font-weight: 900; }
        .input-box {
          width: 100%;
          height: 40px;
          border-radius: 12px;
          border: 1px solid #e2e8f0;
          background: #fff;
          padding: 0 12px;
          font-size: 13px;
          font-weight: 800;
          outline: none;
        }
        .input-box:focus { border-color: #48bb78; box-shadow: 0 0 0 3px rgba(72, 187, 120, 0.18); }
        .edit-help { font-size: 11px; color: #a0aec0; font-weight: 800; margin-top: 2px; }

        .cta-row { display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-top: 14px; }

        .bullets { margin-top: 10px; padding-left: 16px; color: #4a5568; font-size: 12px; font-weight: 800; }
        .bullets li { margin-bottom: 6px; }
        .divider { height: 1px; background: #e2e8f0; margin: 14px 0; }
        .link { font-size: 12px; color: #0b3b5b; font-weight: 900; }

        .footer {
          border-top: 1px solid #e2e8f0;
          padding: 22px 0 30px;
          font-size: 12px;
          color: #a0aec0;
        }
        .footer-inner {
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 14px;
          flex-wrap: wrap;
        }
        .footer-links { display: flex; gap: 16px; }

        .edit-row .stTextInput input {
          width: 100%;
          height: 40px;
          border-radius: 12px;
          border: 1px solid #e2e8f0;
          background: #fff;
          padding: 0 12px;
          font-size: 13px;
          font-weight: 800;
        }
        .edit-row .stButton > button {
          width: 100%;
          border-radius: 999px;
          padding: 10px 18px;
          font-size: 13px;
          font-weight: 700;
          background: #edf2f7;
          color: #1a202c;
          border: 1px solid #e2e8f0;
        }
        .edit-row .stButton > button:hover { background: #e2e8f0; }

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
        }
        @media (max-width: 640px) {
          .chips { grid-template-columns: 1fr; }
          .edit-row { flex-direction: column; align-items: stretch; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # st.markdown('<main class="page">', unsafe_allow_html=True)
    # st.markdown('<div class="container-1320">', unsafe_allow_html=True)
    # st.markdown('<div class="content-1120">', unsafe_allow_html=True)

    st.markdown(
        """
        <section class="section-header">
          <div class="eyebrow">SIMULATION · STEP 1</div>
          <h1 class="h2">옥상 조건 확인</h1>
          <p class="subtitle">
            주소를 기반으로 시뮬레이션에 사용할 면적 정보를 확인합니다.
          </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <section class="stepper" aria-label="simulation steps">
          <div class="step active">
            <div class="dot"></div>
            <div class="label">조건확인</div>
          </div>
          <div class="line"></div>
          <div class="step">
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

    # Calculated ratio: 487px vs 360px -> ~1.35 : 1
    # Using specific weights close to that
    left_col, right_col = st.columns([1.35, 1], gap="large")

    with left_col:
        st.markdown(
            f"""
            <section class="card">
              <div class="card-header">
                <div class="pin">📍</div>
                <div class="header-text">
                  <div class="card-title">{address_title}</div>
                  <div class="card-caption">{address_caption}</div>
                </div>
              </div>

              <div class="chips">
                <div class="chip">
                  <div class="chip-label">바닥면적</div>
                  <div class="chip-value">{_format_number(floor_area)} <span class="unit">㎡</span></div>
                </div>
                <div class="chip">
                  <div class="chip-label">옥상 가용면적</div>
                  <div class="chip-value">{_format_number(suggested_area)} <span class="unit">㎡</span></div>
                </div>
                <div class="chip">
                  <div class="chip-label">가용 비율</div>
                  <div class="chip-value">{_format_ratio(availability_ratio)} <span class="unit">%</span></div>
                </div>
              </div>

              <div class="callout">
                <div class="callout-icon">i</div>
                <div class="callout-text">
                  이 면적은 다음 단계에서 CO₂·온도·경제성 계산의 기준값으로 사용됩니다.
                </div>
              </div>

              <div class="edit">
                <div class="edit-title">면적이 다르면 직접 수정할 수 있습니다.</div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="edit-row">', unsafe_allow_html=True)
        input_col, button_col = st.columns([3, 1], gap="small")
        with input_col:
            st.markdown(
                """
                <div class="input">
                  <div class="input-label">옥상 가용면적(㎡)</div>
                """,
                unsafe_allow_html=True,
            )
            roof_area_value = st.text_input(
                "",
                value=f"{default_area:.0f}" if default_area else "",
                placeholder=f"{suggested_area:.0f}" if suggested_area else "",
                key="roof_area_input",
                label_visibility="collapsed",
            )
            st.markdown("</div>", unsafe_allow_html=True)
        with button_col:
            apply_clicked = st.button("값 적용", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
              <div class="edit-help">
                가용면적은 옥상 구조·설비에 따라 달라질 수 있습니다.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="cta-row">', unsafe_allow_html=True)
        prev_col, next_col = st.columns([1, 1], gap="small")
        with prev_col:
            prev_clicked = st.button("이전(주소 수정)", type="secondary")
        with next_col:
            next_clicked = st.button("다음: 녹화 계획 →", type="primary")
        st.markdown("</div></section>", unsafe_allow_html=True)

    with right_col:
        st.markdown(
            """
            <section class="card">
              <div class="card-title">왜 면적 확인이 필요한가요?</div>
              <ul class="bullets">
                <li>면적은 CO₂ 흡수량 계산의 기준입니다.</li>
                <li>면적은 온도 저감 효과의 크기를 결정합니다.</li>
                <li>리포트(PDF)에는 이 값이 근거로 포함됩니다.</li>
              </ul>

              <div class="divider"></div>

              <a class="link" href="#">데이터 근거 보기 →</a>
            </section>
            """,
            unsafe_allow_html=True,
        )

    # st.markdown("</div></div></main>", unsafe_allow_html=True)

    return {
        "roof_area_value": roof_area_value,
        "apply_clicked": apply_clicked,
        "prev_clicked": prev_clicked,
        "next_clicked": next_clicked,
    }