# LinkedIn Post Generator

This tool analyzes a user's past LinkedIn posts to understand their unique writing style, then generates new, high-engagement posts that sound authentic to them.

![App Screenshot](UI.png)

## How It Works

Imagine an influencer who wants to maintain a consistent voice but needs help drafting content. They can feed their past data into this tool.

1.  **Select a Style:** The tool looks at past posts (e.g., "Data Engineering", "Supply Chain") to find the right "voice."
2.  **Define the Content:** The user inputs a specific topic (e.g., "Why Agentic RAG is the future").
3.  **Generate:** The tool uses **Few-Shot Learning**—picking real examples from the past history—to guide the LLM in generating a new post that matches the user's length and tone preferences.

## Technical Architecture

The project operates in two main stages:

* **Stage 1 (Data Prep):** Raw LinkedIn posts are processed to extract tags, line counts, and metadata (handled by `preprocess.py` and stored in `processed_posts.json`).
* **Stage 2 (Generation):**
    1.  The User selects a **Topic**, **Length**, and **Style Category** in the UI.
    2.  `few_shot.py` fetches the most relevant past posts.
    3.  `post_generator.py` constructs a prompt including these "Ground Truth" examples.
    4.  The **Groq LLM** (Llama 3.3) generates a new post, mimicking the sentence structure and vocabulary of the examples.

## Setup & Installation

### 1. Prerequisite: Groq API Key
This project uses the fast Groq inference engine.
* Get a free API Key here: [https://console.groq.com/keys](https://console.groq.com/keys)
* Create a file named `.env` in the root directory.
* Add your key inside it:
    ```text
    GROQ_API_KEY=your_actual_api_key_here
    ```

### 2. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt

```

### 3. Run the App

Launch the user interface with Streamlit:

```bash
streamlit run main.py

```

## Credits & Changes

**Inspiration:**
This project was inspired by the Linkedin Post generator from **Codebasics**.

**Modifications & Improvements:**

* **Architecture Refactoring:** Split the monolithic code into modular files (`main.py` for UI, `post_generator.py` for logic) for better maintainability.
* **Dynamic Topic Input:** Added a text area allowing users to define specific post topics, rather than relying solely on generic tags.
* **Language Simplification:** Removed the "Hinglish/Language" selector to focus purely on professional English content.
* **Model Upgrade:** Updated the LLM integration to use Groq's latest `llama-3.3-70b-versatile` model for higher quality output.

