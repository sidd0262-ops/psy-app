import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

st.set_page_config(page_title="Psy-Interpreter Auto", layout="wide", page_icon="🛡️")

with st.sidebar:
    st.header("🛡️ 자동 우회 모드")
    raw_key = st.text_input("Gemini API Key 입력", type="password")
    user_api_key = raw_key.strip() if raw_key else None
    
    uploaded_file = st.file_uploader("논문 파일 (PDF)", type=['pdf'])
    mode = st.radio("분석 스타일", ["🎓 교수님 브리핑", "📖 교과서 해설", "✍️ 논문 결과 작성"])

st.title("🛡️ 심리 통역사 (오류 방지 모드)")

if not user_api_key:
    st.warning("👈 왼쪽 사이드바에 '새 프로젝트' 키(끝자리 2WB0)를 입력해주세요.")
elif uploaded_file:
    genai.configure(api_key=user_api_key)
    
    # [핵심] 순서대로 시도하는 '무적' 로직
    model_candidates = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    active_model = None
    
    with st.spinner('사용 가능한 AI 모델을 찾는 중...'):
        for model_name in model_candidates:
            try:
                # 모델 연결 테스트
                test_model = genai.GenerativeModel(model_name)
                # 가벼운 인사로 생존 확인
                test_model.generate_content("test")
                active_model = test_model
                st.success(f"✅ 연결 성공! 현재 모델: {model_name}")
                break
            except:
                continue
    
    if active_model:
        with st.spinner('논문 분석 중...'):
            try:
                reader = PdfReader(uploaded_file)
                text = ""
                for i in range(min(10, len(reader.pages))):
                    text += reader.pages[i].extract_text()
                
                prompt = f"당신은 심리학 전문가입니다. 다음 논문을 [{mode}] 스타일로 분석해줘:\n\n{text}"
                response = active_model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"분석 중 오류: {e}")
    else:
        st.error("🚫 모든 모델 연결 실패. API 키가 '새 프로젝트'의 것인지(2WB0) 다시 확인해주세요.")
