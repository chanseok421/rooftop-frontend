import streamlit as st
import os

def render_gseed_page():
    """
    G-SEED 안내 페이지를 렌더링합니다.
    design/okssang_imong/g-seed-info-v2.html의 내용을 st.html()로 이식했습니다.
    """
    
    # ==========================================
    # 1. CSS Definition
    # ==========================================
    css_content = """
    /* 기본 초기화 */
    .gseed-container * { box-sizing: border-box; }
    
    .container {
      max-width: 1120px;
      margin: 0 auto;
      padding: 0 20px;
    }
    
    /* 히어로 */
    .gseed-hero {
      background: linear-gradient(135deg, #0b3b5b 0%, #1a5a7a 100%);
      color: #fff;
      padding: 80px 0;
      text-align: center;
      /* margin-top: -40px !important; Streamlit 기본 패딩 보정 제거 */
    }
    .hero-badge {
      display: inline-block;
      padding: 6px 14px;
      border-radius: 999px;
      background: rgba(72, 187, 120, .2);
      border: 1px solid rgba(72, 187, 120, .4);
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
      margin-bottom: 12px;
      line-height: 1.7;
    }
    .hero-sub {
      font-size: 14px;
      opacity: .75;
    }
    
    /* 섹션 공통 */
    .section { padding: 60px 0; }
    .section-gray { background: #f9fafb; }
    
    .section-title {
      text-align: center;
      font-size: 26px;
      font-weight: 900;
      margin-bottom: 10px;
      color: #1a202c;
    }
    .section-desc {
      text-align: center;
      font-size: 14px;
      color: #718096;
      margin-bottom: 36px;
      line-height: 1.7;
    }
    
    /* 핵심 효과 그리드 */
    .effect-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
    }
    .effect-card {
      background: #fff;
      border-radius: 16px;
      padding: 24px 20px;
      text-align: center;
      box-shadow: 0 10px 40px rgba(15, 23, 42, .08);
    }
    .effect-icon {
      width: 52px; height: 52px;
      border-radius: 14px;
      background: linear-gradient(135deg, #f0fff4, #e6fffa);
      display: flex; align-items: center; justify-content: center;
      font-size: 24px;
      margin: 0 auto 14px;
    }
    .effect-title {
      font-size: 14px;
      font-weight: 900;
      margin-bottom: 6px;
      color: #0b3b5b;
    }
    .effect-desc {
      font-size: 12px;
      color: #718096;
      line-height: 1.5;
    }
    
    /* 인증 등급 & 세제 혜택 */
    .benefit-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 24px;
    }
    .benefit-card {
      background: #fff;
      border-radius: 16px;
      padding: 28px;
      box-shadow: 0 10px 40px rgba(15, 23, 42, .08);
    }
    .benefit-header {
      display: flex; align-items: center; gap: 10px;
      margin-bottom: 16px;
    }
    .benefit-icon { font-size: 24px; }
    .benefit-label {
      font-size: 11px;
      color: #718096;
      font-weight: 700;
      background: #f7fafc;
      padding: 4px 10px;
      border-radius: 999px;
    }
    .benefit-title {
      font-size: 18px;
      font-weight: 900;
      margin-bottom: 6px;
      color: #0b3b5b;
    }
    .benefit-sub {
      font-size: 12px;
      color: #a0aec0;
      margin-bottom: 18px;
    }
    
    /* 테이블 */
    .benefit-table {
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      overflow: hidden;
      margin-bottom: 14px;
    }
    .table-row {
      display: grid;
      grid-template-columns: 1.3fr 1fr .7fr;
      padding: 12px 14px;
      font-size: 12px;
      border-bottom: 1px solid #e2e8f0;
      color: #4a5568;
    }
    .table-row:last-child { border-bottom: none; }
    .table-row.header {
      background: #f7fafc;
      font-weight: 900;
      color: #4a5568;
    }
    .table-row.highlight { background: #f0fff4; }
    .green { color: #2f855a; font-weight: 900; }
    
    .benefit-note {
      font-size: 11px;
      color: #a0aec0;
      display: flex; align-items: flex-start; gap: 6px;
    }
    .benefit-note .icon { color: #ed8936; }
    
    /* 하이라이트 박스 */
    .benefit-highlight {
      background: linear-gradient(135deg, #f0fff4, #e6fffa);
      border-radius: 14px;
      padding: 24px;
      text-align: center;
      margin-bottom: 18px;
    }
    .highlight-value {
      font-size: 32px;
      font-weight: 900;
      color: #2f855a;
    }
    .highlight-label {
      font-size: 12px;
      color: #718096;
      margin-top: 4px;
    }
    .benefit-list {
      padding-left: 18px;
      font-size: 12px;
      color: #4a5568;
      line-height: 1.8;
    }
    .benefit-list li { margin-bottom: 6px; }
    
    /* 평가 분야 */
    .eval-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 18px;
    }
    .eval-card {
      background: #fff;
      border-radius: 14px;
      padding: 20px;
      box-shadow: 0 10px 40px rgba(15, 23, 42, .08);
    }
    .eval-number {
      width: 32px; height: 32px;
      border-radius: 999px;
      background: linear-gradient(135deg, #48bb78, #2f855a);
      color: #fff;
      font-size: 14px;
      font-weight: 900;
      display: flex; align-items: center; justify-content: center;
      margin-bottom: 12px;
    }
    .eval-title {
      font-size: 13px;
      font-weight: 900;
      margin-bottom: 6px;
      color: #0b3b5b;
    }
    .eval-desc {
      font-size: 11px;
      color: #718096;
      line-height: 1.5;
    }
    
    /* 인증 등급 테이블 */
    .grade-table {
      background: #fff;
      border-radius: 16px;
      padding: 28px;
      box-shadow: 0 10px 40px rgba(15, 23, 42, .08);
      max-width: 700px;
      margin: 0 auto;
    }
    .grade-table-title {
      font-size: 16px;
      font-weight: 900;
      margin-bottom: 18px;
      text-align: center;
      color: #0b3b5b;
    }
    .grade-row {
      display: grid;
      grid-template-columns: 1.2fr 1fr 1fr;
      padding: 14px 16px;
      font-size: 13px;
      border-bottom: 1px solid #e2e8f0;
      color: #4a5568;
    }
    .grade-row:last-child { border-bottom: none; }
    .grade-row.header {
      background: #0b3b5b;
      color: #fff;
      font-weight: 700;
      border-radius: 10px 10px 0 0;
    }
    .grade-row.green1 { background: #f0fff4; }
    .grade-badge {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 999px;
      font-size: 10px;
      font-weight: 900;
    }
    .badge-green1 { background: #c6f6d5; color: #22543d; }
    .badge-green2 { background: #bee3f8; color: #2a4365; }
    .badge-green3 { background: #feebc8; color: #744210; }
    .badge-green4 { background: #e2e8f0; color: #4a5568; }
    
    /* 법적 근거 */
    .legal-ref {
      background: #f7fafc;
      border-radius: 12px;
      padding: 16px 20px;
      margin-top: 24px;
      font-size: 11px;
      color: #718096;
      line-height: 1.6;
    }
    .legal-ref strong { color: #4a5568; }
    
    /* 푸터 */
    .footer {
      border-top: 1px solid #e2e8f0;
      padding: 22px 0 30px;
      font-size: 12px;
      color: #a0aec0;
      background: #fff;
    }
    .footer-inner {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
    }
    .footer-links { display: flex; gap: 16px; }
    .footer-links a { text-decoration: none; color: inherit; }
    
    /* 반응형 */
    @media (max-width: 900px) {
      .effect-grid { grid-template-columns: repeat(2, 1fr); }
      .benefit-grid { grid-template-columns: 1fr; }
      .eval-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 640px) {
      .effect-grid { grid-template-columns: 1fr; }
      .eval-grid { grid-template-columns: 1fr; }
      .hero-title { font-size: 28px; }
    }
    """
    
    # ==========================================
    # 2. HTML Content (Ported from g-seed-info-v2.html)
    # ==========================================
    html_content = """
    <div class="gseed-container">
        <!-- 히어로 -->
        <section class="gseed-hero">
          <div class="container">
            <div class="hero-badge">🏢 녹색건축 인증제도</div>
            <h1 class="hero-title">
              <span class="highlight">G-SEED</span>란?
            </h1>
            <p class="hero-desc">
              Green Standard for Energy and Environmental Design<br />
              설계·시공·유지·관리 전 과정에서 에너지 절약 및 환경오염 저감에 기여한<br />
              <strong>친환경 건축물에 인증을 부여하는 국가 제도</strong>입니다.
            </p>
            <p class="hero-sub">
              공공건축물(연면적 3,000㎡ 이상)은 인증 취득이 의무화되어 있으며,<br />
              인증 건축물에는 취득세·재산세 감면 등 세제 인센티브가 제공됩니다.
            </p>
          </div>
        </section>

        <!-- 핵심 효과 -->
        <section class="section">
          <div class="container">
            <h2 class="section-title">녹색건축 인증의 핵심 효과</h2>
            <p class="section-desc">G-SEED 인증 건축물은 환경적·경제적 가치를 동시에 제공합니다.</p>

            <div class="effect-grid">
              <div class="effect-card">
                <div class="effect-icon">⚡</div>
                <div class="effect-title">에너지 절감</div>
                <div class="effect-desc">연간 에너지 사용량<br />20~30% 절감</div>
              </div>
              <div class="effect-card">
                <div class="effect-icon">💧</div>
                <div class="effect-title">수자원 절약</div>
                <div class="effect-desc">빗물 재활용 및<br />절수 설비 적용</div>
              </div>
              <div class="effect-card">
                <div class="effect-icon">🌬️</div>
                <div class="effect-title">환경오염 감소</div>
                <div class="effect-desc">CO₂ 및 미세먼지<br />배출 저감</div>
              </div>
              <div class="effect-card">
                <div class="effect-icon">🏢</div>
                <div class="effect-title">자산 가치 상승</div>
                <div class="effect-desc">건물 가치 및<br />임대 경쟁력 향상</div>
              </div>
            </div>
          </div>
        </section>

        <!-- 인증 등급 & 세제 혜택 -->
        <section class="section section-gray">
          <div class="container">
            <h2 class="section-title">인증 등급 & 세제 혜택</h2>
            <p class="section-desc">G-SEED 인증 등급에 따라 취득세·재산세 감면 혜택이 제공됩니다.</p>

            <div class="benefit-grid">
              <!-- 취득세 감면 -->
              <div class="benefit-card">
                <div class="benefit-header">
                  <span class="benefit-icon">🏷️</span>
                  <span class="benefit-label">신축 건축물</span>
                </div>
                <h3 class="benefit-title">취득세 감면</h3>
                <p class="benefit-sub">2026년 12월 31일까지</p>
                
                <div class="benefit-table">
                  <div class="table-row header">
                    <span>인증 등급</span>
                    <span>에너지효율등급</span>
                    <span>감면율</span>
                  </div>
                  <div class="table-row highlight">
                    <span>최우수 (그린1등급)</span>
                    <span>1+등급 이상</span>
                    <span class="green">10%</span>
                  </div>
                  <div class="table-row">
                    <span>우수 (그린2등급)</span>
                    <span>1+등급 이상</span>
                    <span class="green">5%</span>
                  </div>
                </div>
                <div class="benefit-note">
                  <span class="icon">⚠️</span>
                  <span>에너지효율등급 1+등급 이상 동시 충족 필요</span>
                </div>
              </div>

              <!-- 재산세 감면 -->
              <div class="benefit-card">
                <div class="benefit-header">
                  <span class="benefit-icon">🏠</span>
                  <span class="benefit-label">보유 건축물</span>
                </div>
                <h3 class="benefit-title">재산세 감면</h3>
                <p class="benefit-sub">인증일로부터 5년간</p>
                
                <div class="benefit-highlight">
                  <div class="highlight-value">3% ~ 15%</div>
                  <div class="highlight-label">감면율</div>
                </div>
                
                <ul class="benefit-list">
                  <li>녹색건축 인증 또는 에너지효율등급 인증 건물</li>
                  <li>인증일(또는 준공일) 기준 5년간 적용</li>
                  <li>두 인증 날짜가 다를 경우 먼저 받은 인증일 기준</li>
                </ul>
              </div>
            </div>

            <div class="legal-ref">
              <strong>📋 법적 근거:</strong> 「지방세특례제한법」 제47조의2, 같은 법 시행령 제24조
            </div>
          </div>
        </section>

        <!-- 인증 등급 체계 -->
        <section class="section">
          <div class="container">
            <h2 class="section-title">인증 등급 체계</h2>
            <p class="section-desc">G-SEED는 100점 만점 기준 4개 등급으로 분류됩니다.</p>

            <div class="grade-table">
              <div class="grade-table-title">📊 등급별 점수 기준 (100점 만점)</div>
              <div class="grade-row header">
                <span>등급</span>
                <span>점수 기준</span>
                <span>비고</span>
              </div>
              <div class="grade-row green1">
                <span><span class="grade-badge badge-green1">최우수</span> 그린1등급</span>
                <span>80점 이상</span>
                <span>취득세 10% 감면</span>
              </div>
              <div class="grade-row">
                <span><span class="grade-badge badge-green2">우수</span> 그린2등급</span>
                <span>70점 이상</span>
                <span>취득세 5% 감면</span>
              </div>
              <div class="grade-row">
                <span><span class="grade-badge badge-green3">우량</span> 그린3등급</span>
                <span>60점 이상</span>
                <span>-</span>
              </div>
              <div class="grade-row">
                <span><span class="grade-badge badge-green4">일반</span> 그린4등급</span>
                <span>50점 이상</span>
                <span>-</span>
              </div>
            </div>
          </div>
        </section>

        <!-- 평가 분야 -->
        <section class="section section-gray">
          <div class="container">
            <h2 class="section-title">7개 평가 분야</h2>
            <p class="section-desc">G-SEED는 7개 분야에서 건축물의 친환경 성능을 종합 평가합니다.</p>

            <div class="eval-grid">
              <div class="eval-card">
                <div class="eval-number">1</div>
                <h4 class="eval-title">토지이용 및 교통</h4>
                <p class="eval-desc">대지 보존성, 대중교통 접근성, 자전거 보관시설 등</p>
              </div>
              <div class="eval-card">
                <div class="eval-number">2</div>
                <h4 class="eval-title">에너지 및 환경오염</h4>
                <p class="eval-desc">에너지 성능, 온실가스 저감, 오존층 보호 등</p>
              </div>
              <div class="eval-card">
                <div class="eval-number">3</div>
                <h4 class="eval-title">재료 및 자원</h4>
                <p class="eval-desc">친환경 자재, 재활용 비율, 유해물질 저감 등</p>
              </div>
              <div class="eval-card">
                <div class="eval-number">4</div>
                <h4 class="eval-title">물순환 관리</h4>
                <p class="eval-desc">빗물 관리, 절수 설비, 우수 저류 시설 등</p>
              </div>
              <div class="eval-card">
                <div class="eval-number">5</div>
                <h4 class="eval-title">유지관리</h4>
                <p class="eval-desc">체계적 관리 시스템, 운영 매뉴얼 등</p>
              </div>
              <div class="eval-card">
                <div class="eval-number">6</div>
                <h4 class="eval-title">생태환경</h4>
                <p class="eval-desc">생태면적률, 녹지 공간, 비오톱 조성 등</p>
              </div>
              <div class="eval-card">
                <div class="eval-number">7</div>
                <h4 class="eval-title">실내환경</h4>
                <p class="eval-desc">실내 공기질, 쾌적성, 소음 저감 등</p>
              </div>
              <div class="eval-card">
                <div class="eval-number">+</div>
                <h4 class="eval-title">혁신적 설계 (가산)</h4>
                <p class="eval-desc">도시 열섬 저감, 혁신 기술 적용 등</p>
              </div>
            </div>
          </div>
        </section>

        <!-- 푸터 -->
        <footer class="footer">
          <div class="container footer-inner">
            <div>© 2025 옥상이몽 · Rooftop Greening Effect Simulator</div>
            <div class="footer-links">
              <a href="#">개인정보처리방침</a>
              <a href="#">문의하기</a>
            </div>
          </div>
        </footer>
    </div>
    """
    
    # Render with st.html
    st.html(f"<style>{css_content}</style>{html_content}")
