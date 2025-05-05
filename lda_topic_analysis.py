import os
import json
import re
import jieba
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import glob

# --- Configuration ---
COMMENT_DIRS = [
    '/home/user/YunTech2025/schoolProject/xxSearchCrawler/output_comments/momo',
    '/home/user/YunTech2025/schoolProject/xxSearchCrawler/output_comments/pchome'
]
STOPWORDS_PATH = '/home/user/YunTech2025/meatballSpaghetii/integration/resource/stopwords (1).txt'
NUM_TOPICS = 5  # You can adjust the number of topics
N_TOP_WORDS = 15 # Number of top words to display per topic

# --- Functions ---

def load_stopwords(filepath):
    """Loads stopwords from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            stopwords = {line.strip() for line in f}
        # Add common single characters/symbols often left after cleaning
        stopwords.update([' ', '\\n', '\\r', '\\t', '：', '(', ')', '！', '。', '，', '；', '？', '[', ']', '{', '}'])
        return stopwords
    except FileNotFoundError:
        print(f"Warning: Stopwords file not found at {filepath}. Proceeding without custom stopwords.")
        return set([' ', '\\n', '\\r', '\\t', '：', '(', ')', '！', '。', '，', '；', '？', '[', ']', '{', '}']) # Basic stopwords

def load_comments_from_dirs(directories):
    """Loads comments from JSON files in specified directories, handling nested comment objects."""
    all_comments = []
    files_with_comments = 0
    comments_found_count = 0 # Total comments found across all files
    for directory in directories:
        json_files = glob.glob(os.path.join(directory, '*.json'))
        print(f"Found {len(json_files)} JSON files in {directory}")
        for file_path in json_files:
            comments_in_current_file = 0 # Reset for each file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Ensure the loaded data is a list
                    if not isinstance(data, list):
                        print(f"Warning: Expected a list in {file_path}, but got {type(data)}. Skipping file.")
                        continue
                    for item in data:
                        # Check if '評論' key exists and is a non-empty list
                        if isinstance(item, dict) and '評論' in item and isinstance(item['評論'], list):
                            # Iterate through the list of comment objects
                            for comment_obj in item['評論']:
                                # Check if the element is a dict and has the inner '評論' key
                                if isinstance(comment_obj, dict) and '評論' in comment_obj:
                                    comment_text = comment_obj['評論']
                                    # Add only non-empty string comments
                                    if isinstance(comment_text, str) and comment_text.strip():
                                        all_comments.append(comment_text)
                                        comments_in_current_file += 1
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {file_path}")
            except Exception as e:
                print(f"Warning: Error processing file {file_path}: {e}")

            if comments_in_current_file > 0:
                files_with_comments += 1
                comments_found_count += comments_in_current_file
                # Optional: Uncomment the line below for very detailed logging
                # print(f"Debug: Found {comments_in_current_file} comments in {file_path}")

    print(f"Found non-empty comment lists in {files_with_comments} files.")
    print(f"Loaded {len(all_comments)} comments in total (Total count from lists: {comments_found_count}).") # Use len(all_comments) for actual loaded count
    return all_comments

def preprocess_text(text, stopwords):
    """Cleans, segments, and removes stopwords from text."""
    # Remove punctuation, numbers, and non-Chinese characters (optional, adjust regex as needed)
    text = re.sub(r"[^\u4e00-\u9fa5]", "", text)
    # Segment text using jieba
    words = jieba.cut(text)
    # Remove stopwords and single characters
    filtered_words = [word for word in words if word not in stopwords and len(word) > 1]
    return " ".join(filtered_words) # Return space-separated string for Vectorizer

def display_topics(model, feature_names, n_top_words):
    """Displays the top words for each topic."""
    for topic_idx, topic in enumerate(model.components_):
        print(f"Topic #{topic_idx + 1}:")
        top_words_indices = topic.argsort()[:-n_top_words - 1:-1]
        top_words = [feature_names[i] for i in top_words_indices]
        print(" ".join(top_words))
        print("-" * 20)

# --- Main Execution ---
if __name__ == "__main__":
    print("Loading stopwords...")
    stopwords = load_stopwords(STOPWORDS_PATH)
    # Add custom dictionary if needed (example from your run.py context)
    # jieba.load_userdict('/home/user/YunTech2025/meatballSpaghetii/integration/resource/dict (1).txt') # Uncomment if needed

    print("Loading comments...")
    comments = load_comments_from_dirs(COMMENT_DIRS)

    if not comments:
        print("No comments found or loaded. Exiting.")
    else:
        print("Preprocessing comments...")
        processed_comments = [preprocess_text(comment, stopwords) for comment in comments if comment] # Ensure comment is not None or empty
        # Filter out any documents that became empty after preprocessing
        processed_comments = [doc for doc in processed_comments if doc.strip()]

        if not processed_comments:
             print("All comments became empty after preprocessing. Cannot perform LDA. Check stopwords or cleaning steps.")
        else:
            print(f"Preprocessing complete. {len(processed_comments)} documents remaining.")
            print("Creating document-term matrix...")
            # Use CountVectorizer for LDA
            vectorizer = CountVectorizer(max_df=0.95, min_df=2) # Ignore terms that appear in >95% or <2 documents
            dtm = vectorizer.fit_transform(processed_comments)
            feature_names = vectorizer.get_feature_names_out()
            print(f"Document-Term Matrix shape: {dtm.shape}")

            if dtm.shape[1] == 0:
                print("No features found after vectorization. Cannot perform LDA. Check preprocessing/vectorizer settings.")
            else:
                print(f"Training LDA model with {NUM_TOPICS} topics...")
                lda = LatentDirichletAllocation(n_components=NUM_TOPICS, random_state=42, learning_method='batch', max_iter=10)
                lda.fit(dtm)

                print("\n--- LDA Topic Analysis Results ---")
                display_topics(lda, feature_names, N_TOP_WORDS)
                print("---------------------------------")
                print("LDA analysis complete.")

                # Optional: Assign topics to documents
                # doc_topic_dist = lda.transform(dtm)
                # doc_dominant_topic = doc_topic_dist.argmax(axis=1)
                # print("\nDominant topic for first 10 documents:")
                # print(doc_dominant_topic[:10])

# Note: You might need to install scikit-learn and jieba if you haven't already:
# pip install scikit-learn jieba pandas
