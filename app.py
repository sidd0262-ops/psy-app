import streamlit as st
import google.generativeai as genai
import pandas as pd
from PyPDF2 import PdfReader

# --- 앱 설정 ---
st.set_page_config(page_title="Psy-Interpreter Pro", layout="wide", page_icon="🧠")

# --- 사이드바 ---
with st.sidebar:
    st.header("⚙️ 설정 및 업로드")
    user_api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    uploaded_file = st.file_uploader("파일 업로드 (PDF, 이미지)", type=['pdf', 'png', 'jpg', 'jpeg'])
    mode = st.radio("모드", ["🎓 교수님 브리핑용", "📖 교과서 해설용", "✍️ 논문 결과 작성용"])

# --- 메인 화면 ---
st.title("🧠 Psy-Interpreter")

if not user_api_key:
    st.warning("👈 왼쪽 사이드바에 API Key를 입력해주세요.")
elif uploaded_file:
    genai.configure(api_key=user_api_key)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    with st.spinner('분석 중...'):
        try:
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                text = "".join([p.extract_text() for p in reader.pages[:10]])
                response = model.generate_content(f"다음 논문을 {mode} 스타일로 분석해줘:\n{text}")
            else:
                img = uploaded_file.getvalue()
                response = model.generate_content([f"이 통계 이미지를 {mode} 스타일로 해석해줘.", {"mime_type": uploaded_file.type, "data": img}])
            st.success("✅ 분석 완료!")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"에러 발생: {e}")
