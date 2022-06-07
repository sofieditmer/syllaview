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
        choose = option_menu("", ["About", "FAQ"],
                        icons = ['info-circle-fill', 'question-circle-fill'],
                        orientation = "horizontal",
                        styles = {"container": {"padding": "5!important", "background-color": "#898989"}, 
                                "icon": {"color": "black", "font-size": "15px"}, 
                                "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                                "nav-link-selected": {"background-color": "#B2BABB"}})

        # about
        if choose == "About":

            with st.container():

                st.write("SyllaView is a tool developed with university students in mind. SyllaView makes it possible to gain a quick overview of your course syllabi to allow you to focus on the more important part of exam preparation. To create a SyllaView all you have to do is upload your course readings and SyllaView will do the rest!")
                
                st.write("With SyllaView you get:")

                st.write("1. A summary of each uploaded reading")

                st.write("2. The most important keywords")
                
                st.write("3. The most prominent topics")

                st.write("4. The possibility to download the SyllaView as a CSV-file to your local computer")

                st.write("5. The possibility to create mindmaps and download them to your local computer")

                st.write("All of the above are gathered in one place, which means that you no longer have to flick through multiple PDFs at once!")

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
                st.write("If you are wondering how SyllaView makes the reading summaries, finds the most important keywords and topics, feel free to visit our [GitHub-repository](https://github.com/sofieditmer/syllaview) to have a look at the Python-scripts that work behind the scenes.")
