import streamlit as st
from transformers import pipeline


def load_file():
    """Load text from file"""
    uploaded_file = st.file_uploader("Upload text Files",type=['txt'])
    st.button('Get Answer',)