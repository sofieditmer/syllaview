# SyllaView: A Tool to Assist University Students in Gaining an Overview of Their Syllabus

## Description

This repository contains the scripts and resources for the exam project of Human Computer Interaction (HCI) course at Aarhus University, Cognitive Science Master's Degree. 

**Abstract**

## Repository Structure

```
|-- src/                        # Directory for python scripts
    |-- notebooks/              # Directory for notebooks used for data preprocessing
    |-- grid_search.py          # Script for grid search of linear regression and neural network parameters
    |-- sentiment_prediction.py # Script for model evaluation on test data and sentiment prediction 
    |-- lexicon_evaluation.py   # Script for lexicon evaluation of sentiment classification task
    
|-- utils/                      # Directory for utility scripts
    |-- data_utils.py           # Utility functions for data processing
    |-- model_utils.py          # Utility functions for model training and evaluation
    |-- linear_regression.py    # Linear regression class
    |-- neural_network.py       # Neural network class
    |-- classification_utils.py # Utility functions for sentiment classification
    |-- twittertokens.py        # Defines tokens for Twitter API (not on github)

|-- README.md
|-- requirements.txt            # Dependencies to run scripts and notebooks
|-- install_requirements.txt     # Bash script to install dependencies and language models
```

The files described in the repository structure, which are not on GitHub can be provided on request. 

## Usage

**!** The scripts have only been tested on Linux, using Python 3.9.1.  

To run the scripts, we recommend cloning this repository and installing necessary dependencies in a virtual environment. Dependencies are listed in the `requirements.txt` file. To install all necessary requirements, including the English spaCy language model, the bash script `install_requirements.sh` shoud be used. 

## Contributors
This project was developed in a joined effort by Melina Vejlø and Sofie Ditmer.