"""
HOMEPAGE OF SYLLAVIEW

This is the homepage of SyllaView which contains a brief welcome-greeting to the users as well as an introduction video that demonstrates how to use SyllaView.
"""

# --------- PACKAGES --------- #
import streamlit as st 

# --------- MAIN FUNCTION --------- #
def main():

    with st.container():

        # title
        st.markdown("<h4 style='text-align: center; color: black;'>Welcome to SyllaView!</h1>", unsafe_allow_html=True)
        
        # text
        st.markdown("Tired of having multiple files opened at once to try and get a grasp of the course syllabus? Syllaview is a tool developed with university students in mind, allowing you to create a quick overview of your course syllabi. Watch the video below for a guided tour of how to use SyllaView.")

        # demonstration video
        st.video("https://www.youtube.com/watch?v=fm7PIdc4tBU")