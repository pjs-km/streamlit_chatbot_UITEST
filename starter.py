import streamlit as st
import time

# 챗봇 제목 설정
st.title("NL to SQL 챗봇")

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 대화 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("질문을 입력하세요"):
    # 사용자 메시지 표시
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 챗봇 응답 시뮬레이션
    with st.chat_message("assistant"):
        with st.spinner("쿼리 생성 중..."):
            time.sleep(2)  # 백엔드 연결 대신 시간 지연 시뮬레이션
            response = f"귀하의 질문에 대한 SQL 쿼리입니다:\n\n```sql\nSELECT * FROM user_data WHERE name = '{prompt}'\n```"
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

import streamlit as st

# 사이드바에 스키마 정보 표시
st.sidebar.header("데이터베이스 스키마")
st.sidebar.write("### `orders` 테이블")
st.sidebar.code("id: INT, customer_id: INT, product_name: VARCHAR, price: DECIMAL")
st.sidebar.write("### `customers` 테이블")
st.sidebar.code("id: INT, name: VARCHAR, address: VARCHAR")

import pandas as pd
import streamlit as st

# SQL 쿼리 출력
st.subheader("생성된 SQL 쿼리")
st.code("SELECT name, price FROM products WHERE category = 'electronics'", language='sql')

# 쿼리 실행 결과 테이블 출력 (더미 데이터 사용)
st.subheader("쿼리 실행 결과")
df = pd.DataFrame({
    'name': ['노트북', '스마트폰', '태블릿'],
    'price': [1200, 800, 500]
})
st.dataframe(df)

import streamlit as st
import time

# 제목 설정
st.title("NL to SQL 챗봇")

# --- 세션 상태 초기화 ---
# 'messages'는 현재 대화 기록을 저장합니다.
if "messages" not in st.session_state:
    st.session_state.messages = []

# 'chat_history'는 저장된 대화 목록을 딕셔너리 형태로 저장합니다.
# {대화명: [대화기록1, 대화기록2, ...]}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

# 'current_chat_name'은 현재 대화의 이름을 저장합니다.
if "current_chat_name" not in st.session_state:
    st.session_state.current_chat_name = "새로운 대화"


# --- 사이드바 UI ---
with st.sidebar:
    st.header("대화 목록")

    # 대화명 입력 및 저장
    new_chat_name = st.text_input("새 대화명", value=st.session_state.current_chat_name)
    if st.button("대화 저장"):
        if new_chat_name and st.session_state.messages:
            # 현재 대화 기록을 chat_history에 저장
            st.session_state.chat_history[new_chat_name] = st.session_state.messages
            st.session_state.current_chat_name = new_chat_name
            st.success(f"'{new_chat_name}' 대화가 저장되었습니다.")

    st.markdown("---")

    # 저장된 대화 목록 표시
    if st.session_state.chat_history:
        for chat_name in st.session_state.chat_history:
            if st.button(chat_name, key=chat_name):
                # 버튼 클릭 시 해당 대화 기록 불러오기
                st.session_state.messages = st.session_state.chat_history[chat_name]
                st.session_state.current_chat_name = chat_name
                st.experimental_rerun()  # 페이지를 다시 로드하여 새 대화 기록 표시


# --- 메인 챗봇 UI ---
st.subheader(f"현재 대화: {st.session_state.current_chat_name}")

# 기존 대화 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("질문을 입력하세요"):
    # 사용자 메시지 표시
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 챗봇 응답 시뮬레이션
    with st.chat_message("assistant"):
        with st.spinner("쿼리 생성 중..."):
            time.sleep(1)
            response = "백엔드가 준비되면 여기에 응답이 표시됩니다."
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
