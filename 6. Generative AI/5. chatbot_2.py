from langchain_openai import ChatOpenAI
from langchain_classic.schema import SystemMessage, HumanMessage, AIMessage
import streamlit as st
from streamlit_chat import message
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), override=True)

st.set_page_config(page_title="Nova GPT", page_icon="🤖")

st.subheader("Your Custom GPT to help you with everyday tasks")

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.2,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    system_message = st.text_input(label="Assitant Role")
    user_prompt = st.text_input("Enter your message")

    if system_message:
        if not any(isinstance(x, SystemMessage) for x in st.session_state.messages):
            st.session_state.messages.append(SystemMessage(content=system_message))

    if user_prompt:
        st.session_state.messages.append(HumanMessage(content=user_prompt))
        with st.spinner("Assistant is typing..."):
            response = llm.invoke(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))


# st.session_state.messages

# message("This is Chatgpt", is_user=False)
# message("This is a user", is_user=True)


for i, msg in enumerate(st.session_state.messages[1:]):
    if i%2==0:
        message(msg.content, is_user=False, key=f"{i}+ 😎")
    else: 
        message(msg.content, is_user=True, key=f"{i}+ 😍")