import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# [1] 최신 엔진에 맞춘 페이지 설정
st.set_page_config(page_title="Psy-Interpreter Flash", layout="wide", page_icon="⚡")

with st.sidebar:
    st.header("⚡ 최신 Flash 모드")
    raw_key = st.text_input("Gemini API Key 입력", type="password")
    user_api_key = raw_key.strip() if raw_key else None
    
    uploaded_file = st.file_uploader("논문 파일 업로드 (PDF)", type=['pdf'])
    mode = st.radio("분석 스타일", ["🎓 교수님 브리핑", "📖 교과서 해설", "✍️ 논문 결과 작성"])

st.title("⚡ 심리 통역사 (최신 Flash 모드)")

if not user_api_key:
    st.warning("👈 왼쪽 사이드바에 API 키를 입력해주세요.")
elif uploaded_file:
    # [2] 최신 키 설정
    genai.configure(api_key=user_api_key)
    
    # [3] 핵심: 에러 안 나는 최신 모델 'gemini-1.5-flash' 사용
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    with st.spinner('최신 AI가 논문을 분석 중입니다...'):
        try:
            reader = PdfReader(uploaded_file)
            text = ""
            # 텍스트 추출
            for i in range(min(10, len(reader.pages))):
                text += reader.pages[i].extract_text()
            
            # 분석 요청
            prompt = f"당신은 심리학 전문가입니다. 다음 논문을 [{mode}] 스타일로 분석해줘:\n\n{text}"
            response = model.generate_content(prompt)
            
            st.success("✅ 분석 성공! (Flash 모델 가동)")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
