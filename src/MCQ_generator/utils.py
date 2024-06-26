import os 
import sys
from src.MCQ_generator.exception import CustomException
from src.MCQ_generator.logger import logging
import json
import PyPDF2
import base64 
import streamlit as st 
import traceback

def read_file(file):
    """
    Reads text from a file.

    Args:
    - file: A file object
    
    Returns:
    - text: Extracted text from the file
    """

    if file.name.endswith('.pdf'):
        try:
            # If the file is a PDF, use PyPDF2 to extract text from each page
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        
        except Exception as e:
            logging.info("Error occurred while reading the file")
            raise CustomException(e,sys)

    elif file.name.endswith('.txt'):
        # If the file is a text file, read its contents
        return file.read().decode('utf-8')
    
    else:
        raise CustomException(e,sys)
    




import json
import traceback

def get_table_data(quiz_str):
    """
    Extracts table data from a quiz string.
    
    Args:
    - quiz_str (str): A string representing the quiz in JSON format
    
    Returns:
    - list: A list of dictionaries containing table data for each MCQ
    """
    try:
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        for key, value in quiz_dict.items():
            mcq = value.get("mcq", "")
            options = " || ".join([
                f"{option}-> {option_value}" for option, option_value in value.get("options", {}).items()
            ])
            correct = value.get("correct", "")
            quiz_table_data.append({
                "MCQ": mcq,
                "Choice": options,
                "Correct": correct
            })
        
        return quiz_table_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


    
