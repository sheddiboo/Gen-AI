import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Look in the parent directory for the .env file
load_dotenv("../.env")

# Initialize LLM with the supported model
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)