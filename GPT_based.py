
import openai
import os
import json
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
import pandas as pd

# Set environment variables for OpenAI API

os.environ["OΡΕΝΑΙ_API_TYPE"] = 'Your_Open_AI_Type'
os.environ["OPENAI_API_VERSION"] = 'Your_Open_AI_Version'
os.environ["AZURE_OPENAI_ENDPOINT"]= 'Your_Azure_Open_AI_Endpoint'
os.environ['AZURE_OPENAI_API_KEY']= 'Your_Open_AI_API_Key'

# Initialize the LLM
llm = AzureChatOpenAI(
    deployment_name="gpt-4o",
    temperature=0,
    max_tokens=4000,
    openai_api_version="2024-06-01",
)

departments = [
    "Administrative Reforms and PG", 
    "Agriculture and Cooperation", 
    "Agriculture Research and Education", 
    "Animal Husbandry, Dairying", 
    "Atomic Energy", 
    "Ayush", 
    "Bio Technology", 
    "Central Board of Direct Taxes (Income Tax)", 
    "Central Board of Excise and Customs", 
    "Chemicals and Petrochemicals", 
    "Civil Aviation", 
    "Coal", 
    "Commerce", 
    "Consumer Affairs", 
    "Corporate Affairs", 
    "Culture", 
    "Defence", 
    "Defence Finance", 
    "Defence Production", 
    "Defence Research and Development", 
    "Development of North Eastern Region", 
    "Drinking Water and Sanitation", 
    "Earth Sciences", 
    "Economic Affairs", 
    "Electronics & Information Technology", 
    "Empowerment of Persons with Disabilities", 
    "Environment, Forest and Climate Change", 
    "Ex Servicemen Welfare", 
    "Expenditure", 
    "External Affairs", 
    "Fertilizers", 
    "Financial Services (Banking Division)", 
    "Financial Services (Insurance Division)", 
    "Financial Services (Pension Reforms)", 
    "Fisheries", 
    "Food and Public Distribution", 
    "Food Processing Industries", 
    "Health & Family Welfare", 
    "Health Research", 
    "Heavy Industry", 
    "Higher Education", 
    "Home Affairs", 
    "Housing and Urban Affairs", 
    "Industrial Policy & Promotion", 
    "Information and Broadcasting", 
    "Investment & Public Asset Management", 
    "Justice", 
    "Labour and Employment", 
    "Land Resources", 
    "Legal Affairs", 
    "Legislative Department", 
    "Micro Small and Medium Enterprises", 
    "Mines", 
    "Minority Affairs", 
    "New and Renewable Energy", 
    "NITI Aayog", 
    "O/o the Comptroller & Auditor General of India", 
    "Official Language", 
    "Panchayati Raj", 
    "Parliamentary Affairs", 
    "Personnel and Training", 
    "Petroleum and Natural Gas", 
    "Pharmaceutical", 
    "Posts", 
    "Power", 
    "Public Enterprises", 
    "Railways, ( Railway Board)", 
    "Revenue", 
    "Road Transport and Highways", 
    "Rural Development", 
    "School Education and Literacy", 
    "Science and Technology", 
    "Scientific & Industrial Research", 
    "Shipping", 
    "Skill Development and Entrepreneurship", 
    "Social Justice and Empowerment", 
    "Space", 
    "Sports", 
    "Statistics and Programme Implementation", 
    "Steel", 
    "Telecommunications", 
    "Textiles", 
    "Tourism", 
    "Tribal Affairs", 
    "Unique Identification Authority of India", 
    "Water Resources, River Development & Ganga Rejuvenation", 
    "Women and Child Development"
]

# Define the prompt template for grievance filing
prompt_1="Using the following Departments {context}, For a given Grievances {question}, find the name of the most correct matched dapatment. Give output in structured json.\n {format_instructions}. If the department is unclear or the question is not in the type of Grienvance then return 'Uncategorized' for that Grienvance. Strict to the context"

# Define summary model for parsing LLM output
class Summary(BaseModel):
    Grievance: str = Field(description="Give me the Grievances text")
    Department: str = Field(description="Give me the category of grievances")
    Message: str = Field(description="Grievance filed successfully! But for 'Uncategorized' departments, the message is 'Ask the right Grievance'.")

class SummaryModel(BaseModel):
    summary: List[Summary]

# Setup JSON output parser
parser = JsonOutputParser(pydantic_object=SummaryModel)

# Create the prompt template for the chain
prompt = PromptTemplate(
    template=prompt_1,
    input_variables=["context", "question"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# Define the chain
chain = prompt | llm | parser

# Streamlit UI Setup
st.title("Grievance Filing System")
st.markdown("### Welcome! You can file grievances and get responses in real-time. You can ask multiple questions.")

# Create a session state to store conversations
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Create input field for the grievance
grievance_text = st.text_area("Enter your Grievance (English/Hindi):", "", height=200)

# Function to process the grievance and get response
def process_grievance(grievance_text):
    result = chain.invoke({"context": departments, "question": grievance_text})
    return result

# Handle form submission
if st.button("Submit Grievance"):
    if grievance_text:
        response_txt = process_grievance(grievance_text)
        
        # Save the grievance and the response to the conversation history
        st.session_state.conversation.append({
            'grievance': grievance_text,
            'response': response_txt
        })
        
        # Display responses in a readable format
        st.subheader("Grievance:")
        st.write(grievance_text)
        st.subheader("Response:")
        st.json(response_txt)
        # df = pd.DataFrame.from_dict(response_txt, orient="index", columns=["Value"]).reset_index()
        # df.columns = ["Key", "Value"]
        # st.table(df)
    else:
        st.warning("Please enter a grievance before submitting.")

# Show the conversation history in the UI
st.markdown("### Conversation History")
if st.session_state.conversation[:-1]:
    for i, item in enumerate(st.session_state.conversation[:-1]):
        st.subheader(f"Grievance {i+1}:")
        st.write(item['grievance'])
        st.subheader(f"Response {i+1}:")
        st.json(item['response'])
        # df = pd.DataFrame.from_dict(item['response'], orient="index", columns=["Value"]).reset_index()
        # df.columns = ["Key", "Value"]
        # st.table(df)
else:
    st.write("No grievances filed yet.")
