import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- 앱 설정 ---
st.set_page_config(page_title="Psy-Interpreter Pro", layout="wide")

# --- 사이드바 ---
with st.sidebar:
    st.header("⚙️ 설정")
    # API 키 입력 시 앞뒤 공백을 자동으로 제거합니다.
    raw_key = st.text_input("Gemini API Key를 입력하세요", type="password")
    user_api_key = raw_key.strip() if raw_key else None
    
    uploaded_file = st.file_uploader("파일 업로드 (PDF, 이미지)", type=['pdf', 'png', 'jpg', 'jpeg'])
    mode = st.radio("모드", ["🎓 교수님 브리핑용", "📖 교과서 해설용", "✍️ 논문 결과 작성용"])

# --- 메인 화면 ---
st.title("🧠 Psy-Interpreter")

if not user_api_key:
    st.warning("👈 왼쪽 사이드바에 Gemini API Key를 입력해주세요.")
elif uploaded_file:
    # API 설정
    genai.configure(api_key=user_api_key)
    
    # [중요] 모델 이름을 가장 단순하게 설정하여 404 에러를 방지합니다.
    # 텍스트 분석용 모델
    model = genai.GenerativeModel('gemini-1.5-flash-latest') 
    
    with st.spinner('박재연 소장님 논문을 분석 중입니다...'):
        try:
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                # 속도와 안정성을 위해 5페이지만 추출
                text = ""
                for i in range(min(5, len(reader.pages))):
                    text += reader.pages[i].extract_text()
                
                # 분석 요청
                response = model.generate_content(f"당신은 심리학 전문가입니다. 다음 내용을 [{mode}] 스타일로 분석해줘:\n\n{text}")
            else:
                # 이미지 분석
                img_data = uploaded_file.getvalue()
                response = model.generate_content([
                    f"이 이미지를 [{mode}] 스타일로 해석해줘.",
                    {"mime_type": uploaded_file.type, "data": img_data}
                ])
            
            st.success("✅ 분석 완료!")
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            # 여전히 에러가 날 경우를 대비한 대체 모델 시도
            try:
                alt_model = genai.GenerativeModel('gemini-1.5-flash')
                # (재시도 로직...)
                st.error(f"기본 모델 오류로 대체 모델을 시도 중입니다... ({e})")
            except:
                st.error(f"최종 오류 발생: {e}")
                st.info("Tip: 구글 AI 스튜디오에서 새로운 API 키를 발급받아보시는 것을 권장합니다.")
