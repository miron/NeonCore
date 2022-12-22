import re
import nltk
from PyPDF2 import PdfReader
nltk.download('punkt')

# Open the PDF file in read-only mode
with open('RTG-CPR-EasyModev1.1.pdf', 'rb') as file:
    # Create a PDF object
    pdf = PdfReader(file)
    # Get the number of pages in the PDF
    num_pages = len(pdf.pages)
    # Create an empty list to store the sentences
    sentences = []
    # Iterate over the pages and extract the text
    for i in range(num_pages):
        page = pdf.getPage(i)
        text = page.extractText()
        # Remove leading and trailing white space and newline characters
        text = text.strip() 
        # Replace newline characters with a single space
        text = text.replace('\n', ' ')
        # Replace hyphens and spaces following them with an empty string
        text = re.sub(r'(\s+-\s+)|(-\s+)|(\s+-)', '', text) 
        # Tokenize the text into sentences
        page_sentences = nltk.sent_tokenize(text)
         # Split the sentences into a list of words
        page_sentences = [sentence.split() for sentence in page_sentences]
        # Remove punctuation using regular expressions
        page_sentences = [[re.sub(r'[^\w\s\’\']', '', word) for word in sentence] for sentence in page_sentences]
        # Join the words into sentences while inserting a single space character between each word
        page_sentences = [' '.join(sentence) for sentence in page_sentences]
        sentences.extend(page_sentences)
    print(sentences)
