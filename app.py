import streamlit as st
from openai import OpenAI

# Set the page configuration
st.set_page_config(page_title="Coding Assistant", layout="wide")

st.title("Coding assistant")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

def initialize_state():
    st.session_state.messages = []
    # Add a system message
    system_message = {"role": "system", "content": "You are a helpful Python coding assistant."}
    st.session_state.messages.append(system_message)

def display_chat_history():
    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def main():
    if "initialized" not in st.session_state:
        initialize_state()
        st.session_state.initialized = True

    prompt = st.chat_input("I am ready to help!")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get response from the assistant
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                messages=st.session_state.messages,  # Messages now include the system prompt
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    if st.button("New Chat"):
        initialize_state()

    display_chat_history()

if __name__ == '__main__':
    main()