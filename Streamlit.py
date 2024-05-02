import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from MCQ_generator.utils import read_file,get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from MCQ_generator.mcqgenerator import generate_evaluate_chain
from MCQ_generator.logger import logging

#loading json file

with open('Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

#creating a title for the app
st.title("MCQs Creator Application with LangChain 🦜⛓️")

#Create a form using st.form
with st.form("user_inputs"):
    #File Upload
    uploaded_file=st.file_uploader("Uplaod a PDF or txt file")

    #Input Fields
    mcq_count=st.number_input("No. of MCQs", min_value=3, max_value=50)

    #Subject
    subject=st.text_input("Insert Subject",max_chars=20)

    # Quiz Tone
    tone=st.text_input("Complexity Level Of Questions", max_chars=20, placeholder="Simple")

    #Add Button
    button=st.form_submit_button("Create MCQs")
