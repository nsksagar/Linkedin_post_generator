# LinkedIn Post Generator

## Overview
A Streamlit web application that generates personalized LinkedIn posts using LLMs and few-shot learning. Given a set of LinkedIn posts from a specific person, the app learns their writing style and generates new posts on any topic, in any length, and in any language — mimicking that person's voice.

---

## How It Works

### 1. Data Collection
Collect raw LinkedIn posts from the person whose style you want to replicate and store them in `Data/Raw_posts.json`.

### 2. Preprocessing (`preprocess.py`)
Each raw post goes through metadata extraction using an LLM:
- **line_count** — number of lines in the post
- **language** — English or Hinglish
- **tags** — up to 2 topic tags (e.g. Job Search, Motivation)

Tags across all posts are then unified using the LLM — similar tags like "Job Hunting", "Jobseekers" get merged into one canonical tag like "Job Search". The enriched posts are saved to `Data/processed_posts.json`.

### 3. Few-Shot Learning (`few_shots.py`)
When generating a post, the app retrieves the most relevant examples from the processed posts that match the selected topic, length, and language. These examples are injected into the prompt so the LLM learns the writing style on the fly — this is few-shot learning.

### 4. Post Generation (`post_generater.py`)
The prompt is constructed with:
- The desired topic
- The desired length
- The desired language
- Up to 2 example posts matching those filters (few-shot examples)

The LLM then generates a new post that matches both the topic requirements and the writing style of the person.

### 5. Streamlit UI (`main.py`)
A simple 3-column web interface where the user selects:
- **Topic** — dropdown populated from all unique tags extracted from the posts
- **Length** — Short (1–5 lines), Medium (6–10 lines), Long (11–15 lines)
- **Language** — English or Hinglish

Clicking **Generate** produces a LinkedIn post.

---

## Project Structure
```
Linkedin_post_generator/
│
├── Data/
│   ├── Raw_posts.json           # Raw LinkedIn posts input
│   └── processed_posts.json     # Enriched posts with metadata
│
├── preprocess.py                # Extracts metadata and unifies tags
├── few_shots.py                 # Filters and retrieves few-shot examples
├── post_generater.py            # Builds prompt and generates post via LLM
├── llm_helper.py                # Initializes the LLM (Groq + LangChain)
├── main.py                      # Streamlit UI
├── .env                         # API keys (not committed to git)
└── requirements.txt
```

---

## Tech Stack
- **LLM** — Llama 3.1 8B via Groq API
- **LangChain** — Prompt templates, chains, output parsing
- **Streamlit** — Web UI
- **Pandas** — Post filtering and metadata management
- **Python** — Core language

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/Linkedin_post_generator.git
cd Linkedin_post_generator
```

### 2. Create and activate virtual environment
```bash
conda create -n linkedenv python=3.12
conda activate linkedenv
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
```
API_KEY=your_groq_api_key_here
```

### 5. Add your raw posts
Populate `Data/Raw_posts.json` with LinkedIn posts in this format:
```json
[
  {
    "text": "Your LinkedIn post text here..."
  }
]
```

### 6. Run preprocessing
```bash
python3 preprocess.py
```
This generates `Data/processed_posts.json`.

### 7. Run the app
```bash
streamlit run main.py
```

---

## Key Concepts

### Few-Shot Learning
Instead of fine-tuning the model, we inject real examples of the target person's posts directly into the prompt. The LLM uses these examples to understand and replicate the writing style without any training.

### Tag Unification
Raw tags extracted from posts can be inconsistent — "Job Hunting", "Jobseekers", "Job Tips" all mean roughly the same thing. The LLM unifies these into a canonical set of tags, keeping the topic dropdown clean and useful.

### Hinglish Support
Hinglish is a mix of Hindi and English commonly used in Indian LinkedIn posts. The app supports generating posts in Hinglish while keeping the script in English characters.

---

## Notes
- Raw posts may contain corrupted emoji characters (unicode surrogates). The app handles this automatically by stripping them during preprocessing and loading.
- The app uses a maximum of 2 few-shot examples per generation to stay within token limits.
- Currently supports Groq's `llama-3.1-8b-instant` model. You can swap this in `llm_helper.py`.