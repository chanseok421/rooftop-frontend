import streamlit as st

def render_contact_ui():
    """
    문의하기 페이지 UI를 렌더링합니다.
    Design Source: design/okssang_imong/contact.html
    """
    st.html("""
    <style>
    /* Scoped CSS for Contact Page */
    
    .contact-section {
        padding: 60px 0 80px;
    }
    .section-badge {
        font-size: 12px;
        font-weight: 700;
        color: #48bb78;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .section-title {
        font-size: 32px;
        font-weight: 900;
        color: #1a202c;
        margin-bottom: 10px;
    }
    .section-desc {
        font-size: 14px;
        color: #718096;
        margin-bottom: 40px;
    }

    /* Content Grid */
    .contact-grid {
        display: grid;
        grid-template-columns: 1.5fr 1fr;
        gap: 32px;
    }

    /* Cards */
    .contact-card, .info-card {
        background: #fff;
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 10px 40px rgba(15,23,42,.08);
        color: #1a202c;
    }
    .card-title {
        font-size: 16px;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 24px;
    }

    /* Form Elements */
    .form-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-bottom: 16px;
    }
    .form-group { margin-bottom: 16px; }
    .form-label {
        display: block;
        font-size: 13px;
        font-weight: 600;
        color: #4a5568;
        margin-bottom: 8px;
    }
    .form-input, .form-select, .form-textarea {
        width: 100%;
        padding: 12px 14px;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        font-size: 14px;
        font-family: inherit;
        color: #1a202c;
        background: #fff;
        transition: border-color .2s, box-shadow .2s;
        box-sizing: border-box; /* Important for width: 100% */
    }
    .form-input:focus, .form-select:focus, .form-textarea:focus {
        outline: none;
        border-color: #48bb78;
        box-shadow: 0 0 0 3px rgba(72,187,120,.15);
    }
    .form-input::placeholder, .form-textarea::placeholder { color: #a0aec0; }
    .form-textarea {
        min-height: 120px;
        resize: vertical;
    }
    .form-note {
        font-size: 12px;
        color: #718096;
        margin-top: 16px;
        margin-bottom: 16px;
    }
    .btn-submit {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 12px 24px;
        background: linear-gradient(135deg, #48bb78, #2f855a);
        color: #fff !important;
        font-size: 14px;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: transform .2s, box-shadow .2s;
        text-decoration: none;
    }
    .btn-submit:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(72,187,120,.3);
        color: #fff !important;
    }

    /* Info List */
    .info-list {
        list-style: none;
        margin-bottom: 24px;
        padding-left: 0;
    }
    .info-list li {
        position: relative;
        padding-left: 20px;
        font-size: 14px;
        color: #4a5568;
        margin-bottom: 12px;
        line-height: 1.6;
    }
    .info-list li::before {
        content: "•";
        position: absolute;
        left: 0;
        color: #48bb78;
        font-weight: 700;
    }
    .info-divider {
        height: 1px;
        background: #e2e8f0;
        margin: 24px 0;
    }
    .info-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 13px;
        margin-bottom: 10px;
    }
    .info-label { color: #718096; }
    .info-value {
        color: #1a202c;
        font-weight: 600;
    }

    /* Responsive */
    @media (max-width: 768px){
        .contact-grid { grid-template-columns: 1fr; }
        .form-row { grid-template-columns: 1fr; }
        .section-title { font-size: 24px; }
    }
    </style>

    <div class="container-1320 contact-section">
      <div class="section-badge">CONTACT</div>
      <h1 class="section-title">문의하기</h1>
      <p class="section-desc">서비스, 시뮬레이션, 협업에 대해 무엇이든 문의해주세요.</p>

      <div class="contact-grid">
        <!-- 폼 카드 -->
        <div class="contact-card">
          <div class="card-title">문의 내용 입력</div>
          <form onsubmit="return false;"> <!-- Streamlit form handling is separate, UI only here -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">이름</label>
                <input type="text" class="form-input" placeholder="홍길동">
              </div>
              <div class="form-group">
                <label class="form-label">이메일</label>
                <input type="email" class="form-input" placeholder="email@example.com">
              </div>
            </div>
            <div class="form-group">
              <label class="form-label">문의 유형</label>
              <select class="form-select">
                <option>서비스 문의</option>
                <option>시뮬레이션 결과 문의</option>
                <option>협업 제안</option>
                <option>G-SEED 인증 자문</option>
                <option>기타</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">문의 내용</label>
              <textarea class="form-textarea" placeholder="문의하실 내용을 자세히 작성해주세요."></textarea>
            </div>
            <p class="form-note">접수된 문의는 영업일 기준 1~2일 이내에 답변드립니다.</p>
            <div style="text-align:right;">
              <button class="btn-submit">문의 보내기</button>
            </div>
          </form>
        </div>

        <!-- 안내 카드 -->
        <div class="info-card">
          <div class="card-title">안내 사항</div>
          <ul class="info-list">
            <li>시뮬레이션 결과 문의 시 주소를 함께 남겨주세요.</li>
            <li>공공기관·기업 협업 문의 환영합니다.</li>
            <li>G-SEED 인증 관련 자문 가능합니다.</li>
          </ul>
          <div class="info-divider"></div>
          <div class="info-row">
            <span class="info-label">이메일</span>
            <span class="info-value">contact@oksangimong.kr</span>
          </div>
          <div class="info-row">
            <span class="info-label">운영시간</span>
            <span class="info-value">평일 10:00 – 18:00</span>
          </div>
        </div>
      </div>
    </div>
    """)
