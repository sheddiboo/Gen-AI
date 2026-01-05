import json
from llm_helper import llm  # Interfaces with Groq llama-3.2-90b-text-preview
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def process_posts(raw_file_path, processed_file_path=None):
    """
    Orchestrates the data pipeline: reads raw posts, enriches them with technical
    metadata, and unifies tags for a clean dataset.
    """
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        enriched_posts = []

        # Initial technical enrichment per post
        for post in posts:
            # Extract metadata like pillar and language using the LLM
            metadata = extract_metadata(post['text'])
            # Merge original dictionary with new metadata fields
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

    # Consolidate technical tags across the dataset
    # This ensures consistency by mapping specific terms to broader categories
    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:
        current_tags = post.get('tags', [])
        # Map original tags to their unified technical categories
        new_tags = {unified_tags.get(tag, tag) for tag in current_tags}
        post['tags'] = list(new_tags)

    # Write processed data to a new file
    with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
        json.dump(enriched_posts, outfile, indent=4)


def extract_metadata(post):
    """
    Analyzes a post to determine its technical pillar and structural metadata.
    """
    template = '''
    You are an expert in Data Science, Supply Chain Management (SCM), and Cloud Systems. 
    Analyze the following LinkedIn post and extract metadata.

    - Return valid JSON without any preamble or conversational text. 
    - Include these keys: "line_count" (int), "tags" (array), and "primary_pillar".
    - For "tags": Extract 2-3 technical keywords like "RAG", "Kubernetes", or "Logistics".
    - For "primary_pillar": Select the best fit from: [Data, Supply Chain, ML Systems, Cloud].

    Post content to analyze:
    {post}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"post": post})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        # Fallback to prevent script termination on a single bad parse
        raise OutputParserException("LLM output could not be parsed as JSON.")
    return res

def get_unified_tags(posts_with_metadata):
    """
    Creates a mapping to merge similar technical tags into unified categories.
    """
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post.get('tags', []))

    unique_tags_list = ', '.join(unique_tags)

    template = '''
    Unify and map these technical tags into broad professional categories.
    - Use Title Case only.
    - Follow these categorization examples:
       - "Logistics" or "Warehousing" maps to "Supply Chain"
       - "AWS", "Docker", or "K8s" maps to "Cloud Infrastructure"
       - "LLMs" or "RAG" maps to "Machine Learning"
       - "Snowflake" or "SQL" maps to "Data Engineering"
    - Output ONLY a JSON object mapping the original tag to the unified tag.

    List of tags to process: 
    {tags}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": unique_tags_list})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        # Return an empty dictionary if unification logic fails
        return {}
    return res


if __name__ == "__main__":
    # Execute the processing pipeline
    process_posts("data/raw_posts.json", "data/processed_posts.json")