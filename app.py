import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

st.set_page_config(page_title="Psy-Interpreter Pro", layout="wide")

with st.sidebar:
    st.header("⚙️ 설정")
    user_api_key = st.text_input("Gemini API Key", type="password")
    uploaded_file = st.file_uploader("논문 업로드", type=['pdf', 'png', 'jpg'])
    mode = st.radio("모드", ["🎓 교수님 브리핑용", "📖 교과서 해설용", "✍️ 논문 결과 작성용"])

st.title("🧠 Psy-Interpreter")

if user_api_key and uploaded_file:
    genai.configure(api_key=user_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # 속도가 가장 빠른 모델
    
    with st.spinner('핵심 내용을 빠르게 분석 중...'):
        try:
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                # 속도를 위해 핵심 결과가 있는 앞쪽 5페이지만 집중 분석
                text = "".join([p.extract_text() for p in reader.pages[:5]])
                prompt = f"심리학 전문가로서 다음 논문의 핵심을 [{mode}] 스타일로 요약해줘:\n\n{text}"
                response = model.generate_content(prompt)
            else:
                img = uploaded_file.getvalue()
                response = model.generate_content([f"이 이미지를 [{mode}]로 해석해줘", {"mime_type": uploaded_file.type, "data": img}])
            
            st.success("✅ 분석 완료!")
            st.write(response.text)
        except Exception as e:
            st.error(f"오류 발생: {e}")
