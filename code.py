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
import matplotlib.pyplot as plt
import numpy as np

# The functions

def missing_value(source: str) -> str:
    try:
        if source == "train":
            data = pd.read_csv(f"/data/train.csv")
        elif source == "test":
            data = pd.read_csv(f"/data/test.csv")
        else:
            return f"Source Error"
        missing_cols = ["keyword", "location"]
        x = np.array(missing_cols)
        y = np.array([data["keyword"].isnull().sum(), data["location"].isnull().sum()])
        plt.bar(x, y)
        plt.savefig(f"/data/missing_value_{source}.png")
        plt.close("all")
        return "Figure saved to \"/data/missing_value_{source}.png\""
    except IOError as e:
        return f"ERROR: {e} ({e.errno})"

def number_of_words(source: str) -> str:
    try:
        data = pd.read_csv(f"/data/{source}.csv")
        data["length"] = data["text"].str.split().map(lambda x: len(x))
        plt.hist(data[data["target"] == 0]["length"], alpha = 0.6, label = "No disaster")
        plt.hist(data[data["target"] == 1]["length"], alpha = 0.6, label = "With disaster")
        plt.xlabel("number of words")
        plt.ylabel("frequency")
        plt.legend(loc = "upper right")
        plt.grid()
        plt.savefig(f"/data/number_of_words_{source}.png")
        plt.close()
        return "Figure saved to \"/data/number_of_words_{source}.png\""
    except:
        return f"Error: {e} ({e.errno})"



# The entrypoint of the script
if __name__ == "__main__":
    # Make sure that at least one argument is given, that is either 'write' or 'read'
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} write|read")
        exit(1)

    # If it checks out, call the appropriate function
    command = sys.argv[1]
    if command == "missing_value":
        print(yaml.dump({ "contents": missing_value(os.environ["SOURCE"]) }))
    elif command == "number_of_words":
        print(yaml.dump({ "contents": number_of_words(os.environ["SOURCE"]) }))
    # Done!
