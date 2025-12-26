import streamlit as st

def render_service_intro_ui():
    """
    서비스 소개 페이지 UI를 렌더링합니다.
    Design Source: design/okssang_imong/service-intro-v2.html
    """
    st.html("""
    <style>
    /* Scoped CSS for Service Intro Page */
    /* Reusing some global styles but ensuring specificity */
    
    .service-hero {
        background: linear-gradient(135deg, #0b3b5b 0%, #1a5a7a 100%);
        color: #fff;
        padding: 80px 0;
        text-align: center;
        margin-top: -40px; /* Adjust for Streamlit padding */
    }
    .hero-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 999px;
        background: rgba(72,187,120,.2);
        border: 1px solid rgba(72,187,120,.4);
        font-size: 12px;
        font-weight: 700;
        color: #68d391;
        margin-bottom: 18px;
    }
    .hero-title {
        font-size: 40px;
        font-weight: 900;
        margin-bottom: 16px;
        line-height: 1.3;
    }
    .hero-title .highlight { color: #48bb78; }
    .hero-desc {
        font-size: 16px;
        opacity: .9;
        margin-bottom: 28px;
        line-height: 1.7;
    }
    .hero-cta {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #48bb78;
        color: #fff !important;
        padding: 14px 28px;
        border-radius: 999px;
        font-size: 15px;
        font-weight: 700;
        text-decoration: none;
        transition: all .2s;
    }
    .hero-cta:hover {
        background: #2f855a;
        transform: translateY(-2px);
        color: #fff !important;
    }

    /* Section Common */
    .section { padding: 60px 0; }
    .section-gray { background: #f9fafb; }
    .section-problem { background: #fff5f5; }
    .section-solution { background: linear-gradient(135deg, #f0fff4, #e6fffa); }
    .section-dark { background: #0b3b5b; color: #fff; }

    .section-title {
        text-align: center;
        font-size: 26px;
        font-weight: 900;
        margin-bottom: 10px;
        color: #1a202c;
    }
    .section-dark .section-title { color: #fff; }
    
    .section-desc {
        text-align: center;
        font-size: 14px;
        color: #718096;
        margin-bottom: 36px;
        line-height: 1.7;
    }
    .section-dark .section-desc { color: rgba(255,255,255,.7); }

    /* Problem Section */
    .problem-intro {
        text-align: center;
        max-width: 700px;
        margin: 0 auto 40px;
    }
    .problem-quote {
        font-size: 20px;
        font-weight: 900;
        color: #c53030;
        margin-bottom: 12px;
    }
    .problem-explain {
        font-size: 14px;
        color: #4a5568;
        line-height: 1.7;
    }
    .problem-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 24px;
    }
    .problem-card {
        background: #fff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 40px rgba(15,23,42,.08);
        color: #1a202c;
    }
    .problem-card.current { border: 2px solid #e2e8f0; }
    .problem-card.issues { border: 2px solid #fc8181; }
    
    .problem-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        background: #edf2f7;
        font-size: 10px;
        font-weight: 900;
        color: #4a5568;
        margin-bottom: 12px;
    }
    .problem-badge.warning { background: #fed7d7; color: #c53030; }
    
    .problem-title {
        font-size: 16px;
        font-weight: 900;
        margin-bottom: 14px;
        color: #1a202c;
    }
    .problem-formula {
        background: #f7fafc;
        border-radius: 10px;
        padding: 14px;
        font-size: 13px;
        font-weight: 700;
        color: #4a5568;
        text-align: center;
        margin-bottom: 14px;
    }
    .problem-list {
        padding-left: 18px;
        font-size: 13px;
        color: #4a5568;
        margin-bottom: 14px;
    }
    .problem-list li { margin-bottom: 6px; }
    
    .problem-issue {
        display: flex;
        align-items: flex-start;
        gap: 8px;
        background: #fff5f5;
        border-radius: 10px;
        padding: 12px;
        font-size: 12px;
        color: #c53030;
    }
    .issue-list { display: flex; flex-direction: column; gap: 10px; }
    .issue-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 14px;
        background: #f7fafc;
        border-radius: 10px;
    }
    .issue-label { font-size: 13px; font-weight: 700; color: #2d3748; }
    .issue-status {
        font-size: 10px;
        font-weight: 900;
        color: #c53030;
        background: #fed7d7;
        padding: 4px 10px;
        border-radius: 999px;
    }

    /* Solution Section */
    .solution-card {
        background: #fff;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 16px 48px rgba(15,23,42,.1);
        max-width: 900px;
        margin: 0 auto;
        color: #1a202c;
    }
    .solution-icon { font-size: 48px; margin-bottom: 16px; }
    .solution-title {
        font-size: 24px;
        font-weight: 900;
        margin-bottom: 14px;
        color: #0b3b5b;
    }
    .solution-desc {
        font-size: 15px;
        color: #4a5568;
        line-height: 1.8;
        margin-bottom: 28px;
    }
    .solution-table {
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        overflow: hidden;
        margin-bottom: 28px;
        text-align: left;
    }
    .sol-row {
        display: grid;
        grid-template-columns: 1fr 1fr 1.3fr;
        padding: 14px 18px;
        font-size: 13px;
        border-bottom: 1px solid #e2e8f0;
        color: #2d3748;
    }
    .sol-row:last-child { border-bottom: none; }
    .sol-row.header {
        background: #f0fff4;
        font-weight: 900;
        color: #2f855a;
    }
    
    .btn-primary {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #48bb78, #2f855a);
        color: #fff !important;
        padding: 16px 32px;
        border-radius: 999px;
        font-size: 15px;
        font-weight: 700;
        border: none;
        cursor: pointer;
        transition: all .2s;
        text-decoration: none;
    }
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(72,187,120,.3);
        color: #fff !important;
    }

    /* Features Section */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 24px;
    }
    .feature-card {
        background: #fff;
        border-radius: 16px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(15,23,42,.08);
        color: #1a202c;
    }
    .feature-icon {
        width: 56px; height: 56px;
        border-radius: 16px;
        background: linear-gradient(135deg, #f0fff4, #e6fffa);
        display: flex; align-items: center; justify-content: center;
        font-size: 26px;
        margin: 0 auto 16px;
    }
    .feature-title {
        font-size: 15px;
        font-weight: 900;
        margin-bottom: 8px;
        color: #0b3b5b;
    }
    .feature-desc {
        font-size: 12px;
        color: #718096;
        line-height: 1.6;
    }

    /* Process Section */
    .process-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
    }
    .process-step {
        text-align: center;
        position: relative;
    }
    .process-step:not(:last-child)::after {
        content: "→";
        position: absolute;
        right: -14px;
        top: 30px;
        font-size: 20px;
        color: #cbd5e0;
    }
    .step-number {
        width: 48px; height: 48px;
        border-radius: 999px;
        background: linear-gradient(135deg, #48bb78, #2f855a);
        color: #fff;
        font-size: 18px;
        font-weight: 900;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 12px;
    }
    .step-title {
        font-size: 14px;
        font-weight: 900;
        margin-bottom: 6px;
        color: #fff;
    }
    .step-desc {
        font-size: 11px;
        color: rgba(255,255,255,.7);
    }

    /* CTA Section */
    .cta-section {
        background: linear-gradient(135deg, #48bb78, #2f855a);
        padding: 60px 0;
        text-align: center;
        color: #fff;
    }
    .cta-title {
        font-size: 28px;
        font-weight: 900;
        margin-bottom: 12px;
    }
    .cta-desc {
        font-size: 15px;
        opacity: .9;
        margin-bottom: 24px;
    }
    .btn-cta {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #fff;
        color: #2f855a !important;
        padding: 16px 32px;
        border-radius: 999px;
        font-size: 15px;
        font-weight: 700;
        border: none;
        cursor: pointer;
        transition: all .2s;
        text-decoration: none;
    }
    .btn-cta:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0,0,0,.2);
        color: #2f855a !important;
    }

    /* Responsive */
    @media (max-width: 900px){
        .problem-grid { grid-template-columns: 1fr; }
        .feature-grid { grid-template-columns: 1fr; }
        .process-grid { grid-template-columns: repeat(2, 1fr); }
        .process-step:not(:last-child)::after { display: none; }
    }
    @media (max-width: 640px){
        .hero-title { font-size: 28px; }
        .process-grid { grid-template-columns: 1fr; }
    }
    </style>

    <!-- 히어로 -->
    <section class="service-hero">
      <div class="container-1320">
        <div class="hero-badge">🌿 Rooftop Greening Effect Simulator</div>
        <h1 class="hero-title">
          옥상녹화의 효과를<br />
          <span class="highlight">숫자로 증명</span>합니다
        </h1>
        <p class="hero-desc">
          주소만 입력하면 CO₂ 흡수량, 온도 저감 효과를 자동 계산<br />
          G-SEED 정책 개선을 위한 정량적 근거 자료를 제공합니다
        </p>
        <a class="hero-cta" href="/" target="_top">시뮬레이션 시작하기 →</a>
      </div>
    </section>

    <!-- 문제 제기 -->
    <section class="section section-problem">
      <div class="container-1320">
        <div class="problem-intro">
          <div class="problem-quote">"녹색 건물인데, 녹화 효과는 측정하지 않는다?"</div>
          <p class="problem-explain">
            현재 G-SEED 인증은 옥상녹화의 실제 환경 효과(탄소 흡수량, 온도 저감)를<br />
            정량적으로 측정하지 않고, 단순히 '토심(흙 깊이)'만으로 평가합니다.
          </p>
        </div>

        <div class="problem-grid">
          <!-- 현행 방식 -->
          <div class="problem-card current">
            <div class="problem-badge">현행 G-SEED 평가 방식</div>
            <h3 class="problem-title">토심(흙 깊이) 기반 가중치 평가</h3>
            <div class="problem-formula">
              <span>생태면적 = 녹화면적 × 가중치</span>
            </div>
            <ul class="problem-list">
              <li>토심 20cm 이상: 가중치 <strong>0.6</strong></li>
              <li>토심 20cm 미만: 가중치 <strong>0.5</strong></li>
            </ul>
            <div class="problem-issue">
              <span class="issue-icon">⚠️</span>
              <span>"흙만 깔아놓고 식물이 죽어도 점수를 받는" 구조적 한계</span>
            </div>
          </div>

          <!-- 문제점 -->
          <div class="problem-card issues">
            <div class="problem-badge warning">정량 평가 부재 항목</div>
            <h3 class="problem-title">측정되지 않는 실제 환경 효과</h3>
            <div class="issue-list">
              <div class="issue-item">
                <span class="issue-label">🌿 탄소 흡수량 (kg CO₂/년)</span>
                <span class="issue-status">측정 안 함</span>
              </div>
              <div class="issue-item">
                <span class="issue-label">🌡️ 온도 저감 효과 (°C)</span>
                <span class="issue-status">측정 안 함</span>
              </div>
              <div class="issue-item">
                <span class="issue-label">☀️ 냉방 에너지 절감</span>
                <span class="issue-status">측정 안 함</span>
              </div>
              <div class="issue-item">
                <span class="issue-label">🏙️ 도시 열섬 완화 효과</span>
                <span class="issue-status">측정 안 함</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 솔루션 -->
    <section class="section section-solution">
      <div class="container-1320">
        <div class="solution-card">
          <div class="solution-icon">💡</div>
          <h2 class="solution-title">옥상이몽이 제안하는 솔루션</h2>
          <p class="solution-desc">
            G-SEED 생태환경 분야에 <strong>탄소 흡수량</strong>과 <strong>냉각 효과</strong>를<br />
            정량적으로 평가하는 세부 항목을 추가한다면,<br />
            정책 의도에 맞는 실질적인 환경 효과를 극대화할 수 있습니다.
          </p>
          
          <div class="solution-table">
            <div class="sol-row header">
              <span>분석 데이터</span>
              <span>G-SEED 연계 항목</span>
              <span>기대 효과</span>
            </div>
            <div class="sol-row">
              <span>🌲 수종별 탄소 흡수량</span>
              <span>생태환경 (생태면적률)</span>
              <span>탄소 저감 효율 높은 수종 선정 근거</span>
            </div>
            <div class="sol-row">
              <span>🌡️ 옥상 냉각 효과</span>
              <span>에너지 (EPI 지표)</span>
              <span>냉방 에너지 부하 감소 입증</span>
            </div>
            <div class="sol-row">
              <span>📊 종합 분석</span>
              <span>혁신적 설계 (열섬 저감)</span>
              <span>도시 미기후 개선 기여도 증명</span>
            </div>
          </div>

          <a class="btn-primary" href="/" target="_top">옥상이몽 시뮬레이션 체험하기 →</a>
        </div>
      </div>
    </section>

    <!-- 주요 기능 -->
    <section class="section section-gray">
      <div class="container-1320">
        <h2 class="section-title">주요 기능</h2>
        <p class="section-desc">옥상이몽은 정책 담당자와 건물주 모두에게 유용한 데이터를 제공합니다.</p>

        <div class="feature-grid">
          <div class="feature-card">
            <div class="feature-icon">📍</div>
            <h3 class="feature-title">주소 기반 자동 계산</h3>
            <p class="feature-desc">건물 주소만 입력하면 VWorld API를 통해 옥상 면적을 자동으로 추출합니다.</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🌿</div>
            <h3 class="feature-title">녹화 유형별 효과 분석</h3>
            <p class="feature-desc">잔디, 세덤, 관목 등 녹화 유형에 따른 CO₂ 흡수량과 온도 저감 효과를 비교합니다.</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3 class="feature-title">Before/After 시각화</h3>
            <p class="feature-desc">녹화 전후 환경 효과를 직관적으로 비교할 수 있는 시각화 리포트를 제공합니다.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 시뮬레이션 프로세스 -->
    <section class="section section-dark">
      <div class="container-1320">
        <h2 class="section-title">시뮬레이션 프로세스</h2>
        <p class="section-desc">4단계 과정을 통해 옥상녹화 효과를 확인하세요.</p>

        <div class="process-grid">
          <div class="process-step">
            <div class="step-number">1</div>
            <div class="step-title">주소 입력</div>
            <div class="step-desc">건물 주소를 검색하여 입력</div>
          </div>
          <div class="process-step">
            <div class="step-number">2</div>
            <div class="step-title">조건 확인</div>
            <div class="step-desc">옥상 면적 및 가용 면적 확인</div>
          </div>
          <div class="process-step">
            <div class="step-number">3</div>
            <div class="step-title">녹화 계획</div>
            <div class="step-desc">녹화 유형 및 비율 설정</div>
          </div>
          <div class="process-step">
            <div class="step-number">4</div>
            <div class="step-title">결과 확인</div>
            <div class="step-desc">CO₂, 온도 저감 효과 리포트</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="cta-section">
      <div class="container-1320">
        <h2 class="cta-title">지금 바로 옥상녹화 효과를 확인해보세요</h2>
        <p class="cta-desc">주소만 입력하면 10초 안에 결과를 확인할 수 있습니다.</p>
        <a class="btn-cta" href="/" target="_top">🌿 시뮬레이션 시작하기</a>
      </div>
    </section>
    """)
