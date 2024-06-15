import pandas as pd
from bs4 import BeautifulSoup
import csv
import re

# Function to clean text
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Replace all whitespace (including newlines) with a single space
    return text.strip()

# Load HTML content from file
file_path = 'input.html'

with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Extracting questions, choices, and explanations
data = []

for question_div in soup.find_all('div', class_='container_question'):
    question_text = clean_text(question_div.find('div', class_='question').get_text(strip=True))
    
    answer_choices = [clean_text(li.get_text(strip=True)) for li in question_div.find('ul', class_='container_answer').find_all('li')]
    explanation_div = question_div.find('div', class_='container_explication')
    
    if explanation_div:
        explanation_text = clean_text(explanation_div.get_text(strip=True))
    else:
        explanation_text = ""

    # Prepare choices
    choices = answer_choices[:4]  # Ensure there are at most 4 choices
    
    # Ensure there are exactly 4 choices
    while len(choices) < 4:
        choices.append('')
    
    data.append([question_text, choices[0], '', choices[1], '', choices[2], '', choices[3], '', explanation_text])

# Create a DataFrame
df = pd.DataFrame(data, columns=['question', 'choice1', 'c1', 'choice2', 'c2', 'choice3', 'c3', 'choice4', 'c4', 'explanation'])

# Save DataFrame to CSV with quotes around all fields
csv_file_path = 'exam_questions.csv'
df.to_csv(csv_file_path, index=False, quoting=csv.QUOTE_ALL)

print(f"Data has been saved to {csv_file_path}")
