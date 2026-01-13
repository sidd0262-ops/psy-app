{\rtf1\ansi\ansicpg949\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import google.generativeai as genai\
import pandas as pd\
from PyPDF2 import PdfReader\
\
# --- \uc0\u50545  \u49444 \u51221  ---\
st.set_page_config(page_title="Psy-Interpreter Pro", layout="wide", page_icon="\uc0\u55358 \u56800 ")\
\
# --- UI \uc0\u49828 \u53440 \u51068 \u47553  ---\
st.markdown("""\
    <style>\
    .stAlert \{ border-radius: 10px; \}\
    .stButton>button \{ border-radius: 20px; height: 3em; background-color: #4A90E2; color: white; \}\
    </style>\
    """, unsafe_allow_html=True)\
\
# --- \uc0\u49324 \u51060 \u46300 \u48148 : \u49444 \u51221  \u50689 \u50669  ---\
with st.sidebar:\
    st.header("\uc0\u9881 \u65039  \u49444 \u51221  \u48143  \u50629 \u47196 \u46300 ")\
    \
    # API \uc0\u53412  \u51077 \u47141 \u52285  (\u49324 \u50857 \u51088 \u44032  \u51649 \u51217  \u51077 \u47141 )\
    user_api_key = st.text_input("Gemini API Key\uc0\u47484  \u51077 \u47141 \u54616 \u49464 \u50836 ", type="password")\
    st.caption("[API Key \uc0\u48156 \u44553 \u48155 \u44592 ](https://aistudio.google.com/app/apikey)")\
    \
    st.divider()\
    \
    uploaded_file = st.file_uploader(\
        "\uc0\u48516 \u49437 \u54624  \u54028 \u51068  (PDF, PNG, JPG)", \
        type=['pdf', 'png', 'jpg', 'jpeg']\
    )\
    \
    mode = st.radio("\uc0\u48516 \u49437  \u47784 \u46300 ", ["\u55356 \u57235  \u44368 \u49688 \u45784  \u48652 \u47532 \u54609 \u50857 ", "\u55357 \u56534  \u44368 \u44284 \u49436  \u54644 \u49444 \u50857 ", "\u9997 \u65039  \u45436 \u47928  \u44208 \u44284  \u51089 \u49457 \u50857 "])\
\
# --- \uc0\u47700 \u51064  \u47196 \u51649  ---\
st.title("\uc0\u55358 \u56800  Psy-Interpreter")\
st.info("\uc0\u49900 \u47532 \u53685 \u44228  \u44208 \u44284 \u50752  \u45436 \u47928 \u51012  \u50976 \u52285 \u54616 \u44172  \u49444 \u47749 \u54644 \u51452 \u45716  AI \u48708 \u49436 \u51077 \u45768 \u45796 .")\
\
if not user_api_key:\
    st.warning("\uc0\u55357 \u56392  \u50812 \u51901  \u49324 \u51060 \u46300 \u48148 \u50640  API Key\u47484  \u47676 \u51200  \u51077 \u47141 \u54644 \u51452 \u49464 \u50836 .")\
else:\
    genai.configure(api_key=user_api_key)\
    model = genai.GenerativeModel('gemini-1.5-flash')\
\
    if uploaded_file:\
        with st.spinner('AI\uc0\u44032  \u45936 \u51060 \u53552 \u47484  \u48516 \u49437 \u54616 \u44256  \u51080 \u49845 \u45768 \u45796 ...'):\
            try:\
                # 1. \uc0\u47928 \u49436 /\u51060 \u48120 \u51648  \u52376 \u47532 \
                if uploaded_file.type == "application/pdf":\
                    reader = PdfReader(uploaded_file)\
                    text = ""\
                    # \uc0\u54645 \u49900  \u54168 \u51060 \u51648 (\u52488 \u48152 \u48512 +\u44208 \u44284 \u48512 ) \u52628 \u52636 \
                    total_pages = len(reader.pages)\
                    sample_pages = list(range(min(10, total_pages))) + list(range(max(0, total_pages-5), total_pages))\
                    for i in sorted(set(sample_pages)):\
                        text += reader.pages[i].extract_text()\
                    input_data = [f"\uc0\u45436 \u47928  \u53581 \u49828 \u53944  \u48516 \u49437  \u50836 \u52397 :\\n\{text[:15000]\}"]\
                else:\
                    image_data = uploaded_file.getvalue()\
                    input_data = [\
                        \{"mime_type": uploaded_file.type, "data": image_data\},\
                        "\uc0\u51060  \u53685 \u44228  \u44208 \u44284  \u54364 \u51032  \u49688 \u52824 \u47484  \u49900 \u47532 \u54617 \u51201 \u51004 \u47196  \u54644 \u49437 \u54644 \u51480 ."\
                    ]\
\
                # 2. \uc0\u54532 \u47212 \u54532 \u53944  \u49892 \u54665 \
                prompt = f"""\
                \uc0\u45817 \u49888 \u51008  \u49900 \u47532 \u54617  \u53685 \u44228  \u51204 \u47928 \u44032 \u51077 \u45768 \u45796 . \u51228 \u49884 \u46108  \u51088 \u47308 \u47484  [\{mode\}] \u49828 \u53440 \u51068 \u47196  \u49345 \u49464 \u55176  \u49444 \u47749 \u54616 \u49464 \u50836 .\
                \uc0\u45236 \u50857 \u50640 \u45716  \u48152 \u46300 \u49884  \u45796 \u51020 \u51060  \u54252 \u54632 \u46104 \u50612 \u50556  \u54633 \u45768 \u45796 :\
                1. \uc0\u50672 \u44396  \u44032 \u49444  \u48143  \u48320 \u49688 \u44036 \u51032  \u44288 \u44228 (\u47588 \u44060 /\u51312 \u51208  \u46321 ) \u47749 \u54869 \u54868 \
                2. \uc0\u53685 \u44228 \u52824 (p, Beta, F, t, R\'b2)\u51032  \u44396 \u52404 \u51201  \u54644 \u49444 \
                3. \uc0\u44368 \u49688 \u45784 \u51032  \u50696 \u49345  \u50517 \u48149  \u51656 \u47928 \u44284  \u50976 \u52285 \u54620  \u48169 \u50612  \u45813 \u48320  2\u49464 \u53944 \
                4. \uc0\u54617 \u49696 \u51201 \u51064  \u54620  \u51460  \u50836 \u50557 \
                """\
                \
                response = model.generate_content([prompt] + input_data)\
                \
                # 3. \uc0\u44208 \u44284  \u54868 \u47732  \u44396 \u49457 \
                st.success("\uc0\u9989  \u48516 \u49437  \u50756 \u47308 !")\
                st.markdown("---")\
                st.markdown(response.text)\
                \
            except Exception as e:\
                st.error(f"\uc0\u48516 \u49437  \u51473  \u50724 \u47448 \u44032  \u48156 \u49373 \u54664 \u49845 \u45768 \u45796 : \{e\}")\
    else:\
        st.write("\uc0\u54028 \u51068 \u51012  \u50629 \u47196 \u46300 \u54616 \u47732  \u51060 \u44275 \u50640  \u44208 \u44284 \u44032  \u45208 \u53440 \u45225 \u45768 \u45796 .")\
\
}
