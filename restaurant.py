import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# keep temperature high for creativity
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
parser = StrOutputParser()


def generate_restaurant_name_and_items(country):
    # STRATEGY: Use "Positive Constraints"
    # Instead of "Suggest a fancy name", we ask for specific linguistic blends.
    # This forces the model to dig deeper into its vocabulary (Yoruba, Igbo, etc.)

    prompt_template_name = PromptTemplate.from_template(
        """
        I want to open a modern Nigerian restaurant in {country}.

        Generate a sophisticated restaurant name that blends a specific Nigerian word 
        (from Yoruba, Igbo, or Hausa) with a word or concept from {country}'s local language.

        Focus on themes like:
        - Specific Ingredients (e.g., Pepper, Basil, Yam)
        - Geography (Rivers, Islands, Cities)
        - Abstract Concepts (Joy, Soul, Taste)

        Return ONLY the name.
        """
    )

    # Menu prompt remains similar but ensures it matches the new fancy vibe
    prompt_template_items = PromptTemplate.from_template(
        "Suggest 5 avant-garde fusion dishes for a restaurant named '{restaurant_name}' located in {country}. "
        "Return it as a comma-separated string."
    )

    chain = (
            {"restaurant_name": prompt_template_name | llm | parser, "country": RunnablePassthrough()}
            | RunnablePassthrough.assign(menu_items=prompt_template_items | llm | parser)
    )

    return chain.invoke(country)


if __name__ == "__main__":
    result = generate_restaurant_name_and_items("China")
    print(f"--- Results for {result.get('country', 'Selected Country')} ---")
    print(f"Restaurant Name: {result['restaurant_name']}")
    print(f"Menu Items: {result['menu_items']}")