import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# [1] 페이지 설정
st.set_page_config(page_title="Psy-Interpreter Auto", layout="wide", page_icon="🕵️")

with st.sidebar:
    st.header("🕵️ 자동 탐지 모드")
    # 공백 제거 기능 추가 (.strip)
    user_api_key = st.text_input("Gemini API Key 입력 (여기에 붙여넣으세요)", value="").strip()
    
    if user_api_key:
        if user_api_key.startswith("AIza"):
            st.caption(f"✅ 키 형식 정상 (시작: {user_api_key[:4]}...)")
        else:
            st.error("❌ 키가 'AIza'로 시작하지 않습니다.")

    uploaded_file = st.file_uploader("논문 파일 업로드 (PDF)", type=['pdf'])
    mode = st.radio("분석 스타일", ["🎓 교수님 브리핑", "📖 교과서 해설", "✍️ 논문 결과 작성"])

st.title("🕵️ 심리 통역사 (자동 탐지판)")

if not user_api_key:
    st.info("👈 왼쪽 사이드바에 키를 입력해주세요.")
elif uploaded_file:
    genai.configure(api_key=user_api_key)
    
    with st.spinner('사용 가능한 AI 모델을 찾는 중...'):
        try:
            # [핵심] 구글이 제공하는 '진짜 모델 이름'을 직접 가져옴
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # 우선순위: Flash -> Pro -> 구형 Pro
            target_model = None
            for candidate in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
                if candidate in available_models:
                    target_model = candidate
                    break
            
            # 만약 못 찾으면 목록의 첫 번째 놈을 강제로 선택
            if not target_model and available_models:
                target_model = available_models[0]
            
            if target_model:
                st.success(f"✅ 연결 성공! 감지된 모델: {target_model}")
                
                # 분석 시작
                model = genai.GenerativeModel(target_model)
                reader = PdfReader(uploaded_file)
                text = ""
                for i in range(min(10, len(reader.pages))):
                    text += reader.pages[i].extract_text()
                
                prompt = f"당신은 심리학 전문가입니다. 다음 논문을 [{mode}] 스타일로 상세히 분석해줘:\n\n{text}"
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown(response.text)
            else:
                st.error("🚫 사용 가능한 모델을 찾을 수 없습니다. API 키 권한을 확인해주세요.")
                
        except Exception as e:
            st.error(f"오류 발생: {e}")
            st.warning("팁: 키를 지웠다가 다시 붙여넣고 엔터를 쳐보세요.")
