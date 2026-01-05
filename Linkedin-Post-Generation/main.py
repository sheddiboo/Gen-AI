import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post  # Corrected import

# Options for length
length_options = ["Short", "Medium", "Long"]


def main():
    st.set_page_config(page_title="LinkedIn Post Generator", layout="centered")
    st.subheader("LinkedIn Post Generator")

    # Text Input: The actual subject you want to write about
    post_topic = st.text_area("What should the post be about?",
                              placeholder="e.g., Why Agentic RAG is the future of Supply Chain...",
                              height=100)

    # Dropdowns: Style (Tag) and Length
    col1, col2 = st.columns(2)

    fs = FewShotPosts()
    tags = fs.get_tags()

    with col1:
        # The Tag determines which past posts are used as style examples
        selected_tag = st.selectbox("Style Category", options=tags)

    with col2:
        selected_length = st.selectbox("Length", options=length_options)

    # Generate Button
    if st.button("Generate Post", type="primary"):
        if not post_topic.strip():
            st.error("Please enter a topic to generate a post.")
        else:
            with st.spinner("Analyzing your style and generating text..."):
                try:
                    # Corrected function call: matches generate_post(length, tag, topic)
                    post = generate_post(selected_length, selected_tag, post_topic)

                    st.success("Post Generated!")
                    st.markdown("---")
                    st.write(post)
                except Exception as e:
                    st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()