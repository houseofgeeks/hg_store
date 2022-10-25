import streamlit as st
from transformers import pipeline


def load_file():
    """Load text from file"""
    uploaded_file = st.file_uploader("Upload text Files",type=['txt'])
    st.button('Get Answer',)
    
    
    
if __name__ == "__main__":

    # App title and description
    st.title("Answering questions from the given text")
    st.write("Upload your text, pose questions and get answers in seconds!")
