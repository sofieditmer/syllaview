"""
MAIN FUNCTIONALITIES OF SYLLAVIEW

This script holds the main functionalities of SyllaView. This includes making the overview dataframe which holds a summary of each
uploaded reading, the main keywords and topics. It also makes the visualizations which include a wordcloud of the most prominent words
within each reading, word clouds of each of the topics, as well as a graph displaying the raw word frequencies. 
"""

# --------- PACKAGES --------- #
import os
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load("en_core_web_lg")
import nltk
from pages.utils import summarize, convert_tuple_to_dict, save_uploadedfile, convert_df_to_csv
from cleantext import clean
from spacypdfreader import pdf_reader
from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaMulticore
from wordcloud import WordCloud
from itertools import chain
import matplotlib.pyplot as plt
import plotly.express as px

# --------- MAIN FUNCTION --------- #

def main():

    with st.container():

        st.markdown("***")

        # course menu
        choose = option_menu("", ["Course 1", "Course 2", "Course 3"],
                        icons = ['bookmark-fill', 'bookmark-fill', 'bookmark-fill'],
                        orientation = "horizontal",
                        styles = {"container": {"padding": "5!important", "background-color": "#898989"}, 
                                "icon": {"color": "black", "font-size": "15px"}, 
                                "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                                "nav-link-selected": {"background-color": "#B2BABB"}})

        # same functionalities for all courses
        if choose == "Course 1" or choose == "Course 2" or choose == "Course 3":

            # ----- UPLOAD FILES ----- #
            uploaded_files = st.file_uploader("Upload your syllabus as PDFs", type="pdf", accept_multiple_files=True)

            # enable the user to also work with scans of books
            scans = st.checkbox("I have a scanned reading")
            if scans:
                uploaded_scan = st.file_uploader("Upload your scanned readings", type=["jpg", "png"], accept_multiple_files=True)

            # create output directory if it does not exist
            if not os.path.exists(os.path.join("tempDir")):
                os.mkdir(os.path.join("tempDir"))

            if len(uploaded_files) >= 1:

                st.markdown("***")

                # title
                st.markdown(f"<h4 style='text-align: center; color: black;'>Below is your Syllaview</h1>", unsafe_allow_html=True)

                # ----- CUSTOMIZATION OPTIONS ----- #
                with st.expander("Click here for customization options"):
                    
                    # length of summary
                    pick_len_summary = st.radio(
                        "Length of the summary",
                        ('Short', 'Medium', 'Long'))

                    # number of topics
                    pick_n_topics = st.slider("Number of topics", 0, 5, 1)

                    # make overview_df to be appended for each uploaded article
                    if pick_n_topics == 0:
                        overview_df = pd.DataFrame(columns=['Reading', 'Summary', 'Keywords', 'Own Notes'])
                    
                    if pick_n_topics == 1:
                        overview_df = pd.DataFrame(columns=['Reading', 'Summary', 'Keywords', 'Main Topic', 'Own Notes'])

                    if pick_n_topics == 2:
                        overview_df = pd.DataFrame(columns=['Reading', 'Summary', 'Keywords', 'Topic 1', 'Topic 2', 'Own Notes'])

                    if pick_n_topics == 3:
                        overview_df = pd.DataFrame(columns=['Reading', 'Summary', 'Keywords', 'Topic 1', 'Topic 2', 'Topic 3', 'Topic 4', 'Own Notes'])

                    if pick_n_topics == 4:
                        overview_df = pd.DataFrame(columns=['Reading', 'Summary', 'Keywords', 'Topic 1', 'Topic 2', 'Topic 3', 'Topic 4', 'Topic 5', 'Own Notes'])

                for uploaded_file in uploaded_files:

                    # ----- READ PDFs ----- #
                    doc, list_clean_tokens, reading_summary = read_files(uploaded_file, pick_len_summary)

                    # ----- FREQUENCY PLOT ----- #
                    frequency_plot = most_frequent_words(list_clean_tokens, uploaded_file)

                    # ----- WORDCLOUD ----- #
                    keywords_wordcloud, wordcloud_keywords = create_wordcloud(doc, uploaded_file)

                    # ----- TOPIC MODELING ----- #
                    plt, topic0, topic1, topic2, topic3, topic4 = topic_modeling(list_clean_tokens, doc, uploaded_file)

                    # ----- SYLLAVIEW: OVERVIEW DATAFRAME ----- #
                    temp_df = create_overview_df(pick_n_topics, uploaded_file, reading_summary, wordcloud_keywords, topic0, topic1, topic2, topic3, topic4)
                    overview_df = overview_df.append(temp_df, ignore_index=True)   

                # ----- VISUALIZATIONS ----- #
                if len(overview_df) >= 1:

                    # unlist keywords and topics
                    ', '.join(overview_df["Keywords"][0])

                    # download button
                    overview_csv = convert_df_to_csv(overview_df)
                    st.download_button("Download Table", data=overview_csv, file_name='SyllaView.csv')

                    # display syllaview
                    overview_df = overview_df.set_index("Reading") 
                    st.table(overview_df)

                    # make the reader aware that there are more detail below
                    st.markdown(f"<h5 style='text-align: center; color: black;'>Explore readings in more detail below</h1>", unsafe_allow_html=True)

                for uploaded_file in uploaded_files:

                    with st.expander(f"Click to explore '{uploaded_file.name}' in more detail", expanded=False):

                        with st.spinner("Preparing visualizations..."):

                            # ----- READ PDFs ----- #
                            doc, list_clean_tokens, _ = read_files(uploaded_file, pick_len_summary)

                            # ----- FREQUENCY PLOT ----- #
                            frequency_plot = most_frequent_words(list_clean_tokens, uploaded_file)

                            # ----- WORDCLOUD ----- #
                            keywords_wordcloud, wordcloud_keywords = create_wordcloud(doc, uploaded_file)

                            # ----- TOPIC MODELING ----- #
                            plt, topic0, topic1, topic2, topic3, topic4 = topic_modeling(list_clean_tokens, doc, uploaded_file)

                            # ----- TOPIC MODELING ----- #
                            st.markdown(f"<h4 style='text-align: center; color: black;'>The 5 most prevalent topics within '{uploaded_file.name}'</h1>", unsafe_allow_html=True)
                            st.pyplot(plt, use_container_width=True)

                            # ----- WORDCLOUD ----- #
                            st.markdown(f"<h4 style='text-align: center; color: black;'>Common words within '{uploaded_file.name}'</h1>", unsafe_allow_html=True)
                            st.image(keywords_wordcloud.to_array(), caption = "The sizes of the words correspond to their frequencies")

                            # ----- FREQUENCY PLOT ----- #
                            st.markdown("<h4 style='text-align: center; color: black;'>Word Frequencies</h1>", unsafe_allow_html=True)
                            frequency_plot.update_layout(title_x=0.5, title_font_size=20)
                            frequency_plot.update_xaxes(tickangle=45)
                            st.plotly_chart(frequency_plot, use_container_width=True)


# --------- FUNCTIONS --------- #

# --------- READ FILES FUNCTION --------- #
def read_files(uploaded_file, pick_len_summary):
    """
    Reads each uplodaed PDF, annotates them with SpaCy and creates summaries.
    """

    if uploaded_file is not None:

        save_uploadedfile(uploaded_file)
        pdf_path = os.path.join("tempDir", uploaded_file.name)

        with st.spinner(text=f"Preparing summary of {uploaded_file.name}"):

            # read file
            pdf_text = pdf_reader(pdf_path, nlp)

            # annotate with spacy
            doc = nlp(pdf_text)

            # extract meaningful tokens
            remove = ['ADV','PRON','CCONJ','PUNCT','PART','DET','ADP','SPACE', 'NUM', 'SYM']
            list_clean_tokens = [token.lemma_.lower() for token in doc if token.pos not in remove and not token.is_stop and token.is_alpha]

            # split
            list_clean_tokens = [token.split() for token in list_clean_tokens]

            # create summary of length specified by user
            reading_summary = summarize(pdf_text, length = pick_len_summary)
            reading_summary = clean(reading_summary)

    return doc, list_clean_tokens, reading_summary

# --------- ESTIMATE MOST FREQUENT WORDS FUNCTION --------- #
def most_frequent_words(list_clean_tokens, uploaded_file):
    """
    Estimates the most frequent words within each reading and creates a frequency plot.
    """

    with st.spinner(f"Finding the most frequent words in {uploaded_file.name}"):

        # unlist
        unlist_clean_tokens = list(chain.from_iterable(list_clean_tokens))

        # remove single letters
        clean_tokens = []
        for token in unlist_clean_tokens:
            if len(token)>1:
                clean_tokens.append(token)

        # frequency
        token_freq = nltk.FreqDist(clean_tokens)

        # most common tokens
        most_common = token_freq.most_common(20)
        dictionary = {}
        most_common_dict = convert_tuple_to_dict(most_common, dictionary)

        # frequency plot
        frequency_plot = px.bar(x = list(most_common_dict.keys()),
                                y = list(most_common_dict.values()),
                                labels = {'x': 'Word', 'y': 'Frequency'},
                                height = 700,
                                width = 700)

    return frequency_plot

# --------- CREATE WORDCLOUD FUNCTION --------- #
def create_wordcloud(doc, uploaded_file):
    """
    Creates a wordcloud of the most frequent words.
    Code adapted from: https://medium.com/illumination/scraping-news-and-creating-a-word-cloud-in-python-10ea312c49ba
    """

    with st.spinner(f"Preparing wordcloud visualization of {uploaded_file.name}"):

        newText = " "
        for word in doc:
            if word.pos_ in ["ADJ", "NOUN", "VERB"]:
                newText = " ".join((newText, word.text.lower()))

        # big wordcloud with keywords
        keywords_wordcloud = WordCloud(width=1500, 
                                        height=500,
                                        background_color = "white",
                                        color_func=lambda *args, **kwargs: (0,86,148),  # darkblue
                                        stopwords=STOP_WORDS).generate(newText)

        wordcloud_keywords = list(keywords_wordcloud.words_.keys())[:20]
        wordcloud_keywords = ", ".join(wordcloud_keywords)

        return keywords_wordcloud, wordcloud_keywords

# --------- TOPIC MODELING FUNCTION --------- #
def topic_modeling(list_clean_tokens, doc, uploaded_file):
    """
    Performs topic modeling on each reading and creates a wordcloud for each topic. 
    """

    with st.spinner(f"Performing topic modeling on {uploaded_file.name}"):

        # create dictionary
        dictionary = Dictionary(list_clean_tokens)

        # filter out low and high frequency tokens and limit vocav to 1000
        dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=1000)

        # create corpus
        corpus = [dictionary.doc2bow(doc) for doc in list_clean_tokens]

        # topic modeling
        lda_model = LdaMulticore(corpus=corpus, 
                                id2word=dictionary, 
                                iterations=50, 
                                num_topics=5, 
                                workers = 4, 
                                passes=10)

        # Create list of colors
        cols = [color for color in ['#005694', '#005694', '#005694', '#005694', '#005694']]

        # Define wordcloud
        topic_wordclouds = WordCloud(background_color='white',
                                    width=2500,
                                    height=2500,
                                    max_words=10,
                                    prefer_horizontal=1.0,
                                    color_func=lambda *args, **kwargs: cols[i])
        
        # LDA topics
        topics_fromlda = lda_model.show_topics(num_topics = 5, formatted=False)
        
        # make list of topics
        topics_list = []
        for i in range(len(topics_fromlda)):
            temp = dict(topics_fromlda[i][1])
            topics_list.append(temp)

        topic0 = list(topics_list[0].keys())
        topic0 = ", ".join(topic0)

        topic1 = list(topics_list[1].keys())
        topic1 = ", ".join(topic1)

        topic2 = list(topics_list[2].keys())
        topic2 = ", ".join(topic2)

        topic3 = list(topics_list[3].keys())
        topic3 = ", ".join(topic3)

        topic4 = list(topics_list[4].keys())
        topic4 = ", ".join(topic4)

        # Generate a wordcloud for each topic
        fig, axes = plt.subplots(1, 5, figsize=(10,10), sharex=True, sharey=True)

        for i, ax in enumerate(axes.flatten()):
            fig.add_subplot(ax)
            topic_words = dict(topics_fromlda[i][1])
            topic_wordclouds.generate_from_frequencies(topic_words, max_font_size=400)
            plt.gca().imshow(topic_wordclouds)
            plt.gca().set_title('Topic ' + str(i))
            plt.gca().axis('off')
            plt.subplots_adjust(wspace=0, hspace=0)
            plt.axis('off')
            plt.margins(x=0, y=0)
            plt.tight_layout()

    return plt, topic0, topic1, topic2, topic3, topic4

# --------- CREATES OVERVIEW / SYLLAVIEW FUNCTION --------- #
def create_overview_df(pick_n_topics, uploaded_file, reading_summary, wordcloud_keywords, topic0, topic1, topic2, topic3, topic4):
    """
    Creates the overview dataframe, SyllaView, which holds each reading as a row and the summary, keywords, and topics as columns.
    """
        
    with st.spinner("Preparing your SyllaView..."):

        if pick_n_topics == 0:
            temp_df = {'Reading': uploaded_file.name, 
                        'Summary': reading_summary,
                        'Keywords': wordcloud_keywords,
                        'Own Notes': ""}

        elif pick_n_topics == 1:
            temp_df = {'Reading': uploaded_file.name, 
                        'Summary': reading_summary,
                        'Keywords': wordcloud_keywords, 
                        'Main Topic': topic0,
                        'Own Notes': ""}

        elif pick_n_topics == 2:
            temp_df = {'Reading': uploaded_file.name, 
                        'Summary': reading_summary,
                        'Keywords': wordcloud_keywords, 
                        'Topic 1': topic0,
                        'Topic 2': topic1,
                        'Own Notes': ""}
                    
        elif pick_n_topics == 3:
            temp_df = {'Reading': uploaded_file.name, 
                        'Summary': reading_summary,
                        'Keywords': wordcloud_keywords, 
                        'Topic 1': topic0,
                        'Topic 2': topic1,
                        'Topic 3': topic2,
                        'Own Notes': ""}

        elif pick_n_topics == 4:
            temp_df = {'Reading': uploaded_file.name, 
                        'Summary': reading_summary,
                        'Keywords': wordcloud_keywords, 
                        'Topic 1': topic0,
                        'Topic 2': topic1,
                        'Topic 3': topic2,
                        'Topic 4': topic3,
                        'Own Notes': ""}

        else:
            temp_df = {'Reading': uploaded_file.name, 
                        'Summary': reading_summary,
                        'Keywords': wordcloud_keywords, 
                        'Topic 1': topic0,
                        'Topic 2': topic1,
                        'Topic 3': topic2,
                        'Topic 4': topic3,
                        'Topic 5': topic4,
                        'Own Notes': ""}                       

    return temp_df