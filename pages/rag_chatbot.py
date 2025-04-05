import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(".."))
from ragmodel import rag_chatbot

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("🤖 RAG Chatbot")
st.markdown("Ask any question related to the food hamper data or the charity.")

query = st.text_input("Enter your query below:")

if query:
    with st.spinner("Generating answer..."):
        response = rag_chatbot(query)
        st.markdown("### ✅ Response")
        st.write(response)
