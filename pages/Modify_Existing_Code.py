import streamlit as st
from openai import OpenAI

# Set the page configuration
st.set_page_config(page_title="Coding Assistant", layout="wide")

st.title("Coding Assistant")

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
        if message['content'].startswith("Code:"):
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def main():
    if "initialized" not in st.session_state:
        initialize_state()
        st.session_state.initialized = True

    # Create a text area for the user to paste their code
    code_input = st.text_area("Paste your Python code here:", height=200)

    # Create a second text area for the user to ask their question
    question_input = st.text_area("Ask your question about the code:", height=100)

    if st.button("Submit"):
        if code_input:
            st.session_state.messages.append({"role": "user", "content": f"Code:\n{code_input}"})
        if question_input:
            st.session_state.messages.append({"role": "user", "content": question_input})

        # Display the user messages
        if code_input:
            with st.chat_message("user"):
                st.markdown(f"Code:\n{code_input}")
        if question_input:
            with st.chat_message("user"):
                st.markdown(question_input)

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

    # Display the updated chat history
    display_chat_history()

if __name__ == '__main__':
    main()