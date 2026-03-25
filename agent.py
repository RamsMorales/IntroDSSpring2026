import streamlit as st
from google import genai
from google.genai import types

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API")

st.title("AI Document Assistant")

## consider session state as a list of variables during a login session
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=api_key) 

with st.sidebar:
    st.title("Setup")
    uploaded_file = st.file_uploader("Upload a file",type=["pdf","txt"])

    if uploaded_file and "doc_ref" not in st.session_state:
        with st.spinner("Uploading your document..."):
            mime_type = uploaded_file.type 
            #mime is an interesting name here > was told it is standard

            
            #goal here: create a file in standard format for the api
            #upload user file to that file.

            #purpose: helps with reducing errors with api and supposedly 
            #"saftey" 

            with open("temp_file","wb") as write_file:
                write_file.write(uploaded_file.getbuffer())
            
            # This is how the api expects things
            doc_ref = st.session_state.client.files.upload(
                file="temp_file",
                config={'mime_type':mime_type}
            )
            st.session_state.doc_ref = doc_ref
            st.session_state.chat = st.session_state.client.chats.create(
                model="gemini-3-flash-preview",# select which model you want to use
                config=types.GenerateContentConfig(
                    system_instruction="You are a document expert. Answer questions ONLY about the uploaded document. If the answer is not in the document, say you don't know"
                )
            )
        st.success("Document uploaded successfully!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask a question about the document")

if prompt:
    if "chat" not in st.session_state:
        st.error("Please upload a document first")
    else:
        st.session_state.messages.append({"role":"user","content":prompt})
        with st.chat_message("user",avatar="🙈"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(
                message=[st.session_state.doc_ref,prompt]
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role":"assistant","content":response.text})
os.remove("temp_file")