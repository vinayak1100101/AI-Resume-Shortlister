import os
import fitz  # extract text from pdf
import openai
import shutil # copy files
import re # regex to extract filenames from response
import logging # logging warnings
from dotenv import load_dotenv # load environment variables 

# configuration
DATA_FOLDER = "./data" # folder containing resumes
SHORTLIST_FOLDER = "./shortlisted" # folder to save shortlisted resumes It is auto created if not exists
JOB_DESC_FILE = "job_description.txt" # job description
KEYWORDS_FILE = "keywords.txt" # keywords


# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Extracting text from pdf
def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
    except Exception as e:
        logging.error(f"Error extracting text from {pdf_path}: {e}")
        return ""

# Loading job description and keywords
def load_requirements():
    try:
        with open(JOB_DESC_FILE, 'r', encoding='utf-8') as f:
            job_description = f.read()
        with open(KEYWORDS_FILE, 'r', encoding='utf-8') as f:
            keywords = [line.strip() for line in f if line.strip()]
        return job_description, keywords
    except Exception as e:
        logging.error(f"Error loading requirements: {e}")
        return "", []

# Building prompt for LLM
def build_prompt(job_desc, keywords, resumes):
    keyword_str = ', '.join(keywords)
    prompt = f"""
I need to shortlist resumes based on the following job description and required skills.

Job Description:
{job_desc}

Required Skills/Keywords:
{keyword_str}

Each resume is labeled by its filename.

Here are the resumes:
"""
    for filename, content in resumes.items():
        prompt += f"\nResume: {filename}\nContent:\n{content[:3000]}\n---\n"

    prompt += """
Instructions:
- Evaluate each resume using the job description and keywords.
- Score each resume out of 100 based on relevance, experience, and education.
- Return a list of shortlisted resumes (score >= 80) and rejected ones with reasons.
- Sort shortlisted resumes by score descending.

Return format:

Shortlisted:
1. Filename: <filename.pdf>
   Score: <score>
   Summary: <short reason>

Rejected:
1. Filename: <filename.pdf>
   Reason: <short reason>
   Score: <score>
"""
    return prompt

# Calling OpenAI API
def analyze_resumes(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert HR assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        return ""

# Parsing and saving PDFs
def parse_and_save(response_text):
    if os.path.exists(SHORTLIST_FOLDER):
        shutil.rmtree(SHORTLIST_FOLDER)
    os.makedirs(SHORTLIST_FOLDER)

    # Extract shortlisted filenames
    shortlisted = re.findall(r'Filename:\s*(.*\.pdf)', response_text)
    shortlisted = [filename.strip() for filename in shortlisted]

    print("\n📄 Shortlisted Resumes:\n")
    for i, filename in enumerate(shortlisted, 1):
        src_path = os.path.join(DATA_FOLDER, filename)
        if os.path.exists(src_path):
            dst_filename = f"{i:02d}_{filename.replace(' ', '_')}"
            dst_path = os.path.join(SHORTLIST_FOLDER, dst_filename)
            shutil.copy(src_path, dst_path)
            print(f"✔ {filename} → saved as {dst_filename}")
        else:
            logging.warning(f"File not found: {filename}")

# Main function
def main():
    resumes = {}
    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".pdf"):
            path = os.path.join(DATA_FOLDER, file)
            resumes[file] = extract_text_from_pdf(path)

    if not resumes:
        logging.warning("No PDF resumes found in the data folder.")
        return

    job_desc, keywords = load_requirements()
    prompt = build_prompt(job_desc, keywords, resumes)
    result = analyze_resumes(prompt)

    print("\n Response from GPT \n")
    print(result)

    parse_and_save(result)

if __name__ == "__main__":
    main()
