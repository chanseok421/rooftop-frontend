import streamlit as st

def render_data_reference_ui():
    """
    데이터 근거 페이지 UI를 렌더링합니다.
    Design Source: design/okssang_imong/data-reference.html
    """
    st.html("""
    <style>
    /* Scoped CSS for Data Reference Page */
    
    .data-hero {
        background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%);
        color: #fff;
        padding: 60px 0;
        text-align: center;
        margin-top: -40px; /* Streamlit padding correction */
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
        font-size: 32px;
        font-weight: 900;
        margin-bottom: 14px;
        color: #fff;
    }
    .hero-desc {
        font-size: 15px;
        opacity: .85;
        line-height: 1.7;
        color: #fff;
    }

    /* Section Common */
    .section { padding: 50px 0; }
    .section-white { background: #fff; }
    .section-gray { background: #f9fafb; }

    .section-title {
        text-align: center;
        font-size: 22px;
        font-weight: 900;
        margin-bottom: 8px;
        color: #1a202c;
    }
    .section-desc {
        text-align: center;
        font-size: 13px;
        color: #718096;
        margin-bottom: 32px;
    }

    /* Data Cards */
    .data-card {
        background: #fff;
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 10px 40px rgba(15,23,42,.08);
        margin-bottom: 24px;
        color: #1a202c;
    }
    .data-card-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 17px;
        font-weight: 900;
        margin-bottom: 18px;
        color: #0b3b5b;
    }
    .data-card-icon {
        width: 36px; height: 36px;
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-size: 18px;
    }
    .icon-co2 { background: linear-gradient(135deg, #c6f6d5, #9ae6b4); }
    .icon-temp { background: linear-gradient(135deg, #bee3f8, #90cdf4); }
    .icon-pine { background: linear-gradient(135deg, #fefcbf, #faf089); }

    /* Tables */
    .data-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
    }
    .data-table th {
        background: #f7fafc;
        padding: 12px 14px;
        text-align: left;
        font-weight: 700;
        color: #4a5568;
        border-bottom: 2px solid #e2e8f0;
    }
    .data-table td {
        padding: 12px 14px;
        border-bottom: 1px solid #e2e8f0;
        color: #2d3748;
    }
    .data-table tr:last-child td { border-bottom: none; }
    .data-table .highlight {
        font-weight: 700;
        color: #2f855a;
    }

    /* Source Tags */
    .source-tag {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 999px;
        background: #edf2f7;
        font-size: 10px;
        font-weight: 700;
        color: #4a5568;
    }
    .source-tag.korea { background: #fed7e2; color: #97266d; }
    .source-tag.japan { background: #feebc8; color: #c05621; }
    .source-tag.usa { background: #bee3f8; color: #2b6cb0; }
    .source-tag.gov { background: #c6f6d5; color: #276749; }

    /* Source Note */
    .source-note {
        background: #f0fff4;
        border-left: 4px solid #48bb78;
        padding: 14px 18px;
        margin-top: 16px;
        border-radius: 0 10px 10px 0;
        font-size: 12px;
        color: #276749;
    }
    .source-note strong { font-weight: 700; }

    /* References */
    .reference-list {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    .reference-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 16px;
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(15,23,42,.06);
    }
    .ref-number {
        width: 28px; height: 28px;
        border-radius: 999px;
        background: linear-gradient(135deg, #48bb78, #2f855a);
        color: #fff;
        font-size: 12px;
        font-weight: 900;
        display: flex; align-items: center; justify-content: center;
        flex-shrink: 0;
    }
    .ref-content { flex: 1; }
    .ref-title {
        font-size: 13px;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 4px;
    }
    .ref-meta {
        font-size: 11px;
        color: #718096;
    }
    .ref-link {
        color: #3182ce;
        text-decoration: underline;
    }
    
    /* Responsive */
    @media (max-width: 768px){
        .hero-title { font-size: 24px; }
        .data-table { font-size: 12px; }
        .data-table th, .data-table td { padding: 10px 8px; }
    }
    </style>

    <!-- 히어로 -->
    <section class="data-hero">
      <div class="container-1320">
        <div class="hero-badge">📊 Research-Based Data</div>
        <h1 class="hero-title">학술 연구 기반의 정량 데이터</h1>
        <p class="hero-desc">
          옥상이몽의 모든 계산은 국내외 학술 논문과 공공 데이터에 근거합니다.<br />
          신뢰할 수 있는 출처를 투명하게 공개합니다.
        </p>
      </div>
    </section>

    <!-- 핵심 계수 -->
    <section class="section section-gray">
      <div class="container-1320">
        <h2 class="section-title">핵심 계수 데이터</h2>
        <p class="section-desc">옥상이몽 시뮬레이션에 적용되는 주요 계수입니다.</p>

        <!-- CO₂ 흡수 계수 -->
        <div class="data-card">
          <div class="data-card-title">
            <div class="data-card-icon icon-co2">🌿</div>
            CO₂ 흡수 계수 (kg/m²/년)
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>녹화 유형</th>
                <th>적용 계수</th>
                <th>연구 범위</th>
                <th>출처</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>잔디</strong></td>
                <td class="highlight">1.79 ~ 2.5</td>
                <td>버뮤다그래스, 톨페스큐, 금잔디</td>
                <td><span class="source-tag japan">일본</span> Kuronuma et al. (2018)</td>
              </tr>
              <tr>
                <td><strong>세덤</strong></td>
                <td class="highlight">0.14 ~ 0.70</td>
                <td>Sedum acre, S. aizoon 등</td>
                <td><span class="source-tag usa">미국</span> Getter et al. (2009)</td>
              </tr>
              <tr>
                <td><strong>관목</strong></td>
                <td class="highlight">2.07 ~ 2.27</td>
                <td>화살나무, 회양목 등</td>
                <td><span class="source-tag korea">한국</span> 김학구 외 (2022)</td>
              </tr>
            </tbody>
          </table>
          <div class="source-note">
            <strong>💡 보수적 적용:</strong> 본 서비스는 연구 범위 내 <strong>보수적 수치</strong>를 적용하여 정책적 신뢰성을 확보했습니다.
          </div>
        </div>

        <!-- 온도 저감 효과 -->
        <div class="data-card">
          <div class="data-card-title">
            <div class="data-card-icon icon-temp">🌡️</div>
            온도 저감 효과 (°C)
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>녹화 유형</th>
                <th>최대 저감</th>
                <th>측정 조건</th>
                <th>출처</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>세덤</strong></td>
                <td class="highlight">4.7°C</td>
                <td>8월, 12시 기준</td>
                <td><span class="source-tag korea">한국</span> 옥상녹화 유형별 기온저감 연구</td>
              </tr>
              <tr>
                <td><strong>잔디</strong></td>
                <td class="highlight">3.2°C</td>
                <td>8월, 12시 기준</td>
                <td><span class="source-tag korea">한국</span> 옥상녹화 유형별 기온저감 연구</td>
              </tr>
              <tr>
                <td><strong>관목</strong></td>
                <td class="highlight">2.5°C</td>
                <td>8월, 12시 기준</td>
                <td><span class="source-tag korea">한국</span> 옥상녹화 유형별 기온저감 연구</td>
              </tr>
            </tbody>
          </table>
          <div class="source-note">
            <strong>📐 실험 조건:</strong> 1m×1m×1m 건물 모형에서 4개월간(7~10월) 실측한 데이터입니다.
          </div>
        </div>

        <!-- 기준값 -->
        <div class="data-card">
          <div class="data-card-title">
            <div class="data-card-icon icon-pine">🌲</div>
            기준값
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>항목</th>
                <th>값</th>
                <th>설명</th>
                <th>출처</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>소나무 연간 CO₂ 흡수량</strong></td>
                <td class="highlight">9.1 kg/년</td>
                <td>30년생 소나무 기준</td>
                <td><span class="source-tag gov">정부</span> 산림청 국립산림과학원</td>
              </tr>
              <tr>
                <td><strong>옥상 가용율</strong></td>
                <td class="highlight">65%</td>
                <td>건축물 옥상 면적 대비 녹화 가능 면적</td>
                <td><span class="source-tag gov">정부</span> 서울시 옥상녹화 가이드라인</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- 참고 문헌 -->
    <section class="section section-white">
      <div class="container-1320">
        <h2 class="section-title">참고 문헌</h2>
        <p class="section-desc">본 서비스에 인용된 학술 논문 및 공공 데이터 출처입니다.</p>

        <div class="reference-list">
          <div class="reference-item">
            <div class="ref-number">1</div>
            <div class="ref-content">
              <div class="ref-title">CO₂ Payoff of Extensive Green Roofs with Different Vegetation Species</div>
              <div class="ref-meta">Kuronuma, T., Watanabe, H. et al. (2018) · Sustainability, MDPI · <a class="ref-link" href="https://doi.org/10.3390/su10072256" target="_blank">DOI: 10.3390/su10072256</a></div>
            </div>
          </div>
          <div class="reference-item">
            <div class="ref-number">2</div>
            <div class="ref-content">
              <div class="ref-title">Carbon Sequestration Potential of Extensive Green Roofs</div>
              <div class="ref-meta">Getter, K. L. et al. (2009) · Environmental Science & Technology, Michigan State University</div>
            </div>
          </div>
          <div class="reference-item">
            <div class="ref-number">3</div>
            <div class="ref-content">
              <div class="ref-title">정원수목의 탄소흡수량 측정 및 국가 탄소흡수원 자료 구축</div>
              <div class="ref-meta">김학구 외 (2022) · 한국수목원정원관리원</div>
            </div>
          </div>
          <div class="reference-item">
            <div class="ref-number">4</div>
            <div class="ref-content">
              <div class="ref-title">산림생장정보 - 수종별 탄소흡수량</div>
              <div class="ref-meta">산림청 국립산림과학원 · <a class="ref-link" href="https://nifos.forest.go.kr" target="_blank">nifos.forest.go.kr</a></div>
            </div>
          </div>
          <div class="reference-item">
            <div class="ref-number">5</div>
            <div class="ref-content">
              <div class="ref-title">서울시 옥상녹화 가이드라인</div>
              <div class="ref-meta">서울특별시 · 푸른도시국</div>
            </div>
          </div>
        </div>
      </div>
    </section>
    """)
