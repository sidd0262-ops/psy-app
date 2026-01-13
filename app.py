import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

st.set_page_config(page_title="Psy-Interpreter Pro", layout="wide")

with st.sidebar:
    st.header("⚙️ 설정")
    raw_key = st.text_input("Gemini API Key", type="password")
    user_api_key = raw_key.strip() if raw_key else None
    uploaded_file = st.file_uploader("파일 업로드", type=['pdf'])
    mode = st.radio("모드", ["🎓 교수님 브리핑용", "📖 교과서 해설용", "✍️ 논문 결과 작성용"])

st.title("🧠 Psy-Interpreter")

if not user_api_key:
    st.warning("👈 왼쪽 사이드바에 API Key를 입력해주세요.")
elif uploaded_file:
    genai.configure(api_key=user_api_key)
    
    # 404 에러를 피하기 위해 가장 검증된 'gemini-pro'를 사용합니다.
    model = genai.GenerativeModel('gemini-pro') 
    
    with st.spinner('분석 중입니다...'):
        try:
            reader = PdfReader(uploaded_file)
            text = "".join([p.extract_text() for p in reader.pages[:5]])
            
            # 분석 요청
            response = model.generate_content(f"심리학 전문가로서 다음 내용을 [{mode}] 스타일로 분석해줘:\n\n{text}")
            
            st.success("✅ 분석 완료!")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"오류 발생: {e}")
            st.info("이 에러는 구글 API 키의 권한 문제입니다. 새로운 구글 계정으로 키를 발급받는 것이 빠를 수 있습니다.")
