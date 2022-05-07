"""
Main app interface of SyllaView
"""

# packages
import streamlit as st 
from streamlit_option_menu import option_menu
import pages.functions as functions
import pages.homepage as homepage

# global page configurations
st.set_page_config(page_title = "SyllaView", page_icon = "📝", layout="wide")

# main function
def main():

    # header 
    st.markdown("<h1 style='text-align: center; '>SyllaView</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; '>Helping university students gain an overview of their syllabus</h5>", unsafe_allow_html=True)

    # menu https://medium.com/codex/create-a-multi-page-app-with-the-new-streamlit-option-menu-component-3e3edaf7e7ad
    choose = option_menu("", ["Home Page", "Get Started", "Question Answering", "About"],
                        icons=['house-fill', 'geo-alt-fill', 'question-circle-fill', 'book-fill'],
                        orientation="horizontal",
                        styles={"container": {"padding": "5!important", "background-color": "#fafafa"}, 
                                "icon": {"color": "black", "font-size": "25px"}, 
                                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                                "nav-link-selected": {"background-color": "#B2BABB"}}
                        )

    # functions page
    if choose == "Get Started":
        functions.main()

    # homepage
    if choose == "Home Page":
        homepage.main()

if __name__ == "__main__":
    main()