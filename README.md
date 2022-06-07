# *SyllaView:* A Tool to Assist University Students in Gaining an Overview of Their Syllabus

## Description

This repository contains the scripts and resources for the exam project of the Human Computer Interaction (HCI) course at Aarhus University, Cognitive Science Master's Degree. This project involved developing a platform which assists university students in gaining an overview of their course syllabi when studying for upcoming exams. If you wish to know how to use the platform, you can watch the demonstration video below.

[![Watch video](https://github.com/sofieditmer/syllaview/blob/main/src/video_image.png)](https://www.youtube.com/watch?v=fm7PIdc4tBU)

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
|-- requirements.txt            # Dependencies to run scripts
|-- install_requirements.txt    # Bash script to install dependencies and SpaCy language model
```

## Usage

**!** The scripts have only been tested on Linux, using Python 3.9.1.  

To run the scripts, we recommend cloning this repository and installing necessary dependencies in a virtual environment. Dependencies are listed in the `requirements.txt` file. To install all necessary requirements, including the English spaCy language model, the bash script `install_requirements.sh` shoud be used. 

## Contributors
This project was developed in a joined effort by Melina Vejlø and Sofie Ditmer.