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

def missing_value(filename: str, location: str, column_1: str, column_2: str, column_3: str, column_4: str, column_5: str) -> str:
    try:
        data = pd.read_csv(f"{location}/{filename}.csv")
        x = []
        y = []
        columns = [column_1, column_2, column_3, column_4, column_5]
        for col in columns:
            if col != "-":
                y.append(data[col].isnull().sum())
                x.append(col)
            else:
                break
        x = np.array(x)
        y = np.array(y)
        plt.bar(x, y)
        plt.savefig(f"{location}/missing_value_{filename}.png")
        plt.close("all")
        return "Figure saved to \"{location}/missing_value_{filename}.png\""
    except IOError as e:
        return f"ERROR: {e} ({e.errno})"

def number_of_words(filename: str, location: str, column: str, column_target: str) -> str:
    try:
        data = pd.read_csv(f"{location}/{filename}.csv")
        data["length"] = data[column].str.split().map(lambda x: len(x))
        plt.hist(data[data[column_target] == 0]["length"], alpha = 0.6, label = "No disaster")
        plt.hist(data[data[column_target] == 1]["length"], alpha = 0.6, label = "With disaster")
        plt.xlabel("number of words")
        plt.ylabel("frequency")
        plt.legend(loc = "upper right")
        plt.grid()
        plt.savefig(f"{location}/number_of_words_{filename}.png")
        plt.close()
        return "Figure saved to \"{location}/number_of_words_{filename}.png\""
    except IOError as e:
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
        print(yaml.dump({ "contents": missing_value(os.environ["FILENAME"], os.environ["LOCATION"], os.environ["COLUMN_1"], os.environ["COLUMN_2"], os.environ["COLUMN_3"], os.environ["COLUMN_4"], os.environ["COLUMN_5"]) }))
    elif command == "number_of_words":
        print(yaml.dump({ "contents": number_of_words(os.environ["FILENAME"], os.environ["LOCATION"], os.environ["COLUMN"], os.environ["COLUMN_TARGET"]) }))
    # Done!
