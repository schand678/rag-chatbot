import streamlit as st
st.set_page_config(page_title="RAG Chatbot", page_icon="💬")  # ✅ First Streamlit command

import sys
import os
sys.path.append(os.path.abspath(".."))
from ragmodel import rag_chatbot

# Sidebar content
st.sidebar.title("💬 Example Questions")
st.sidebar.markdown(
    """
    **Try asking:**
    - What locations were the hampers picked up from?
    - Who picked up the premium hampers?
    - How many hampers were picked up?
    - When was the last pickup?
    - What is the average age of the clients?
    - List all pickup dates and types.
    """
)

# Main section logic (optional placeholder)
st.title("RAG Chatbot Interface")
query = st.text_input("Ask a question:")
if query:
    with st.spinner("Generating answer..."):
        response = rag_chatbot(query)
        st.markdown(f"**Answer:** {response}")
