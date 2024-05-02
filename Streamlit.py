import os
import json
import traceback
import pandas as pd
from src.MCQ_generator.utils import read_file,get_table_data
import fitz
import streamlit as st

from src.MCQ_generator.mcqgenerator import generate_evaluate_chain
from src.MCQ_generator.logger import logging

#loading json file

with open("D:\MCQ_Generator\Response.json","r") as file:
    RESPONSE_JSON=json.load(file)

# Creating a Title For APP Streamlit.py
st.title("MCQ Generator Application WITH GEMINI-PRO And LangChain")
logging.info("The title is set")

# Create a Form Using st.form
with st.form("user_input"):
        # uplode file
        uploded_file = st.file_uploader("Uplode a PDF or TXT File")

        # Input Field 
        mcq_count = st.number_input("Number of MCQs",min_value=3,max_value=100)

        #Subject field
        subject = st.text_input("Insert Subject",max_chars=25)

        # Quiz Tone Field
        tone  = st.text_input("Complexity Level Of Questions",max_chars=20,placeholder="Simple")

        #Add Button
        button = st.form_submit_button("Create MCQs")

        # Check if the button is clicked and all fields have input

    if button and uploded_file is not None and mcq_count and subject and tone:

        with st.spinner("Loading..."):
            try:
                text = read_file(uploded_file)                    
                response=generate_evaluate_chain(
                            {
                                "text": text,
                                "number": mcq_count,
                                "subject":subject,
                                "tone": tone,
                                "response_json": json.dumps(RESPONSE_JSON)
                            }
                        )

            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Error")

                

            if isinstance(response,dict):

                        # Extract the quiz data from response
                quiz = response.get('quiz',None)
                if quiz  is not None:
                    table_data = get_table_data(quiz)
                if table_data is not None:
                    df = pd.DataFrame(table_data)
                    df.index = df.index+1
                    st.table(df)
                                # Display the review in the text box as well
                    st.text_area(label="Review",value=response["review"])
                else:
                    logging.info("Error in table Data")
                    st.error("Error in the Table Data")


            else:
                st.write(response) 