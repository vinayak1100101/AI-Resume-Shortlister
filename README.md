AI Resume Shortlister
This project provides a Python script that automates the process of screening and shortlisting resumes. It uses the OpenAI API (specifically gpt-4o-mini) to analyze a folder of PDF resumes against a given job description and a list of keywords. The script then identifies the most suitable candidates and copies their resumes into a "shortlisted" folder.

Features
Automated Resume Parsing: Extracts text content directly from PDF files.

AI-Powered Analysis: Leverages a Large Language Model to score and evaluate resumes based on relevance, experience, and skills.

Customizable Criteria: Easily define the screening criteria by editing the job_description.txt and keywords.txt files.

Organized Output: Automatically creates a shortlisted folder and copies the resumes of the top candidates for easy access.

Detailed Reporting: Prints a detailed analysis from the AI, including scores and reasons for shortlisting or rejection.

How It Works
Load Inputs: The script reads the job description, a list of keywords, and all PDF resumes from their respective files and folders.

Extract Text: It iterates through each PDF in the ./data folder and extracts its raw text content.

Build Prompt: A comprehensive prompt is constructed for the AI, containing the job description, keywords, and the extracted text from all resumes.

Analyze with AI: The prompt is sent to the OpenAI API. The AI evaluates each resume, assigns a score out of 100, and provides a summary for its decision.

Parse & Save: The script parses the AI's response to identify the filenames of the shortlisted candidates.

Organize Files: It creates a ./shortlisted directory and copies the original PDF files of the successful candidates into it, prefixing them with a number for ranking.

Setup and Usage
Prerequisites
Python 3.7+

An OpenAI API Key

1. Clone the Repository
git clone https://github.com/vinayak1100101/AI-Resume-Shortlister
cd AI-Resume-Shortlister

2. Install Dependencies
The script requires a few Python libraries. You can install them using pip. It's recommended to use a virtual environment.

pip install pymupdf openai python-dotenv

Or, create a requirements.txt file with the following content:

PyMuPDF
openai
python-dotenv

And run:

pip install -r requirements.txt

3. Configure the Project
Set API Key: Create a file named .env in the root directory and add your OpenAI API key to it:

OPENAI_API_KEY="your_openai_api_key_here"

Add Resumes: Place all the candidate resumes (in .pdf format) into the data folder.

Define Job Description: Open job_description.txt and paste the full job description for the role you are hiring for.

List Keywords: Open keywords.txt and add the essential skills, technologies, or qualifications you are looking for. Add one keyword or phrase per line. For example:

Python
Data Analysis
Machine Learning
Project Management
SQL

4. Run the Script
Execute the script from your terminal:

python resume_shortlist.py

5. Check the Results
The script will first print the detailed response from the AI in your terminal.
Afterward, you will find a new folder named shortlisted containing the PDF resumes of the top candidates.

Customization
AI Model: You can change the OpenAI model by modifying the model parameter in the analyze_resumes function in resume_shortlist.py.

Prompt Engineering: To change how the AI evaluates candidates, you can adjust the system message or user instructions in the build_prompt function.

This project is intended as a tool to assist in the hiring process and should be used as a part of a broader, unbiased recruitment strategy.
