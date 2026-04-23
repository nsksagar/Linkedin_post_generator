
import json

def process_posts(raw_file_path, processed_file_path = None):   

    enriched_posts = []
    
    with open(raw_file_path, encoding = 'utf-8') as file:
        posts = json.load(file)
        
        for post in posts:
            metadata = extract_metadata(post['text'])

            post_with_metadata = post | metadata

            enriched_posts.append(post_with_metadata)

    for epost in enriched_posts:
        pass

def extract_metadata(texts):
    pass

if __name__ == '__main__':

    raw_file_path = 'data/raw_posts.json'
    processed_file_path = 'data/processed_posts.json'
    process_posts(raw_file_path, processed_file_path)
