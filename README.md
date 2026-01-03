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
* **Key Features:** Chaining multiple LLM calls together (Cuisine -> Name -> Menu).

### 4. 📚 LangChain Fundamentals (`langchain_fundamentals.ipynb`)
A Jupyter Notebook covering the core building blocks of the LangChain framework.
* **Topics:** Prompt Templates, Simple Sequential Chains, and Memory Buffers.

### 5. 🔬 LLM Fine-Tuning & Reasoning (`/llm_fine_tuning`)
Experimental notebooks focused on model optimization and advanced reasoning capabilities.
* **Unsloth Fine-Tuning:** Uses the Unsloth framework to fine-tune Llama-3.2-3B for "DeepSeek-R1 style" reasoning. 
* **Optimized Learning:** Utilizes QLoRA for 2x faster training and massive VRAM savings.
* **Quantization Basics:** Covers the fundamentals of reducing model precision (INT8/NF4) to make LLMs run efficiently on consumer hardware.

[Image of QLoRA architecture showing 4-bit frozen base weights and 16-bit trainable adapters]

### 6. 🔌 Model Context Protocol (MCP) Server (`/my-first-mcp-server`)
A project exploring **MCP**, an open standard for connecting AI assistants to external data and tools.
* **Goal:** Standardize how LLMs communicate with data sources (databases, APIs, files) to reduce hallucinations and increase automation.
* **Setup:** A custom server built using Python to provide external context to an LLM host.

---

## 🏗️ Directory Structure

```text
gen_ai/
├── tshirt_sales/            # Text-to-SQL database agent
├── news_research_project/   # RAG application for news articles
├── restaurant/              # Multi-chain creative generator
├── llm_fine_tuning/         # Unsloth/QLoRA & Quantization notebooks
│   ├── quantization_basics.ipynb
│   └── unsloth_finetuning.ipynb
├── my-first-mcp-server/     # MCP server implementation for external context
├── langchain_fundamentals.ipynb  # Learning path for core framework concepts
└── README.md                # Project documentation (this file)