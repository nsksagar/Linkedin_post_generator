import json


class FewShotPosts:

    def __init__(self, file_path = 'Data/processed_posts.json'):

        self.df = None 
        self.unique_tags = None 

    def load_posts(self, file_path):

        with open(file_path, encoding = 'utf-8') as f:

            posts = json.load(f)