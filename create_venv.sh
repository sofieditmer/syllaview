#!/usr/bin/env bash

VENVNAME=venv_HCI_exam

python3 -m venv $VENVNAME
source $VENVNAME/bin/activate
pip install --upgrade pip

pip install ipython
pip install jupyter

python -m ipykernel install --user --name=$VENVNAME

test -f requirements.txt && pip install -r requirements.txt

python3 -m spacy download en_core_web_lg

deactivate
echo "build $VENVNAME"
