import streamlit as st
import time
from helper import *
import tempfile
import os

# Initialize session state
if "vector_store" not in st.session_state:
    st.session_state["vector_store"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Page Title
st.markdown("<h1 style='text-align: center;'>🤖 DOCUMIND Chatbot</h1>", unsafe_allow_html=True)

# Sidebar for model selection and document upload
with st.sidebar:
    st.subheader("🔍 Select Model")
    model_choice = st.selectbox("Choose a Model", ["LLaMA 3.2"])
    
    st.subheader("📄 Upload a Document or Provide a Link")
    upload_option = st.radio("Choose an option:", ["Upload Document", "Enter Link"])

    if upload_option == "Upload Document":
        uploaded_file = st.file_uploader("Upload your document", type=["pdf", "txt", "docx"])
        if uploaded_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix="."+uploaded_file.name.split(".")[-1]) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_path = temp_file.name
            input_text = process_input(temp_path)
            new_vector_store = build_vector_store(input_text)
            
            if st.session_state["vector_store"] is None:
                st.session_state["vector_store"] = new_vector_store
            else:
                st.session_state["vector_store"].merge_from(new_vector_store)
            os.remove(temp_path)
            st.success("📄 Document processed successfully!")

    elif upload_option == "Enter Link":
        doc_link = st.text_input("Enter the document link")
        if doc_link:
            st.info("🔗 Scanning Link...")
            input_text = process_input(doc_link)
            vector_store = build_vector_store(input_text)
            st.success(f"✅ Link added: {doc_link}")

# Chat Interface
st.markdown("---")
st.markdown("<h2 style='text-align: center;'>💬 Chat with DOCUMIND</h2>", unsafe_allow_html=True)

# Display Chat History
for chat in st.session_state["chat_history"]:
    with st.chat_message(chat["role"]):
        st.markdown(chat["message"])

# User Input
user_prompt = st.chat_input("Ask a question...")

if user_prompt:
    # Add user message to chat history
    st.session_state["chat_history"].append({"role": "user", "message": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    # Retrieve documents
    retrieved_docs = st.session_state["vector_store"].similarity_search(user_prompt, k=15) if st.session_state["vector_store"] else []
    context = "\n\n".join([f"Document {i+1}:\n{doc.page_content}\n" + "-"*50 for i, doc in enumerate(retrieved_docs)])
    
    # Generate response
    response = generate_response(context, user_prompt)
    bot_reply = response["message"]["content"]
    
    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            time.sleep(2)
            st.markdown(bot_reply)
    
    # Add assistant message to chat history
    st.session_state["chat_history"].append({"role": "assistant", "message": bot_reply})