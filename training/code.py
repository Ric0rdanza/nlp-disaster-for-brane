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
import pandas as pd
import tensorflow as tf
import numpy as np
import pickle
import math

# The functions

def create() -> str:
    try:
        model = tf.keras.Sequential([
                tf.keras.layers.Embedding(10000, 16, input_length = 120),
                tf.keras.layers.GlobalAveragePooling1D(),
                tf.keras.layers.Dense(14, activation = "relu"),
                tf.keras.layers.Dense(1, activation = "sigmoid")
        ])
        model.compile(optimizer = "adam", loss = "binary_crossentropy", metrics = ["accuracy"])
        model.save(f"/data/model.h5")
        return "Create model saved at \"/data/model.h5\""
    except IOError as e:
        return "Error {e} ({e.errno})"

def fit(source: str) -> str:
    try:
        train_x = pickle.load(open(f"/data/padded_cleaned_{source}.pkl", "rb"))
        train_y = pd.read_csv(f"/data/{source}.csv")["target"]
        val_start = math.ceil(len(train_x) / 3)
        model = tf.keras.models.load_model(f"/data/model.h5")
        model.fit(train_x[0: val_start], train_y[0: val_start], epochs = 10, validation_data = (train_x[val_start:], train_y[val_start:]), verbose = 0)
        model.save(f"/data/model.h5")
        return "Trained model saved to \"/data/model.h5\""
    except IOError as e:
        return "Error: {e} ({e.errno})"

def predict(source: str) -> str:
    try:
        model = tf.keras.models.load_model(f"/data/model.h5")
        test = pickle.load(open(f"/data/padded_cleaned_{source}.pkl", "rb"))
        result = model.predict(test, verbose = 0)
        pred_list = []
        for val in result:
            if val > 0.5:
                pred_list.append(1)
            else:
                pred_list.append(0)
        submission = pd.read_csv(f"/data/sample_submission.csv")
        submission["target"] = pred_list
        submission.to_csv(f"/data/predicted.csv", index = False)
        return "Predictions saved to \"/data/predicted.csv\""
    except IOError as e:
        return "Error: {e} ({e.errno})"

def model_summary(name: str) -> str:
    try:
        model = tf.keras.models.load_model(f"/data/model.h5")
        with open(f"/data/{name}.txt", "w") as f:
            model.summary(print_fn = lambda x: f.write(x + '\n'))
        return "Model summary saved to \"/data/{name}.txt\""
    except IOError as e:
        return "Error： {e} ({e.errno})"

# The entrypoint of the script
if __name__ == "__main__":
    # Make sure that at least one argument is given, that is either 'write' or 'read'
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} write|read")
        exit(1)

    # If it checks out, call the appropriate function
    command = sys.argv[1]
    if command == "create":
        print(yaml.dump({ "contents": create() }))
    elif command == "fit":
        print(yaml.dump({ "contents": fit(os.environ["SOURCE"]) }))
    elif command == "predict":
        print(yaml.dump({ "contents": predict(os.environ["SOURCE"]) }))
    elif command == "model_summary":
        print(yaml.dump({ "contents": model_summary(os.environ["NAME"]) }))
    # Done!
