#!/usr/bin/env python3

# CODE.py
#   by Lut99
#
# Created:
#   23 May 2022, 16:23:31
# Last edited:
#   23 May 2022, 16:35:01
# Auto updated?
#   Yes
#
# Description:
#   Contains the code for the third tutorial in the Brane: The User Guide
#   (https://wiki.enablingpersonalizedinterventions.nl/user-guide/software-engi
#   neers/filesystem.md).
#
#   This package implements a very simple "filesystem", which can write and
#   read content to the shared `/data` folder.
#


# Imports
import os
import sys
import yaml
import requests
import pandas as pd
import tensorflow as tf
import numpy as npi
import pickle
import re


# The functions

def cleaning(source: str) -> str:
    try:
        data = pd.read_csv(f"/data/{source}.csv")
        
        def clean_text(text: str):
            text = text.lower()
            text = re.sub("\[.*?\]", "", text)
            text = re.sub("https?://\S+|www\.\S+", "", text)
            text = re.sub("<.*?>+", "", text)
            text = re.sub("\n", "", text)
            text = re.sub("\w*\d\w*", "", text)
            return text
        
        data['text'] = data['text'].apply(lambda x: clean_text(x))
        data.to_csv(f"/data/cleaned_{source}.csv")
        return "Cleaned data saved to \"cleaned_{source}.csv\""
    except IOError as e:
        return f"ERROR: {e} ({e.errno})"

def processing(model: str) -> str:
    try:
        data = pd.read_csv(f"/data/{model}.csv")
        sentences = data["text"].fillna("")
        vocab_size = 1000
        embedding_dim = 16
        max_length = 120
        trunc_type = "post"
        oov_tok = "<OOV>"

        tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words = 10000, oov_token = "<OOV>")
        tokenizer.fit_on_texts(sentences)
        sequence = tokenizer.texts_to_sequences(sentences)
        padded = tf.keras.preprocessing.sequence.pad_sequences(sequence, maxlen = 120, truncating = "post")
        pickle.dump(padded, open(f"/data/padded_{model}.pkl", "wb"))
        return "Preprocessed data saved to \"/data/padded_{model}.pkl\""
    except IOError as e:
        return "ERROR: {e} ({e.errno})"

# The entrypoint of the script
if __name__ == "__main__":
    # Make sure that at least one argument is given, that is either 'write' or 'read'
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} write|read")
        exit(1)

    # If it checks out, call the appropriate function
    command = sys.argv[1]
    if command == "cleaning":
        print(yaml.dump({ "contents": cleaning(os.environ["SOURCE"]) }))
    elif command == "processing":
        print(yaml.dump({ "contents": processing(os.environ["MODEL"]) }))
    # Done!:
