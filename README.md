# 🧠 Generative AI & LLM Projects

Welcome to my collection of Generative AI projects! This repository documents my journey building applications using **Large Language Models (LLMs)**, **LangChain**, **Vector Databases**, and **Python**.

Each folder contains a standalone project demonstrating a specific use case of GenAI, ranging from simple prompt chains to complex database agents.

---

## 📂 Project Overview

### 1. 👕 T-Shirt Store: Talk to a Database (`/tshirt_sales`)
A Text-to-SQL application that allows users to query a MySQL database using natural language.
* **Goal:** Enable store managers to ask questions like *"How much revenue if we sell all Nike shirts?"* without writing SQL.
* **Tech Stack:** Groq (Llama 3), LangChain, TiDB (MySQL), ChromaDB (Few-Shot Learning), Streamlit.
* **Key Features:**
    * Translates English to SQL dynamically.
    * Uses "Few-Shot Learning" to understand context.
    * Handles complex joins and logic automatically.
    

### 2. 📰 News Research Tool (`/news_research_project`)
A Retrieval Augmented Generation (RAG) tool designed to analyze and query news articles.
* **Goal:** Aggregate news data and allow users to ask specific questions based on the content of those articles.
* **Tech Stack:** LangChain, Vector Stores (FAISS/Chroma), LLMs.
* **Key Features:**
    * Loads and processes text from URLs or documents.
    * Uses embeddings to retrieve relevant answers accurately.

### 3. 🍽️ Restaurant Name Generator (`/restaurant`)
A creative generation project demonstrating the basics of Prompt Templates.
* **Goal:** Generate unique restaurant names and menu items based on a specific cuisine type.
* **Tech Stack:** LangChain, Sequential Chains.
* **Key Features:** Simple demonstration of chaining multiple LLM calls together (Cuisine -> Name -> Menu).

### 4. 📚 LangChain Fundamentals (`langchain_fundamentals.ipynb`)
A Jupyter Notebook covering the core building blocks of the LangChain framework.
* **Topics Covered:**
    * Prompt Templates & Chains.
    * Simple Sequential Chains.
    * Memory Buffers (Conversation History).

---

## 🛠️ General Tech Stack

* **Languages:** Python 🐍
* **Frameworks:** LangChain, Streamlit, Jupyter
* **Models (LLMs):** Groq (Llama 3), Google Palm, OpenAI (varies by project)
* **Databases:** MySQL (TiDB), ChromaDB, FAISS

---

## 🚀 Getting Started

To run a specific project, navigate to its folder and follow the instructions in its local `README.md`.

**Example: Running the T-Shirt Store App**
```bash
# 1. Navigate to the project folder
cd tshirt_sales

# 2. Install specific requirements
pip install -r requirements.txt

# 3. Run the app
streamlit run main.py