import streamlit as st
import re
from langchain_helper import get_few_shot_db_chain

st.title("T Shirts Database Q&A 👕")

question = st.text_input("Question: ")

if question:
    chain = get_few_shot_db_chain()

    with st.spinner('Thinking...'):
        try:
            # 1. Execute the chain
            response = chain.invoke(question)

            # 2. Extract internal execution steps
            steps = response.get('intermediate_steps', [])
            sql_code = "N/A"
            db_result = "N/A"

            if isinstance(steps, list) and len(steps) > 1:
                sql_code = steps[1]
                for step in steps:
                    if isinstance(step, str) and (step.startswith("[(") or step.startswith("[")):
                        db_result = step

            # 3. Process the final text response
            final_answer = response['result']
            final_answer = final_answer.split("SQLQuery:")[-1].split("Answer:")[-1].strip()

            # 4. Fallback Logic: If the AI failed to write English (gave raw SQL)
            if "SELECT" in final_answer.upper():
                if db_result != "N/A":
                    # Extract the clean number
                    clean_number = re.sub(r"[^\d.]", "", db_result)

                    # LOGIC: Make it sound natural
                    # If it has a decimal point (like 2805.50), treat it as Revenue/Money
                    if "." in clean_number:
                        final_answer = f"The total amount is ${clean_number}."
                    # If it is just digits (like 310), treat it as a Count/Quantity
                    else:
                        final_answer = f"The total count is {clean_number} items."
                else:
                    final_answer = "I found a result in the database, but couldn't put it into a sentence."

            # 5. Display Output
            st.header("Answer")
            st.write(final_answer)

            with st.expander("View Generated SQL Query"):
                st.code(sql_code, language='sql')
                st.write(f"Raw Database Output: {db_result}")

        except Exception as e:
            st.error(f"An error occurred: {e}")