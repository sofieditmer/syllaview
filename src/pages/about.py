"""
ABOUT PAGE OF SYLLAVIEW

This is the about page for SyllaView which contains a description of the platform, FAQ, as well as contact information.
"""

# --------- PACKAGES --------- #
import os
import streamlit as st 
from streamlit_option_menu import option_menu

# --------- MAIN FUNCTION --------- #
def main():

    with st.container():

        st.markdown("***")

        # menu
        choose = option_menu("", ["About", "How does it work?", "FAQ"],
                        icons = ['info-circle-fill', 'nut-fill','question-circle-fill'],
                        orientation = "horizontal",
                        styles = {"container": {"padding": "5!important", "background-color": "#898989"}, 
                                "icon": {"color": "black", "font-size": "15px"}, 
                                "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                                "nav-link-selected": {"background-color": "#B2BABB"}})

        # about
        if choose == "About":

            with st.container():

                st.write("*SyllaView* is a tool developed with university students in mind. The name 'SyllaView' is a contraction of 'Syllabus' and 'Overview', because the tool makes it possible to gain a quick overview of your course syllabi to allow you to focus on the more important part of exam preparation. To create a SyllaView all you have to do is upload your course readings and SyllaView will do the rest!")
                
                st.write("With SyllaView you get:")

                st.write("1. A summary of each uploaded reading")

                st.write("2. The most important keywords")
                
                st.write("3. The most prominent topics")

                st.write("4. The possibility to download the SyllaView as a CSV-file to your local computer")

                st.write("All of the above are gathered in one place, which means that you no longer have to flick through multiple PDFs at once!")
        
        # functionalities 
        if choose == "How does it work?":

             with st.container():

                st.write("**1. Text Summarization**")
                st.write("When uploading a PDF-file the Python package *pdf_reader* is used to extract the text from the file. The text is then annotated using the SpaCy English model *en_core_web_lg* which is a trained language model. Then the summarization-pipeline available in the *Transformers* Python package is used to create a text summary. If you wish to know more about how the summarization works, you can read more [here](https://huggingface.co/tasks/summarization) or check out the Python scripts available on our [GitHub](https://github.com/sofieditmer/syllaview/blob/main/src/pages/create_syllaview.py).")
                
                st.write("**2. Keywords**")
                st.write("The keywords are the most common words in the uploaded reading. These are estimated using the *FreqDist* function available in the *NLTK* library.")

                st.write("**3. Topic Modeling**")
                st.write(" Topic Modeling is a text-mining tool used to extract hidden semantic structure from a text. Topic modeling assumes that each document can be described as a distribution of topics and each topic can be described by as distribution of words. In SyllaView, the topics are extracted from the uploaded readings using the *LdaMulticore* function available in *Gensim*. This type of analysis is based on word frequency and the assumption that (1) a given word will appear more if a text is about that specific topic and (2) any text typically contains more than one topic. The latter is the reason why SyllaView allows the user to estimate up to 5 topics per text. The topics are listed as clusters of words that make up that particular topic. If you wish to know more about how topic modeling works you can read more [here](https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/) or check out the Python scripts available on our [GitHub](https://github.com/sofieditmer/syllaview/blob/main/src/pages/create_syllaview.py).")

                st.write("**4. Optical Character Recognition (OCR) for scanned readings**")
                st.write("OCR allows a user of SyllaView to upload a scanned reading e.g. as a book. When a scanned text is uploaded, SyllaView converts the scan to gray-scale, i.e. only black and white. The scan is then thresholded to figure out where there is text and is not. The summary is then created the same way as for regular PDF-files.")

        # FAQ
        if choose == "FAQ":

            with st.container():

                st.subheader("Frequently Asked Questions")
                
                st.write("**Is SyllaView free?**")
                st.write("Yes, SyllaView is free to use.")

                st.write("")

                st.write("**How do I use SyllaView?**")
                st.write("You can go to the front page for a guided tour of SyllaView.")

                st.write("")

                st.write("**How does SyllaView work behind the scenes?**")
                st.write("If you are wondering how SyllaView makes the reading summaries, finds the most important keywords and topics, feel free to visit our [GitHub-repository](https://github.com/sofieditmer/syllaview) to have a look at the Python-scripts that work behind the scenes. You can also navigate to 'How does it work?' to read more about the functionalities.")
