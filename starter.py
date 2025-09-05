import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, ChatMessage
from langchain.callbacks.base import BaseCallbackHandler
from dotenv import load_dotenv
from pdfminer.high_level import extract_text

load_dotenv()

# 스트리밍 핸들러
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

# PDF 텍스트 추출
def get_pdf_text(filename):
    raw_text = extract_text(filename)
    return raw_text

# 문서 전처리 + 벡터스토어 생성
def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        raw_text = get_pdf_text(uploaded_file)
        text_splitter = CharacterTextSplitter(
            separator="\n\n",
            chunk_size=1000,
            chunk_overlap=200,
        )
        all_splits = text_splitter.create_documents([raw_text])
        st.write(f"총 {len(all_splits)}개의 passage 생성됨.")

        vectorstore = FAISS.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())
        return vectorstore, raw_text
    return None, None

# 일반 질의응답 (RAG)
def generate_response(query_text, vectorstore, callback):
    docs_list = vectorstore.similarity_search(query_text, k=3)
    docs = ""
    for i, doc in enumerate(docs_list):
        docs += f"'문서{i+1}':{doc.page_content}\n"

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, streaming=True, callbacks=[callback])
    
    rag_prompt = [
        SystemMessage(
            content="너는 문서에 대해 질의응답을 하는 '문서봇'이야. "
                    "주어진 문서를 참고하여 사용자의 질문에 답변을 해줘. "
                    "문서에 내용이 정확하게 나와있지 않으면 대답하지 마."
        ),
        HumanMessage(
            content=f"질문:{query_text}\n\n{docs}"
        ),
    ]

    response = llm(rag_prompt)
    return response.content

# PDF 기반 퀴즈 생성
def generate_quiz(raw_text, callback):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, streaming=True, callbacks=[callback])

    quiz_prompt = [
        SystemMessage(
            content="업로드된 문서를 바탕으로 객관식 3문제를 만들어줘. "
                    "각 문항에는 보기 4개(A~D)와 정답을 포함시켜줘."
        ),
        HumanMessage(
            content=raw_text
        )
    ]

    response = llm(quiz_prompt)
    return response.content

# Streamlit 페이지 설정
st.set_page_config(page_title='🦜🔗 문서 기반 QA & 퀴즈 챗봇')
st.title('🦜🔗 문서 기반 QA & 퀴즈 챗봇')

# 파일 업로드
st.sidebar.header('📄 파일 업로드')
uploaded_file = st.sidebar.file_uploader('문서를 업로드하세요', type=['hwp', 'pdf'])

# Reset 버튼 사이드바에 추가
st.sidebar.header("⚙️ 세션 관리")
if st.sidebar.button("Reset Session", key="reset", help="모든 세션을 초기화합니다.", on_click=lambda: st.session_state.clear()):
    st.experimental_rerun()

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        ChatMessage(role="assistant", content="안녕하세요! 업로드한 문서 기반 QA 및 퀴즈 챗봇입니다.")
    ]

# 대화 내역 출력
for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

# 사용자 입력 처리
if prompt := st.chat_input("질문을 입력하거나 '퀴즈'라고 입력해보세요!"):
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())

        if prompt.strip().lower() == "퀴즈":
            response = generate_quiz(st.session_state['raw_text'], stream_handler)
        else:
            response = generate_response(prompt, st.session_state['vectorstore'], stream_handler)

        st.session_state["messages"].append(
            ChatMessage(role="assistant", content=response)
        )
