import streamlit as st

# Import your actual agent logic or functions from your backend!
# Example: from backend.agent import run_agent_logic

st.title("My Personal AI Agent 🤖")

# Initialize chat history so the conversation flows naturally
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate the response using your actual agent logic
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Call your real agent function here:
            # response = run_agent_logic(prompt)

            response = f"Echo from your agent: {prompt}"  # Replace this with your actual function output

            st.markdown(response)

    # Add assistant response to state
    st.session_state.messages.append({"role": "assistant", "content": response})