import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- 앱 설정 ---
st.set_page_config(page_title="Psy-Interpreter Pro", layout="wide", page_icon="🧠")

# --- 사이드바 ---
with st.sidebar:
    st.header("⚙️ 설정 및 업로드")
    # API 키 입력 시 앞뒤 공백 제거
    raw_api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    user_api_key = raw_api_key.strip() if raw_api_key else None
    
    uploaded_file = st.file_uploader("파일 업로드 (PDF, 이미지)", type=['pdf', 'png', 'jpg', 'jpeg'])
    mode = st.radio("모드", ["🎓 교수님 브리핑용", "📖 교과서 해설용", "✍️ 논문 결과 작성용"])

# --- 메인 화면 ---
st.title("🧠 Psy-Interpreter")

if not user_api_key:
    st.warning("👈 왼쪽 사이드바에 API Key를 입력해주세요.")
elif uploaded_file:
    # API 설정
    genai.configure(api_key=user_api_key)
    
    # [중요] 404 에러 방지를 위한 표준 모델명 설정
    model = genai.GenerativeModel('gemini-1.5-flash') 
    
    with st.spinner('박재연 소장님 논문을 분석 중입니다...'):
        try:
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                # 속도와 안정성을 위해 5페이지만 추출
                text = ""
                for i in range(min(5, len(reader.pages))):
                    text += reader.pages[i].extract_text()
                
                # 분석 요청
                prompt = f"당신은 심리학 통계 전문가입니다. 다음 논문을 [{mode}] 스타일로 분석해줘:\n\n{text}"
                response = model.generate_content(prompt)
            else:
                # 이미지 분석
                img_data = uploaded_file.getvalue()
                response = model.generate_content([
                    f"이 통계 이미지를 [{mode}] 스타일로 해석해줘.",
                    {"mime_type": uploaded_file.type, "data": img_data}
                ])
            
            st.success("✅ 분석 완료!")
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
            st.info("Tip: 404 에러가 지속되면 Google AI Studio에서 'New Project'로 API 키를 새로 발급받아보세요.")
