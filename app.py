import streamlit as st
import google.generativeai as genai
import sys

st.title("🚑 긴급 진단 모드")

# 1. 내 컴퓨터(서버) 상태 확인
st.write(f"Python 버전: {sys.version.split()[0]}")
try:
    st.write(f"AI 엔진 버전: {genai.__version__}")
except:
    st.error("⚠️ 엔진 설치가 안 되었습니다.")

# 2. 키 입력 (비밀번호 가리기 해제)
user_key = st.text_input("새로 받은 키를 붙여넣으세요:", type="default") 

if st.button("진단 시작"):
    if not user_key:
        st.warning("키를 먼저 입력해주세요.")
    else:
        st.write("---")
        # [1단계] 키 모양 검사
        first_4 = user_key[:4]
        st.write(f"🔑 입력하신 키의 앞 4글자: **{first_4}**")
        
        if not user_key.startswith("AIza"):
            st.error("❌ **[중요]** 키가 'AIza'로 시작하지 않습니다! 복사 과정에서 앞부분이 잘렸을 가능성이 99%입니다.")
        else:
            st.success("✅ 키 형식(AIza...)은 정상입니다.")

        # [2단계] 실제 연결 테스트
        genai.configure(api_key=user_key)
        try:
            st.info("📡 구글 서버에 접속을 시도합니다...")
            # 가장 기초적인 명령(모델 목록 조회)을 보내봄
            models = list(genai.list_models())
            st.success("🎉 **연결 성공!** 에러가 해결되었습니다.")
            st.write("감지된 모델 목록:")
            for m in models:
                if 'gemini' in m.name:
                    st.write(f"- {m.name}")
        except Exception as e:
            st.error("💀 **치명적 오류 발생!** 아래 메시지를 확인해주세요:")
            st.code(str(e)) # 에러의 진짜 원인을 그대로 출력
            st.warning("☝️ 위 빨간색 박스 안의 영어 메시지를 캡처하거나 복사해서 알려주세요.")
