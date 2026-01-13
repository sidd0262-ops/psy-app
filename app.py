import streamlit as st
import google.generativeai as genai
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
    # 모델 설정: 'models/'를 제거하고 가장 표준적인 이름을 사용합니다.
    genai.configure(api_key=user_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') 
    
    with st.spinner('박재연 소장님 논문을 분석 중입니다. 잠시만 기다려주세요...'):
        try:
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                # 텍스트 추출 (최대 15페이지까지 확장)
                text = ""
                for i in range(min(15, len(reader.pages))):
                    text += reader.pages[i].extract_text()
                
                # AI 분석 요청
                prompt = f"당신은 심리학 통계 전문가입니다. 다음 논문 내용을 바탕으로 [{mode}] 스타일로 상세히 설명해주세요:\n\n{text}"
                response = model.generate_content(prompt)
            else:
                # 이미지 파일 분석
                img_data = uploaded_file.getvalue()
                response = model.generate_content([
                    f"이 통계 이미지를 [{mode}] 스타일로 전문적으로 해석해줘.",
                    {"mime_type": uploaded_file.type, "data": img_data}
                ])
            
            st.success("✅ 분석 완료!")
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            # 404 에러 등이 발생할 경우를 대비한 상세 안내
            st.error(f"분석 중 오류가 발생했습니다: {e}")
            st.info("Tip: API 키가 정확한지, 혹은 모델 이름이 지원되는지 확인이 필요합니다.")
