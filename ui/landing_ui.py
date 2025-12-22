import streamlit as st
import streamlit.components.v1 as components
import os

# 공통 헤더 컴포넌트 import
from components.common.header import render_header

def load_css_content(file_name):
    """CSS 파일 내용을 문자열로 반환합니다."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    css_path = os.path.join(project_root, "design", "okssang_imong", file_name)
    
    with open(css_path, "r", encoding="utf-8") as f:
        return f.read()

def render_landing_page():
    """랜딩 페이지를 렌더링합니다."""
    
    css_content = load_css_content("index.css")
    
    # ========================================
    # 1. 공통 헤더 (컴포넌트 호출)
    # ========================================
    render_header()
    
    # ========================================
    # 2. Hero 섹션
    # ========================================
    hero_html = f"""
    <style>
    {css_content}
    body {{ margin: 0; padding: 0; }}
    </style>
    <section class="hero">
      <div class="hero-inner">
        <div class="hero-badge">
          <span>서울시 탄소중립 · 옥상녹화</span>
          <span>·</span>
          <span>Biosolar 최적 설계</span>
        </div>
        <h1 class="hero-title">
          주소 하나로 옥상녹화의<br>
          환경·경제 효과를 시뮬레이션합니다.
        </h1>
        <p class="hero-subtitle">
          CO₂ 흡수량, 온도 저감, G-SEED 점수, 절감 금액까지.<br>
          데이터 기반 결과를 서울시 제안서와 건물주용 리포트로 동시에 제공합니다.
        </p>
      </div>
    </section>
    """
    components.html(hero_html, height=320, scrolling=False)
    
    # ========================================
    # 3. 검색바 (Streamlit 위젯 - 인터랙션 필요)
    # ========================================
    _, col_search, _ = st.columns([1, 2.5, 1])
    
    with col_search:
        c1, c2 = st.columns([2.5, 1.5])
        with c1:
            address = st.text_input(
                "Address", 
                placeholder="예) 서울시 중구 세종대로 110 (서울시청) 입력...", 
                label_visibility="collapsed"
            )
        with c2:
            if st.button("시뮬레이션 시작", type="primary", use_container_width=True):
                if address:
                    st.session_state["address"] = address
                st.switch_page("pages/1_📍_주소입력.py")
        
        st.markdown(
            "<p style='text-align:center; font-size:12px; color:#718096; margin-top:8px;'>"
            "실제 서비스에서는 공공데이터와 분석 모델을 활용해 건물별 옥상녹화·태양광 통합 효과를 계산합니다."
            "</p>",
            unsafe_allow_html=True
        )
    
    # ========================================
    # 4. 하단 영역: Features + Project + Use Cases + Footer (통합!)
    # ========================================
    bottom_html = f"""
    <style>
    {css_content}
    body {{ margin: 0; padding: 0; background: #f4f6f9; }}
    </style>
    
    <!-- Features Section -->
    <section class="features" style="margin-top: 0; padding-top: 20px;">
      <div class="container-1320">
        <div class="content-1120">
          <div class="feature-grid">
            <div class="feature-item">
              <div class="feature-icon">🌿</div>
              <div class="feature-title">CO₂ 흡수량 계산</div>
              <div class="feature-desc">녹화 유형·면적·수종에 따라<br>연간 탄소저감량을 정량화합니다.</div>
            </div>
            <div class="feature-item">
              <div class="feature-icon">🌡️</div>
              <div class="feature-title">온도 저감 효과</div>
              <div class="feature-desc">옥상 표면온도 감소와<br>실내 냉방부하 감소를 추정합니다.</div>
            </div>
            <div class="feature-item">
              <div class="feature-icon">📊</div>
              <div class="feature-title">G-SEED · 인증 지원</div>
              <div class="feature-desc">데이터 결과를 기반으로<br>G-SEED 항목 추가 근거를 제공합니다.</div>
            </div>
            <div class="feature-item">
              <div class="feature-icon">💰</div>
              <div class="feature-title">경제성·절감 금액</div>
              <div class="feature-desc">에너지 절감, 세제 혜택 등<br>건물주 관점의 경제성을 보여줍니다.</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Project Structure Section -->
    <section class="section">
      <div class="container-1320">
        <div class="content-1120">
          <div class="section-header">
            <div class="section-kicker">PROJECT STRUCTURE</div>
            <h2 class="section-title">데이터 분석에서 제안서와 서비스까지, 한 번에.</h2>
            <p class="section-subtitle">옥상이몽은 동일한 분석 결과를 서울시 정책 제안서와 건물주 서비스에 각각 최적화된 형태로 제공합니다.</p>
          </div>

          <div class="flow-layout">
            <div class="card">
              <div class="card-header">
                <span class="card-tag">데이터 분석</span>
                <h3 class="card-title">옥상녹화 · 태양광 통합 효과 모델링</h3>
              </div>
              <div class="card-body">
                <p>공공데이터, 기상 데이터, 선행연구를 바탕으로 <strong>CO₂ 흡수량·온도저감 계수</strong>를 도출하고, 옥상 단위로 시뮬레이션합니다.</p>
                <div class="pill-list">
                  <span class="pill">녹화 유형별 탄소흡수 계수</span>
                  <span class="pill">옥상 표면 온도 저감 계수</span>
                  <span class="pill">건물용도·층수별 부하 반영</span>
                  <span class="pill">Biosolar 설치 시나리오 비교</span>
                </div>
              </div>
            </div>

            <div class="card">
              <div class="card-header">
                <span class="card-tag">시뮬레이터 서비스</span>
                <h3 class="card-title">주소 기반 Simulator</h3>
              </div>
              <div class="card-body">
                <p>건물주는 주소만 입력하면, 동일한 모델을 기반으로 <strong>"내 건물에 적용했을 때의 효과"</strong>를 즉시 확인할 수 있습니다.</p>
                <div class="pill-list">
                  <span class="pill">주소·건물 정보 자동 불러오기</span>
                  <span class="pill">녹화 면적·수종 시나리오 선택</span>
                  <span class="pill">CO₂·온도·금액 결과 리포트</span>
                  <span class="pill">G-SEED 준비 체크리스트</span>
                </div>
              </div>
            </div>
          </div>

          <div class="two-cards">
            <div class="card">
              <div class="badge">📄 서울시 제안서</div>
              <div class="scenario-title">"이 데이터가 근거입니다."</div>
              <p class="card-body">시뮬레이션 결과를 모아 서울시에 제출할 <strong>정량적 근거 자료</strong>로 구성합니다.</p>
            </div>
            <div class="card">
              <div class="badge">🖥️ 건물주용 서비스</div>
              <div class="scenario-title">"이걸로 계산하세요."</div>
              <p class="card-body">건물주가 직접 사용하는 <strong>웹 기반 시뮬레이터</strong>로, 옥상녹화·태양광 통합 설치의 효과를 수치와 그래프로 제공합니다.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Use Cases Section -->
    <section class="section" style="padding-top: 0;">
      <div class="container-1320">
        <div class="content-1120">
          <div class="section-header">
            <div class="section-kicker">USE CASES</div>
            <h2 class="section-title">서울시 · 건물주가 이렇게 활용합니다.</h2>
          </div>

          <div class="scenario-grid">
            <div class="card">
              <div class="badge">🏛️ 서울시 · 정책 담당자</div>
              <div class="scenario-title">G-SEED 고도화 · 옥상녹화 확산 정책</div>
              <ul class="scenario-steps">
                <li>1. 시범지역·건축물 대상 데이터 수집 및 시뮬레이션</li>
                <li>2. CO₂·온도저감 효과를 지표화하여 G-SEED 항목 설계</li>
                <li>3. 옥상녹화·Biosolar 설치 인센티브 설계에 활용</li>
              </ul>
            </div>

            <div class="card">
              <div class="badge">🏢 건물주 · 관리자</div>
              <div class="scenario-title">"의무 설치 태양광을, 투자 자산으로."</div>
              <ul class="scenario-steps">
                <li>1. 주소 입력 후 옥상 조건 확인</li>
                <li>2. 녹화 유형·면적·태양광 조합 시나리오 선택</li>
                <li>3. 절감 금액과 인증 가능성 확인 후 의사결정</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
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
    components.html(bottom_html, height=1150, scrolling=False)
