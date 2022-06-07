"""
APP INTERFACE OF SYLLAVIEW

This script contains the setup of the SyllaView interface.
"""

# --------- PACKAGES --------- #
import streamlit as st 
from streamlit_option_menu import option_menu
import pages.create_syllaview as create_syllaview
import pages.homepage as homepage
import pages.about as about

# --------- GLOBAL PAGE CONFIGURATION --------- #
st.set_page_config(page_title = "SyllaView", page_icon = "📝", layout="wide")

# --------- MAIN FUNCTION --------- #
def main():

    # header 
    st.markdown("<h1 style='text-align: center; '>SyllaView</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; '>Helping university students gain an overview of their syllabus</h5>", unsafe_allow_html=True)

    # menu adapted from: https://medium.com/codex/create-a-multi-page-app-with-the-new-streamlit-option-menu-component-3e3edaf7e7ad
    choose = option_menu("", ["Home Page", "Create your SyllaView", "About"],
                        icons = ['house-fill', 'collection-fill', 'book-fill'],
                        orientation = "horizontal",
                        styles = {"container": {"padding": "5!important", "background-color": "#fafafa"}, 
                                "icon": {"color": "black", "font-size": "30px"}, 
                                "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#B2BABB"},
                                "nav-link-selected": {"background-color": "#B2BABB"}})

    # homepage
    if choose == "Home Page":
        homepage.main()
    
    # SyllaView page
    if choose == "Create your SyllaView":
        create_syllaview.main()

    # about page
    if choose == "About":
        about.main()

if __name__ == "__main__":
    main()