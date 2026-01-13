import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- 앱 설정 ---
st.set_page_config(page_title="Psy-Interpreter Pro", layout="wide", page_icon="🧠")

# --- 사이드바 ---
with st.sidebar:
    st.header("⚙️ 설정 및 업로드")
    # API 키 입력 시 공백 제거 처리 추가
    raw_api_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    user_api_key = raw_api_key.strip() if raw_api_key else None
    
    uploaded_file = st.file_uploader("파일 업로드 (PDF, 이미지)", type=['pdf', 'png', 'jpg', 'jpeg'])
    mode = st.radio("모드", ["🎓 교수님 브리핑용", "📖 교과서 해설용", "✍️ 논문 결과 작성용"])

# --- 메인 화면 ---
st.title("🧠 Psy-Interpreter")

if not user_api_key:
    st.warning("👈 왼쪽 사이드바에 API Key를 입력해주세요.")
elif uploaded_file:
    # 가장 안정적인 모델인 gemini-pro 설정 (404 에러 방지)
    genai.configure(api_key=user_api_key)
    model = genai.GenerativeModel('gemini-pro') 
    
    with st.spinner('박재연 소장님 논문을 정밀 분석 중입니다...'):
        try:
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                # 속도와 정확도를 위해 앞쪽 10페이지만 추출
                text = ""
                for i in range(min(10, len(reader.pages))):
                    text += reader.pages[i].extract_text()
                
                # 프롬프트 최적화
                prompt = f"당신은 심리학 및 통계 전문가입니다. 다음 논문을 [{mode}] 스타일로 분석해 주세요. 핵심 수치와 결론을 중심으로 설명해야 합니다:\n\n{text}"
                response = model.generate_content(prompt)
            else:
                # 이미지 분석 (이미지 전용 모델로 자동 전환)
                vision_model = genai.GenerativeModel('gemini-1.5-flash')
                img_data = uploaded_file.getvalue()
                response = vision_model.generate_content([
                    f"이 통계 이미지를 [{mode}] 스타일로 해석해줘.",
                    {"mime_type": uploaded_file.type, "data": img_data}
                ])
            
            st.success("✅ 분석 완료!")
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
            st.info("Tip: API 키가 유효한지 다시 확인하거나, 잠시 후 다시 시도해 주세요.")
