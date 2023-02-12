import pandas as pd
import numpy as np
import re

'''This script contains helper functions for reading and cleaning the tweets'''

def preprocess_tweet(tweet):
    '''This function takes a tweet as input and returns a preprocessed tweet.
    
    Context:
    - I checked for several text cleaning options to evaluate their impact on the subsequent NER tagging step.
    The hashtag removal and @handle removal are vital. If they are not removed, the NER tagging is influenced by the presence of the
    names in @handle and #hashtag.
    - I am not sure about the impact of lowercasing but thats standard preprocessing task
    - I put extra spaces between words to make sure that the NER tagging does not get confused by words that are concatenated. 
    you can uncomment the url removal and punctuation removal to see the impact on the NER tagging.

    input: tweet (string)
    output: tweet (string)'''
    # remove hashtags
    tweet = re.sub(r'#\w+', '', tweet)
    
    # remove mentions
    tweet = re.sub(r'@\w+', '', tweet)

    ## lowercase
    tweet = tweet.lower()

    # remove urls
    #tweet = re.sub(r'http\S+', '', tweet)

    #remove punctuation and exclamations
    #tweet = re.sub(r'[^\w\s]', '', tweet)

    # put extra space between words
    tweet = re.sub(r'\s+', '    ', tweet)
    
    return tweet


def chunk_maker(df, N):
    '''This function takes a dataframe and splits it into N chunks.
    input: df (dataframe), N (int)
    output: chunks (list)'''
    chunks = []
    chunk_size = int(len(df)/N)
    for i in range(N):
        chunks.append(df.iloc[i*chunk_size:(i+1)*chunk_size])
    return chunks


def extract_address(input_object):
    '''This function takes the output of the NER tagging constructs the dataframe from NER-tags and NER-words.
    input: input_object (column)
    output: df (dataframe)'''

    # construct the empty dataframe
    df = pd.DataFrame()

    for i in range(len(input_object)):
        temp_df = pd.json_normalize(input_object[i]["token"])

        try:
            # strip the B- and I- from the entity column
            temp_df['entity'] = temp_df['entity'].str.replace('B-', '')
            temp_df['entity'] = temp_df['entity'].str.replace('I-', '')
            # clean the hashtags
            temp_df['word'] = temp_df['word'].str.replace('##', '')
            temp_df['word'] = temp_df['word'].str.replace(' ##', '')
            
        except KeyError:
            # if there is no entity column, fill it with NaN
            temp_df['entity'] = np.nan
            temp_df["word"] = np.nan

        # group by entity and join the words
        temp_df = temp_df.groupby('entity').agg({'word': ' '.join}).reset_index()
        # convert the orientation to horizontal
        temp_df = temp_df.T
        # make the entity header
        temp_df.columns = temp_df.iloc[0]
        # drop the entity row
        temp_df = temp_df.drop('entity')
        # concat the temp_df to the main df
        df = pd.concat([df, temp_df], axis=0)
        # the NaNs are replaced with empty strings
        df.fillna("", inplace=True)

    df.reset_index(inplace=True)
    return df




