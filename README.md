# *SyllaView:* A Tool to Assist University Students in Gaining an Overview of Their Syllabus

## Description

This repository contains the scripts and resources for the exam project of the Human Computer Interaction (HCI) course at Aarhus University, Cognitive Science Master's Degree. This project involved developing a platform which assists university students in gaining an overview of their course syllabi when studying for upcoming exams. If you wish to know how to use the functional Streamlit platform, you can watch the [demonstration video](https://www.youtube.com/watch?v=fm7PIdc4tBU) below.

[![Watch video](https://github.com/sofieditmer/syllaview/blob/main/src/video_image.png)](https://www.youtube.com/watch?v=fm7PIdc4tBU)

## Figma vs. Streamlit

While this repository contains the functional Streamlit prototype developed in Python, you are welcome to also interact with the conceptual prototype developed in Figma. You can access it [here](https://www.figma.com/proto/3tFwbVng7izhjc9OVAt67X/SyllaView?node-id=38%3A6091&scaling=contain&page-id=0%3A1).

## Repository Structure

```
|-- src/                         # Directory for python scripts
    |-- app.py                   # Python script for the main interface of SyllaView
    |-- pages/                   # Folder containing the python scripts for the different pages of SyllaView
        |-- about.py             # Python script for the About page
        |-- homepage.py          # Python script for the hompage of SyllaView
        |-- create_syllaview.py  # Python script for the SyllaView page
        |-- utils.py             # Utility functions

|-- README.md                   
|-- requirements.txt             # Dependencies to run scripts
|-- install_requirements.sh      # Bash script to install dependencies and SpaCy language model
|-- Figma Conceptual Prototype   # Conceptual prototype of SyllaView
```

## Usage

**!** The scripts have only been tested on Linux, using Python 3.9.1.  

To run the scripts, we recommend cloning this repository and installing necessary dependencies in a virtual environment. Dependencies are listed in the `requirements.txt` file. To install all necessary requirements, including the English spaCy language model, the bash script `install_requirements.sh` should be used. Once, the necessary requirements have been installed the Streamlit App can be run.

```
git clone https://github.com/sofieditmer/syllaview

bash install_requirements.sh

streamlit run src/app.py
```

## Contributors

This project was developed in a joined effort by Melina Vejlø and Sofie Ditmer.