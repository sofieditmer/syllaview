""""
UTILITY SCRIPTS

This script holds several utility functions used in the create_syllaview.py script. 
"""

# --------- PACKAGES --------- #
from unittest.util import _MAX_LENGTH
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load("en_core_web_lg") 
from string import punctuation
from heapq import nlargest
import os
from autocorrect import Speller
import wordsegment
from transformers import pipeline
summarization = pipeline("summarization")

# --------- SUMMARIZER FUNCTION --------- #
def summarize(text, length = "Short"):
    """
    Summarize function adapted from https://www.activestate.com/blog/how-to-do-text-summarization-with-python/
    """

    # annotate input text 
    doc = nlp(text)

    # extract word frequencies
    word_frequencies={}
    for word in doc:
        # remove stopwords
        if word.text.lower() not in list(STOP_WORDS):
            # remove punctuations
            if word.text.lower() not in punctuation:
                # add word to dict
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    # extract the maximum frequncy 
    max_frequency=max(word_frequencies.values())

    # divide the frequency of each word by the maximum frequency 
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency

    # extract sentences from input text 
    sentence_tokens= [sent for sent in doc.sents]

    # calculate sentence scores
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]

     # to make the compiler work
    summary = None

    if length == "Short":        
        summary=nlargest(5, sentence_scores, key=sentence_scores.get)
        final_summary=[word.text for word in summary]
        summary=''.join(final_summary)

    if length == "Medium":
        summary=nlargest(10, sentence_scores, key=sentence_scores.get)
        final_summary=[word.text for word in summary]
        summary=''.join(final_summary)

    if length == "Long":
        summary=nlargest(15, sentence_scores, key=sentence_scores.get)
        final_summary=[word.text for word in summary]
        summary=''.join(final_summary)

    return summary

# --------- CONVERT TO DICTIONARY FUNCTION --------- #
def convert_tuple_to_dict(tuple, dic):
    """
    Converts tuple to dictionary
    """
    dic = dict(tuple)
    return dic

# --------- SAVE UPLOADED FILES FUNCTION --------- #
def save_uploadedfile(uploadedfile):
    """
    Save file in temporary folder.
    """
    with open(os.path.join("tempDir", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())

# --------- CONVERT DATAFRAME TO CSV FUNCTION --------- #
def convert_df_to_csv(df):
    """
    Convert dataframe to csv-file.
    """
    return df.to_csv().encode('utf-8')

# --------- TEXT CLEAN-UP FUNCTION FOR OCR --------- #
def replace(string):
    """
    Cleans up extracted text from OCR.
    """
    processed = string.replace("\n"," ")\
                      .replace("\n\n"," ")\
                      .replace("__"," ")\
                      .replace(" - "," ")\
                      .replace('-""' ," ")\
                      .replace("|", "")\
                      .replace("!", "")\
                      .replace("\s"," ")\
                      .lstrip()
    
    return " ".join(processed.split())

# --------- SPELL-CHECKER AND TOKENIZER FUNCTION FOR OCR --------- #
def ocr_correct(ocr_text):
    """
    Checks spelling and tokenizes extracted text from OCR. 
    """
    # initialize spell-checker and tokenizer
    spell_checker = Speller(lang='en')
    wordsegment.load()

    # Segment based on unigram and bigram frequency
    ocr = wordsegment.segment(ocr_text)

    # join list as string
    ocr = " ".join(ocr)
    
    # spellcheck string
    ocr = spell_checker(ocr)
    
    return ocr

# --------- SUMMARIZATION WITH TRANSFORMERS FUNCTION --------- #
def summarize_using_transformer(doc, pick_len_summary = "Long"):
    """
    Summarizes the input text using the summarization pipeline from the Transformers library.
    """
    # convert doc to string
    string = [sent.text.strip() for sent in doc.sents]

    # unlist
    string = ' '.join([str(elem) for elem in string])

    # pick maximum length as input
    string = string[:1024]

    # Make summary with length determined by user input
    if pick_len_summary == "Short":
        summary_text = summarization(string, max_length=200, min_length=100, do_sample=False)[0]['summary_text']

    if pick_len_summary == "Medium":
        summary_text = summarization(string, max_length=500, min_length=200, do_sample=False)[0]['summary_text']

    if pick_len_summary == "Long":
        summary_text = summarization(string, max_length=1024, min_length=500, do_sample=False)[0]['summary_text']

    return summary_text


