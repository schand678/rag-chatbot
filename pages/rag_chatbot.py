import streamlit as st
st.set_page_config(page_title="RAG Chatbot", page_icon="💬")  # ✅ ADD THIS FIRST
import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(".."))
from ragmodel import rag_chatbot



# ✅ Sidebar: Example questions
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


st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("🤖 RAG Chatbot")
st.markdown("Ask any question related to the food hamper data or the charity.")

query = st.text_input("Enter your query below:")

if query:
    with st.spinner("Generating answer..."):
        response = rag_chatbot(query)
        st.markdown("### ✅ Response")
        st.write(response)
