import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# [1] 페이지 설정
st.set_page_config(page_title="Psy-Interpreter Pro", layout="wide", page_icon="🧠")

# [2] 사이드바
with st.sidebar:
    st.header("🧠 심리 통역사 설정")
    
    # [중요] type='password'를 지워서 키가 눈에 보이게 변경!
    user_api_key = st.text_input("Gemini API Key 입력 (여기에 붙여넣으세요)", value="")
    
    # 입력된 키 확인용 (앞 4자리만 보여줌)
    if user_api_key:
        if user_api_key.startswith("AIza"):
            st.caption(f"✅ 정상 키 감지됨 (시작: {user_api_key[:4]}...)")
        else:
            st.error("❌ 키가 'AIza'로 시작하지 않습니다! 다시 확인해주세요.")

    uploaded_file = st.file_uploader("논문 파일 업로드 (PDF)", type=['pdf'])
    mode = st.radio("분석 스타일", ["🎓 교수님 브리핑", "📖 교과서 해설", "✍️ 논문 결과 작성"])

st.title("🧠 심리 통역사 (최종 완성판)")

# [3] 실행 로직
if not user_api_key:
    st.info("👈 왼쪽 사이드바에 'AIza...'로 시작하는 키를 넣어주세요.")
elif uploaded_file:
    # 키 설정
    genai.configure(api_key=user_api_key)
    
    # 아까 진단기에서 성공했던 그 모델!
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    with st.spinner('논문을 분석하고 있습니다...'):
        try:
            reader = PdfReader(uploaded_file)
            text = ""
            for i in range(min(10, len(reader.pages))):
                text += reader.pages[i].extract_text()
            
            prompt = f"당신은 심리학 전문가입니다. 다음 논문을 [{mode}] 스타일로 상세히 분석해줘:\n\n{text}"
            response = model.generate_content(prompt)
            
            st.success("✅ 분석 완료!")
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
