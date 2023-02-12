import requests
import pandas as pd
import os
from ETL.Functions import chunk_maker, extract_address
import time


# Get the value of the environment variable
azure_url = os.environ.get("azure_url")
azure_api_key = os.environ.get("azure_api_key")

# Get the list of files in the preprocessed folder
preprocessed_data_path = 'preprocessed_data/'
preprocessed_files = os.listdir(preprocessed_data_path)

# final_data_path
final_data_path = 'final_data/'
final_files = os.listdir(final_data_path)

print("preprocessed files are: ", preprocessed_files)


# setting the sleep time to 1 seconds
sleep_time = 1



# read in the preprocessed files and make chunks of 1000
for preprocessed_file in preprocessed_files:

    # only process csv files
    if not preprocessed_file.endswith(".csv"):
        continue

    # define preprocessed file name
    final_file = "addresses_" + preprocessed_file
    if final_file not in final_files:
        print("preprocessed file not found for: ", preprocessed_file, "\n and now working on them")
        # start the time counter
        start_time = time.time()
        # read in the preprocessed file
        df = pd.read_csv(preprocessed_data_path + preprocessed_file, sep=';').fillna('placeholder text')
        ## make chunks of 1000
        chunks = chunk_maker(df, 15)
        ## iterate over the chunks
        ner_chunks = []
        for chunk in chunks:
            try:
            # make the request
                resp = requests.post(
                    azure_url,
                    json={"input_data": chunk.to_dict(orient="split")},
                    headers={"Authorization": ("Bearer " + azure_api_key)},
                                    )
            except ValueError:
                print("ValueError: ", ValueError)
                continue
        
            # raise an error if the request was not successful
            resp.raise_for_status()
        
            # get the result
            ner_chunks.extend(resp.json())
            # print the time elapsed
            print("time elapsed: ", time.time() - start_time)
            print("Now sleeping for ", sleep_time, " seconds")
            time.sleep(sleep_time)

        # extract address from the result
        print("extracting addresses from the result")
        result = extract_address(ner_chunks)
        
        # save the result to a csv file
        print("saving the result to a csv file")
        result.to_csv(final_data_path+final_file, encoding='utf-8', sep=";", index=False)


# Done
print("I am done, thank you for your patience!. Check the final_data folder for the results")

