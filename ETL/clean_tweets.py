import pandas as pd
import os
from Functions import preprocess_tweet

''' This script goes through the raw tweets folder, takes each csv file and cleans the tweet text. It then saves the cleaned tweets in a new folder called preprocessed_data'''

# get the folder paths
raw_data_path = 'raw_data/'
preprocessed_data_path = 'preprocessed_data/'


# get the list of files in the folders
raw_files = os.listdir(raw_data_path)
preprocessed_files = os.listdir(preprocessed_data_path)


# as the other csv's have no headers, we need to infer the column names from the csv with headers
inferred_columns = pd.read_csv('raw_data/eq_1.csv', sep=';').columns

# now checking for each raw file if there is a preprocessed file
for raw_file in raw_files:
    # only process csv files
    if not raw_file.endswith(".csv"):
        continue
    # define preprocessed file name
    preprocessed_file = "preprocessed_" + raw_file

    # check if preprocessed file exists
    if preprocessed_file not in preprocessed_files:
        print("preprocessed file not found for: ", raw_file)
        # try to read the csv file
        try:
            df = pd.read_csv(raw_data_path + raw_file, sep=';', usecols=['Tweet Text']).rename(columns={'Tweet Text': 'input'})
            # preprocess the tweet
            df["input"] = df["input"].apply(preprocess_tweet)
            # save the preprocessed file
            df.to_csv(preprocessed_data_path + preprocessed_file, encoding='utf-8', sep=";", index=False)
        # the exception is thrown when the csv file has no headers. Use inferred columns in this case
        except:
            df = pd.read_csv(raw_data_path + raw_file, sep=';',header = None, names=inferred_columns, usecols=["Tweet Text"]).rename(columns={'Tweet Text': 'input'})
            # preprocess the tweet
            df["input"] = df["input"].apply(preprocess_tweet)
            # save the preprocessed file
            df.to_csv(preprocessed_data_path + preprocessed_file, encoding='utf-8', sep=";", index=False)


