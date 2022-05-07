import streamlit as st 

def main():
    video_file = open('src/pages/test_video.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes, start_time=0)