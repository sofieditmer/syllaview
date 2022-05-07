"""
Functions of SyllaView.
"""

# packages
import os
import streamlit as st
from streamlit import components
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load("en_core_web_lg")
from spacypdfreader import pdf_reader
from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaMulticore
import pyLDAvis.gensim_models
from wordcloud import WordCloud
from itertools import chain
import nltk
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from pages.utils import summarize
import matplotlib.colors as mcolors


def main():
    with st.container():

        st.markdown("***")

        ######### READ PDFs #########

        uploaded_files = st.file_uploader("Upload your syllabus as PDFs her", type="pdf", accept_multiple_files=True)

        if not os.path.exists(os.path.join("tempDir")):
            os.mkdir(os.path.join("tempDir"))

        def save_uploadedfile(uploadedfile):
            with open(os.path.join("tempDir", uploadedfile.name), "wb") as f:
                f.write(uploadedfile.getbuffer())

        # make overview_df to be appended for each uploaded article
        overview_df = pd.DataFrame(columns=['Reading', 'Summary', 'Keywords', 'Topics'])

        if uploaded_files is not None:

            for uploaded_file in uploaded_files:
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

                    ######## SUMMARY ##########
                    if len(pdf_text) < 1500:
                        reading_summary = summarize(pdf_text, 0.05)

                    else:
                        reading_summary = summarize(pdf_text, 0.01)

                    ######### MOST FREQUENT WORDS #########

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

                    # convert to dictionary
                    def Convert(tup, di):
                        di = dict(tup)
                        return di
                        
                    dictionary = {}
                    most_common_dict = Convert(most_common, dictionary)

                    frequency_plot = px.bar(x = list(most_common_dict.keys()),
                                            y = list(most_common_dict.values()),
                                            labels = {'x': 'Word', 'y': 'Frequency'},
                                            height = 700,
                                            width = 700)

                    ######### WORDCLOUD #########
                    # https://medium.com/illumination/scraping-news-and-creating-a-word-cloud-in-python-10ea312c49ba

                    newText = " "
                    for word in doc:
                        if word.pos_ in ["ADJ", "NOUN", "VERB"]:
                            newText = " ".join((newText, word.text.lower()))

                    # big word cloud with keywords
                    keywords_wordcloud = WordCloud(width=1500, 
                                                    height=500,
                                                    background_color = "white",
                                                    color_func=lambda *args, **kwargs: (0,86,148),  # darkblue
                                                    stopwords=STOP_WORDS).generate(newText)

                    wordcloud_keywords = list(keywords_wordcloud.words_.keys())[:20]
                    wordcloud_keywords = ", ".join(wordcloud_keywords)

                    ######## TOPIC MODELING #######
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

                    # visualize with pyLDAvis
                    #prepared_pyLDAvis_data = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)
                    #html_string = pyLDAvis.prepared_data_to_html(prepared_pyLDAvis_data)

                    # Create list of colors
                    cols = [color for color in ['#005694', '#005694', '#005694', '#005694', '#005694']]

                    # Define word cloud
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

                    # convert list to dictionary
                    topics_dict = {k: v for d in topics_list for k, v in d.items()}
                    topic_words_display = ", ".join(list(topics_dict.keys()))
                        
                    # Generate a word cloud for each topic
                    fig, axes = plt.subplots(1, 5, figsize=(10,10), sharex=True, sharey=True)

                    for i, ax in enumerate(axes.flatten()):
                        fig.add_subplot(ax)
                        topic_words = dict(topics_fromlda[i][1])
                        topic_wordclouds.generate_from_frequencies(topic_words, max_font_size=400)
                        plt.gca().imshow(topic_wordclouds)
                        plt.gca().set_title('Topic ' + str(i))
                        plt.gca().axis('off')
                        
                        # Additional adjusting
                        plt.subplots_adjust(wspace=0, hspace=0)
                        plt.axis('off')
                        plt.margins(x=0, y=0)
                        plt.tight_layout()
                    
                    ########## OVERVIEW #########
                    temp_df = pd.DataFrame({'Reading': [uploaded_file.name], 
                                            'Summary': reading_summary,
                                            'Keywords': wordcloud_keywords, 
                                            'Topics': topic_words_display})
                                            
                    overview_df = pd.concat([overview_df, temp_df])
                    overview_df = overview_df.set_index('Reading')

            
            ########### DISPLAY ###########

            if len(overview_df) >= 1:

                # unlist keywords and topics
                ', '.join(overview_df["Keywords"][0])

                st.markdown("***")

                # display table overview
                st.markdown(f"<h4 style='text-align: center; color: black;'>Below is your Syllaview</h1>", unsafe_allow_html=True)
                st.table(overview_df)

                # download button
                def convert_df_to_csv(df):
                    return df.to_csv().encode('utf-8')

                overview_csv = convert_df_to_csv(overview_df)

                st.download_button(label="Download table", data=overview_csv, file_name='SyllaView.csv')

                # make the reader aware that there are more detail below
                st.markdown(f"<h5 style='text-align: center; color: black;'>Explore readings in more detail below</h1>", unsafe_allow_html=True)


            for uploaded_file in uploaded_files:

                with st.expander(f"Click to explore '{uploaded_file.name}' in more detail", expanded=False):

                    with st.spinner("Preparing visualizations..."):

                        # SUMMARY
                        st.markdown(f"<h4 style='text-align: center; color: black;'>Summary of '{uploaded_file.name}'</h1>", unsafe_allow_html=True)
                        st.write(f"**Summary:** {reading_summary}")

                        # TOPIC MODELING
                        #components.v1.html(html_string, width=3000, height=1000, scrolling=True)
                        st.markdown(f"<h4 style='text-align: center; color: black;'>The 5 most prevalent topics within '{uploaded_file.name}'</h1>", unsafe_allow_html=True)
                        
                        st.pyplot(plt, use_container_width=True)

                        # WORDCLOUD
                        st.markdown(f"<h4 style='text-align: center; color: black;'>Common words within '{uploaded_file.name}'</h1>", unsafe_allow_html=True)
                        st.image(keywords_wordcloud.to_array())

                        # FREQUENCY PLOT
                        st.markdown("<h4 style='text-align: center; color: black;'>Word Frequencies</h1>", unsafe_allow_html=True)
                        frequency_plot.update_layout(title_x=0.5, title_font_size=20)
                        frequency_plot.update_xaxes(tickangle=45)
                        st.plotly_chart(frequency_plot, use_container_width=True)

                        