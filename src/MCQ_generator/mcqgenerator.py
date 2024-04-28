import pandas as pd
import os
import sys
from dotenv import load_dotenv 
from src.MCQ_generator.utils import read_file,get_table_data
from src.MCQ_generator.logger import logging 
from src.MCQ_generator.exception import CustomException

# Importing imp packages from langchain
 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

# Load the environment variables from the .env file
load_dotenv()

# Access the environment variables just like you would with os.environ
KEY=os.getenv("API_KEY")

## google gemini model 
llm = ChatGoogleGenerativeAI(model="gemini-pro",
                             google_api_key=KEY,
# Setting the temperature parameter to 1.0. Temperature controls the randomness of the model's responses.
                             temperature=0.8)

# Define a template string for generating a quiz
Template = """
Text:{text}
You are an expert MCQ maker.Given the about text, it is your job to\
create a quize of {number} multiple choice questions fro {subject} students in {tone} tone.
Make sure the questions are not repated and check all questions to be conforming the text as well.
Make sure to Format your Response like RESPONSE_JSON below use it as guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

try:

    quiz_generator_prompt = PromptTemplate(
        input_variables=["text","number","subject","tone","response_json"],
        template=Template
        )
except Exception as e:    
    logging.info("Error has been occurred while Setting up a PromptTemplate instance")
    raise CustomException(e,sys)

try:
    # Create an LLMChain instance for generating quizzes
    quiz_chain = LLMChain(llm=llm,
                          prompt=quiz_generator_prompt,
                    # Specify the key for accessing the output related to quizzes
                        output_key="quiz",
                    # Enable verbose mode to receive additional information during generation
                    verbose=True)
except Exception as e:
    logging.info("Error has been occurred while Setting up a LLMChain instance")
    raise CustomException(e)

Template2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

try:

    quiz_evaluation_prompt = PromptTemplate(
        input_variables=["subject","quiz"],
        template=Template2
        )
except Exception as e:    
    logging.info("Error has been occurred while Setting up a PromptTemplate instance")
    raise CustomException(e,sys)


try:
    # Create an LLMChain instance for generating quizzes
    review_chain = LLMChain(llm=llm,
                          prompt=quiz_evaluation_prompt,
                    # Specify the key for accessing the output related to quizzes
                        output_key="Review",
                    # Enable verbose mode to receive additional information during generation
                    verbose=True)
except Exception as e:
    logging.info("Error has been occurred while Setting up a Quiz LLMChain instance")
    raise CustomException(e)

try :
    # Create a SequentialChain instance to combine quiz generation and evaluation
    generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain,review_chain],
    # input for quiz chain
    input_variables=["text","number","subject","tone","response_json"],
    # output var for review chain
    output_variables=["quiz","review"]
)
    
except Exception as e:
    logging.info("Error occurred while Setting up a SequentialChain instance")
    raise CustomException(e,sys)







