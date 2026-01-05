from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()

def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"
    return "6 to 10 lines"

def generate_post(length, tag, topic):
    """
    Main function to generate the post.
    Args:
        length (str): Short, Medium, or Long.
        tag (str): The style category (e.g., "Machine Learning").
        topic (str): The actual content you want to write about.
    """
    prompt = get_prompt(length, tag, topic)
    response = llm.invoke(prompt)
    return response.content

def get_prompt(length, tag, topic):
    length_str = get_length_str(length)

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {topic}
    2) Length: {length_str}
    3) Style Context: The post should be relevant to {tag} professionals.
    '''

    # Fetch examples based on length and tag (Style)
    examples = few_shot.get_filtered_posts(length, tag)

    if len(examples) > 0:
        prompt += "\n4) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\n Example {i+1}: \n\n {post_text}'

        if i == 1: # Use max two samples to keep the prompt focused
            break

    return prompt

if __name__ == "__main__":
    # Test run
    print(generate_post("Medium", "Machine Learning", "Why Agentic RAG is the future"))