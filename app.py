import streamlit as st
import time
from helper import *

vector_store = build_vector_store("https://python.langchain.com/docs/introduction/")

st.title("📄 DOCUMIND")

model_choice = st.selectbox("Select Model", ["llama 3.2"])

st.subheader("Upload a Document or Provide a Link")
upload_option = st.radio("Choose an option:", ["Upload Document", "Enter Link"])

scanning_message = ""

if upload_option == "Upload Document":
    uploaded_file = st.file_uploader("Upload your document", type=["pdf", "txt", "docx"])
    if uploaded_file:
        input_text = process_input(uploaded_file)
        vector_store = build_vector_store(input_text)
        file_extension = uploaded_file.name.split(".")[-1]
        scanning_message = f"📄 Scanning {file_extension.upper()} file..."
        st.success(f"Uploaded: {uploaded_file.name}")
        st.info(scanning_message)

elif upload_option == "Enter Link":
    doc_link = st.text_input("Enter the document link")
    if doc_link:
        scanning_message = "🔗 Scanning Link..."
        input_text = process_input(doc_link)
        vector_store = build_vector_store(input_text)
        st.success(f"Link added: {doc_link}")
        st.info(scanning_message)


user_prompt = st.text_input("Enter your prompt", "")

retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 15})
filtered_results = filtered_retrieval(user_prompt, vector_store)


retrieved_docs = retriever.get_relevant_documents(user_prompt)
context = "\n\n".join([f"Document {i+1}:\n{doc.page_content}\n" + "-"*50 for i, doc in enumerate(retrieved_docs)])

response = generate_response(context, user_prompt)

if st.button("Submit"):
    if user_prompt:
        st.subheader("Model's Answer")
        st.write("🔍 Processing... (Integration with backend model needed)")
        time.sleep(2)
        st.success(response["message"]["content"])

    else:
        st.warning("Please enter a prompt!")
