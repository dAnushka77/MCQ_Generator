import random
import spacy
from collections import Counter
from flask_bootstrap import Bootstrap
from flask import Flask, request, render_template
from PyPDF2 import PdfReader, PdfWriter

app = Flask(__name__)
Bootstrap(app)

# Load English tokenizer, tagger, parser, NER and vectors
nlp = spacy.load('en_core_web_sm')

def generate_mcqs(text, num_questions=5):
    if not text:
        return []

    # Process the text with spacy
    doc = nlp(text)

    # Extract sentences from the text
    sentences = [sent.text for sent in doc.sents]

    # Select a few sentences to generate questions from
    selected_sentences = random.sample(sentences, min(num_questions, len(sentences)))

    # Extract all unique nouns from the entire text
    all_nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    unique_nouns = list(set(all_nouns))

    # Initialize list to store generated MCQs
    mcqs = []

    # Generate MCQs for each selected sentence
    for sentence in selected_sentences:
        # Process the sentence with spacy
        sent_doc = nlp(sentence)

        # Extracting entities (nouns) from sentence
        nouns = [token.text for token in sent_doc if token.pos_ == "NOUN"]

        # Ensure there are enough nouns to generate MCQs
        if len(nouns) < 2:
            continue

        # Select the most common noun as the subject of the question
        noun_counts = Counter(nouns)
        subject = noun_counts.most_common(1)[0][0]

        # Generate the question stem
        question_stem = sentence.replace(subject, "________")

        # Generate the answer choices, starting with the correct answer
        answer_choices = [subject]

        # Generate distractors
        distractors = [word for word in unique_nouns if word != subject and word not in answer_choices]
        random.shuffle(distractors)

        # Add distractors to the answer choices, ensuring uniqueness
        answer_choices.extend(distractors[:3])

        # Shuffle the answer choices
        random.shuffle(answer_choices)

        # Converting correct answer key to A/B/C/D code
        correct_answer = chr(65 + answer_choices.index(subject))

        # Append the generated MCQs to the list
        mcqs.append((question_stem, answer_choices, correct_answer))

    return mcqs


def process_pdf(file):
    # Initialize empty string to store the extracted text
    text = ""
    # Creating an object
    pdf_reader = PdfReader(file)
    # Looping through the pdf file's pages
    for page_num in range(len(pdf_reader.pages)):
        # Extract text from the current page
        page_text = pdf_reader.pages[page_num].extract_text()
        # Append the extracted text to the overall text
        text += page_text
    return text 
    

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        text = ""
        
        # check if files were uploaded
        if 'files[]' in request.files:
            files = request.files.getlist("files[]")
            for file in files:
                #print(file)
                if file.filename.endswith('.pdf'):
                    # Process pdf files
                    text += process_pdf(file)
                elif file.filename.endswith('.txt'):
                    # Process text files
                    text += file.read().decode('utf-8') 
        else: 
            # Process manual input  
            text= request.form['text']      
    
        # Get the selected number of questions from the dropdown menu                
        num_questions = int(request.form['num_questions'])    
        mcqs = generate_mcqs(text, num_questions=num_questions)
        
        # Ensure that each mcq is correctly formatted as (question_stem, answer_choices, correct_answer)
        mcqs_with_index = [(i + 1, mcq) for i,mcq in enumerate(mcqs)]
        return render_template('mcqs.html', mcqs=mcqs_with_index)
    
                          
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
