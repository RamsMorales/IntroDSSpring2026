import streamlit as st
def on_select_change():
    if st.session_state.search_category != None:
        st.session_state.search_text = ""

def on_text_change():
    if st.session_state.search_text:
        st.session_state.search_category = None