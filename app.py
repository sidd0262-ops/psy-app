import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# [1] 페이지 설정
st.set_page_config(page_title="Psy-Interpreter Pro", layout="wide", page_icon="🧠")

# [2] 사이드바 설정
with st.sidebar:
    st.header("🧠 심리 통역사 설정")
    # 비밀번호처럼 가려지는 입력칸
    raw_key = st.text_input("Gemini API Key 입력", type="password")
    user_api_key = raw_key.strip() if raw_key else None
    
    uploaded_file = st.file_uploader("논문 파일 업로드 (PDF)", type=['pdf'])
    mode = st.radio("분석 스타일", ["🎓 교수님 브리핑", "📖 교과서 해설", "✍️ 논문 결과 작성"])

st.title("🧠 심리 통역사 (최종 완성판)")

# [3] 분석 로직
if not user_api_key:
    st.info("👈 왼쪽 사이드바에 방금 확인하신 '정상 키(AIza...)'를 입력해주세요.")
elif uploaded_file:
    # 키 설정
    genai.configure(api_key=user_api_key)
    
    # [핵심] 방금 진단기에서 성공한 그 모델!
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    with st.spinner('논문을 분석하고 있습니다...'):
        try:
            reader = PdfReader(uploaded_file)
            text = ""
            # 최대 10페이지까지만 추출 (속도 최적화)
            for i in range(min(10, len(reader.pages))):
                text += reader.pages[i].extract_text()
            
            # AI에게 질문
            prompt = f"당신은 심리학 전문가입니다. 다음 논문을 [{mode}] 스타일로 상세히 분석해줘:\n\n{text}"
            response = model.generate_content(prompt)
            
            st.success("✅ 분석 완료!")
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
