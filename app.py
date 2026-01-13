import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

st.set_page_config(page_title="Psy-Interpreter Pro", layout="wide")

with st.sidebar:
    st.header("⚙️ 설정")
    raw_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    user_api_key = raw_key.strip() if raw_key else None
    uploaded_file = st.file_uploader("파일 업로드", type=['pdf', 'png', 'jpg', 'jpeg'])
    mode = st.radio("모드", ["🎓 교수님 브리핑용", "📖 교과서 해설용", "✍️ 논문 결과 작성용"])

st.title("🧠 Psy-Interpreter")

if not user_api_key:
    st.warning("👈 왼쪽 사이드바에 '새로 발급받은' API Key를 입력해주세요.")
elif uploaded_file:
    genai.configure(api_key=user_api_key)
    
    # 모델명을 가장 표준적인 형태로 수정
    model = genai.GenerativeModel('gemini-1.5-flash') 
    
    with st.spinner('박재연 소장님 논문을 분석 중입니다...'):
        try:
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                text = "".join([p.extract_text() for p in reader.pages[:5]])
                response = model.generate_content(f"심리학 전문가로서 다음 논문을 [{mode}] 스타일로 분석해줘:\n\n{text}")
            else:
                img_data = uploaded_file.getvalue()
                response = model.generate_content([f"이 이미지를 [{mode}] 스타일로 해석해줘.", {"mime_type": uploaded_file.type, "data": img_data}])
            
            st.success("✅ 분석 완료!")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"오류 발생: {e}")
