import pandas as pd
import json


class FewShotPosts:
    def __init__(self, file_path="data/processed_posts.json"):
        self.df = None
        self.unique_tags = None
        self.unique_pillars = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        with open(file_path, encoding="utf-8") as f:
            posts = json.load(f)
            self.df = pd.json_normalize(posts)

            # Apply length categorization logic
            self.df['length'] = self.df['line_count'].apply(self.categorize_length)

            # Collect all unique tags for the dropdown
            all_tags = self.df['tags'].apply(lambda x: x).sum()
            self.unique_tags = list(set(all_tags))

            # Collect unique pillars if they exist in the data
            if 'primary_pillar' in self.df.columns:
                self.unique_pillars = self.df['primary_pillar'].unique().tolist()

    def get_filtered_posts(self, length, tag):
        """
        Retrieves posts matching a specific length and technical tag.
        Removed 'language' argument since all your posts are English.
        """
        df_filtered = self.df[
            (self.df['tags'].apply(lambda tags: tag in tags)) &
            (self.df['length'] == length)
            ]
        return df_filtered.to_dict(orient='records')

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        return self.unique_tags

    def get_pillars(self):
        return self.unique_pillars


if __name__ == "__main__":
    # Simple test to verify the class works
    fs = FewShotPosts()

    # Check what pillars and tags were loaded
    print("Pillars found:", fs.get_pillars())
    print("Tags found:", fs.get_tags())

    # Example Usage: Get Medium length posts about 'Machine Learning'
    posts = fs.get_filtered_posts("Medium", "Machine Learning")
    print(f"\nExample Post found: {len(posts)}")
    if posts:
        print(posts[0]['text'][:100] + "...")