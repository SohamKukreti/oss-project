from pages.finance_tracker_data.mainbot import generateResponse
import streamlit as st


    
st.set_page_config(page_title="Finance Helper bot")
with st.sidebar:
    st.title('Finance Helper bot')
    filename = st.selectbox(
        "Select a file for data:",
        options=["newsdata", "taxdata"],  # Available files
        help="Choose the dataset you want the bot to use."
    )



# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Welcome, let's make finances simple!"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User-provided prompt
if input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": input})
    with st.chat_message("user"):
        st.write(input)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Getting your answer from my sources.."):
            response = generateResponse(input, filename) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)