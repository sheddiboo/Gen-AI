import os
import streamlit as st
import pickle
import time
import torch  # We need this to handle a memory loading bug in some torch versions
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# --- Setup & Configuration ---
# Let's get our API keys and setup the basic app look
load_dotenv()

st.set_page_config(page_title="News Research Tool", page_icon="📈")
st.title("News Research Tool 📈")
st.sidebar.title("News Article URLs")

# Sidebar for URL inputs
urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i + 1}")
    urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")
file_path = "vector_index.pkl"

# A place to show updates while the code works
main_placeholder = st.empty()

# --- Initialize AI Models ---
# Using Groq (Llama 3) for the thinking part because it's incredibly fast
llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.5)

# We force the embedding model to load on the CPU.
# This fixes the "meta tensor" error you saw earlier.
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

# --- Data Processing Logic ---
if process_url_clicked:
    # First, let's scrape the websites
    main_placeholder.text("Data Loading...Started...✅✅✅")
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()

    # Now we chop the text into 1000-character chunks
    # This keeps things small enough for the AI to "digest"
    main_placeholder.text("Text Splitter...Started...✅✅✅")
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000
    )
    docs = text_splitter.split_documents(data)

    # We turn those text chunks into mathematical vectors (embeddings)
    # and store them in a FAISS searchable database
    main_placeholder.text("Embedding Vector Started Building...✅✅✅")
    vectorstore = FAISS.from_documents(docs, embeddings)
    time.sleep(2)

    # Save the database to a file so we don't have to re-scrape later
    with open(file_path, "wb") as f:
        pickle.dump(vectorstore, f)

    main_placeholder.success("Processing Complete! Ask your question below.")

# --- Question & Answering (RAG) ---
query = st.text_input("Question: ")

if query:
    if os.path.exists(file_path):
        # Reload the brain from the pickle file
        with open(file_path, "rb") as f:
            vectorstore = pickle.load(f)

            # Define how we fetch relevant data (top 2 results)
            retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

            # Create the instructions for the AI
            template = """
            You are a helpful assistant. Answer the question based ONLY on the following context.
            If you don't know the answer, just say "I don't know".

            Context:
            {context}

            Question: {question}
            """
            prompt = ChatPromptTemplate.from_template(template)

            # Glue chunks together into one string
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)

            # The modern LCEL "Pipe" pipeline
            rag_chain = (
                    {"context": retriever | format_docs, "question": RunnablePassthrough()}
                    | prompt
                    | llm
                    | StrOutputParser()
            )

            # Get and display the answer
            result = rag_chain.invoke(query)
            st.header("Answer")
            st.write(result)

            # List the sources we used for transparency
            relevant_docs = retriever.invoke(query)
            st.subheader("Sources:")
            for doc in relevant_docs:
                st.write(f"- {doc.metadata.get('source', 'Unknown Source')}")

    else:
        st.error(f"Vector Store not found. Please click 'Process URLs' first.")