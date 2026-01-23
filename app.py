import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# [1] 페이지 설정
st.set_page_config(page_title="Psy-Interpreter Auto", layout="wide", page_icon="🧠")

with st.sidebar:
    st.header("🧠 심리 통역사 설정")
    
    # [핵심] 1. 비밀 금고(Secrets)에서 키를 찾아봄
    if "GEMINI_API_KEY" in st.secrets:
        user_api_key = st.secrets["GEMINI_API_KEY"]
        st.success("🔐 저장된 API 키를 자동으로 불러왔습니다!")
    # [핵심] 2. 없으면 직접 입력받음
    else:
        user_api_key = st.text_input("Gemini API Key 입력", type="password")

    uploaded_file = st.file_uploader("논문 파일 업로드 (PDF)", type=['pdf'])
    mode = st.radio("분석 스타일", ["🎓 교수님 브리핑", "📖 교과서 해설", "✍️ 논문 결과 작성"])

st.title("🧠 심리 통역사 (자동 로그인)")

if not user_api_key:
    st.info("👈 왼쪽 사이드바에 API 키를 입력하거나, App Settings > Secrets에 저장해주세요.")
elif uploaded_file:
    genai.configure(api_key=user_api_key)
    
    with st.spinner('AI 모델과 연결 중...'):
        try:
            # 자동 탐지 로직
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            target_model = None
            
            # 우선순위: Flash -> Pro
            for candidate in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
                if candidate in available_models:
                    target_model = candidate
                    break
            
            if not target_model and available_models:
                target_model = available_models[0]
            
            if target_model:
                # 모델 연결
                model = genai.GenerativeModel(target_model)
                
                # PDF 읽기
                reader = PdfReader(uploaded_file)
                text = ""
                for i in range(min(10, len(reader.pages))):
                    text += reader.pages[i].extract_text()
                
                # 분석 요청
                prompt = f"당신은 심리학 전문가입니다. 다음 논문을 [{mode}] 스타일로 상세히 분석해줘:\n\n{text}"
                response = model.generate_content(prompt)
                
                st.success(f"✅ 분석 완료! (사용 모델: {target_model})")
                st.markdown("---")
                st.markdown(response.text)
            else:
                st.error("🚫 사용 가능한 모델을 찾을 수 없습니다.")
                
        except Exception as e:
            st.error(f"오류 발생: {e}")
