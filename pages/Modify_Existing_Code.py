import streamlit as st
from openai import OpenAI

# Set the page configuration
st.set_page_config(page_title="Coding Assistant", layout="wide")

st.title("Coding Assistant")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []
if "code_input" not in st.session_state:
    st.session_state.code_input = ""
if "initialized" not in st.session_state:
    st.session_state.initialized = False

def initialize_state():
    st.session_state.messages = []
    st.session_state.code_input = ""  # Store code input in session state
    # Add a system message
    system_message = {"role": "system", "content": "You are a helpful Python coding assistant."}
    st.session_state.messages.append(system_message)

def display_chat_history():
    # Display chat history
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

def main():
    if not st.session_state.initialized:
        initialize_state()
        st.session_state.initialized = True

    # Create a text area for the user to paste their code
    code_input = st.text_area("Paste your Python code here:", height=200, value=st.session_state.code_input)

    # Create a second text area for the user to ask their question
    question_input = st.text_area("Ask your question about the code:", height=100, value="", placeholder="Type your question here...")

    if st.button("Submit"):
        # Save the code input in session
        st.session_state.code_input = code_input

        # Handle the question input
        if question_input:
            # Append the user question to messages
            st.session_state.messages.append({"role": "user", "content": question_input})

            # Display the question message
            with st.chat_message("user"):
                st.markdown(question_input)

            # Prepare the messages to send to the assistant, including the current code
            messages_to_send = st.session_state.messages + [{"role": "user", "content": f"Code:\n{st.session_state.code_input}"}]

            # Get response from the assistant
            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model="gpt-4o-mini-2024-07-18",
                    messages=messages_to_send,
                    stream=True,
                )
                response = st.write_stream(stream)

            # Append the assistant's response to messages
            st.session_state.messages.append({"role": "assistant", "content": response})

        # Clear the question input after processing
        question_input = ""

    if st.button("New Chat"):
        initialize_state()


if __name__ == '__main__':
    main()