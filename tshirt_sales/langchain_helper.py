import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from sqlalchemy import create_engine

# Import the training examples from our separate file(few_shots.py)
from few_shots import few_shots

# Load secret keys (like DB passwords and API keys) from the .env file
load_dotenv()


def get_few_shot_db_chain():
    """
    This function sets up the entire AI pipeline:
    1. Connects to the database.
    2. Sets up the 'Few-Shot' learning (finding similar past examples).
    3. Creates the strict prompt templates.
    4. Returns the executable chain.
    """

    # --- 1. Connect to Database (TiDB) ---
    # We grab credentials from the environment to keep them secure
    db_user = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_DATABASE")
    db_port = os.getenv("DB_PORT")

    # Build the connection string and create the engine
    db_uri = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(db_uri, pool_pre_ping=True, pool_recycle=300)

    # We load sample rows so the AI understands what the data looks like
    db = SQLDatabase(engine, sample_rows_in_table_info=3)

    # --- 2. Initialize the LLM ---
    # We use Groq with Llama 3.
    # Important: Temperature is set to 0. We want the AI to be precise (mathematical), not creative.
    llm = ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=os.getenv("GROQ_API_KEY"), temperature=0)

    # --- 3. Setup 'Few-Shot' Learning ---
    # This part allows the AI to find similar questions we've answered before.
    # We use HuggingFace to turn text into numbers (embeddings).
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    # Store our 'few_shots' examples in a vector database so we can search them
    to_vectorize = [" ".join(example.values()) for example in few_shots]
    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)

    # This selector will find the top 2 examples most similar to the user's new question
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=2,
    )

    # --- 4. Define the Prompts ---
    # This is the instruction manual for the AI. We are very strict here:
    # "No Markdown" and "Don't repeat the SQL code in the final answer."
    mysql_prompt = """You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run.
    IMPORTANT: Return ONLY the raw SQL code in the SQLQuery section. Do NOT use markdown.
    IMPORTANT: In the Answer section, do NOT repeat the SQL code. Only output the final natural language sentence.

    Format:
    Question: {input}
    SQLQuery: Raw SQL query without formatting
    SQLResult: Result of the SQLQuery
    Answer: Final natural language response
    """

    PROMPT_SUFFIX = "Only use these tables: {table_info}\nQuestion: {input}"

    # Template for how the examples should look
    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )

    # Combine everything: The instructions + The similar examples + The user's new question
    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"],
    )

    # --- 5. Create the Chain ---
    # This links the LLM, the Database, and our Prompt together.
    # return_intermediate_steps=True is crucial! It lets us see the SQL code in main.py.
    chain = SQLDatabaseChain.from_llm(
        llm,
        db,
        verbose=False,
        prompt=few_shot_prompt,
        return_intermediate_steps=True
    )

    return chain