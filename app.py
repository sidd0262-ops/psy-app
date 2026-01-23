import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- 페이지 설정 ---
st.set_page_config(page_title="Psy-Interpreter Pro", layout="wide", page_icon="🧠")

# --- 사이드바 ---
with st.sidebar:
    st.header("⚙️ 프로 모드 설정")
    # 키 입력 시 공백 자동 제거
    raw_key = st.text_input("Gemini API Key 입력", type="password")
    user_api_key = raw_key.strip() if raw_key else None
    
    uploaded_file = st.file_uploader("논문 파일 (PDF)", type=['pdf'])
    mode = st.radio("분석 스타일", ["🎓 교수님 브리핑용", "📖 교과서 해설용", "✍️ 논문 결과 작성용"])

st.title("🧠 Psy-Interpreter (Pro Mode)")

if not user_api_key:
    st.warning("👈 왼쪽 사이드바에 '새 프로젝트'에서 발급받은 키를 입력해주세요.")
elif uploaded_file:
    # 프로 모드 활성화
    genai.configure(api_key=user_api_key)
    
    # [핵심] 가장 안정적인 표준 모델 'gemini-pro' 강제 사용
    model = genai.GenerativeModel('gemini-pro') 
    
    with st.spinner('프로 모드로 박재연 소장님 논문을 정밀 분석 중입니다...'):
        try:
            reader = PdfReader(uploaded_file)
            text = ""
            # 핵심 내용이 담긴 앞쪽 10페이지 추출
            for i in range(min(10, len(reader.pages))):
                text += reader.pages[i].extract_text()
            
            # 분석 요청
            prompt = f"당신은 심리학 및 통계 전문가입니다. 다음 논문을 [{mode}] 스타일로 상세히 분석해줘:\n\n{text}"
            response = model.generate_content(prompt)
            
            st.success("✅ 분석 완료!")
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
            st.info("Tip: 404 에러 시, Google AI Studio에서 'Create API key in new project'로 새 키를 발급받으세요.")
# 업데이트 확인용 강제 저장
