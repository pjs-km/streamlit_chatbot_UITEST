import streamlit as st
import time
import pandas as pd
from PIL import Image

# 로고 이미지 파일 경로 설정 (your_logo.png를 프로젝트 폴더에 넣어주세요)
logo_path = 'your_logo.png'

# --- 사이드바 UI ---
with st.sidebar:
    try:
        logo = Image.open(logo_path)
        st.image(logo, use_column_width=True)
    except FileNotFoundError:
        st.error(f"'{logo_path}' 파일을 찾을 수 없습니다. 프로젝트 폴더에 로고를 넣어주세요.")

    st.header("대화 목록")

    # 새 대화 시작 버튼
    if st.button("새로운 대화 시작"):
        st.session_state.messages = []
        st.session_state.current_chat_name = "새로운 대화"
        st.experimental_rerun()

    st.markdown("---")

    # 대화명 입력 및 저장
    new_chat_name = st.text_input("대화명 입력", value=st.session_state.current_chat_name, key="chat_name_input")
    if st.button("대화 저장"):
        if new_chat_name and st.session_state.messages:
            st.session_state.chat_history[new_chat_name] = st.session_state.messages
            st.session_state.current_chat_name = new_chat_name
            st.success(f"'{new_chat_name}' 대화가 저장되었습니다.")
        else:
            st.error("저장할 대화 내용이 없습니다.")
    
    st.markdown("---")
    
    # 저장된 대화 목록 표시
    if st.session_state.chat_history:
        for chat_name in st.session_state.chat_history:
            if st.button(chat_name, key=chat_name):
                st.session_state.messages = st.session_state.chat_history[chat_name]
                st.session_state.current_chat_name = chat_name
                st.experimental_rerun()

    st.markdown("---")
    st.header("데이터베이스 스키마")
    st.write("### `orders` 테이블")
    st.code("id: INT, customer_id: INT, product_name: VARCHAR, price: DECIMAL")
    st.write("### `customers` 테이블")
    st.code("id: INT, name: VARCHAR, address: VARCHAR")

# --- 세션 상태 초기화 ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
if "current_chat_name" not in st.session_state:
    st.session_state.current_chat_name = "새로운 대화"

# --- 메인 챗봇 UI ---
st.subheader(f"현재 대화: {st.session_state.current_chat_name}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("질문을 입력하세요"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("쿼리 생성 중..."):
            time.sleep(1)
            
            st.markdown("### 생성된 SQL 쿼리")
            st.code(f"SELECT * FROM user_data WHERE name = '{prompt}'", language='sql')
            
            st.markdown("### 쿼리 실행 결과")
            df = pd.DataFrame({
                'name': ['노트북', '스마트폰', '태블릿'],
                'price': [1200, 800, 500]
            })
            st.dataframe(df)

    st.session_state.messages.append({"role": "assistant", "content": ""})
