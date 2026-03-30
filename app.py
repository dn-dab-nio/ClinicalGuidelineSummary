#Tu będzie front-end
import pandas as pd
import streamlit as st


st.title('Clinical Guidelines Summary System')
input = st.text_input("Enter a patient description...")

if st.button("Generate summary"):
    if input is None:
        st.warning("Please enter a patient description...")
        st.stop()

        st.header("Patient Classification (TNM + UICC)")


