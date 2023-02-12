# Extracting Address from a Earthquake Aid Requests

This repo contains the code for the project **extracting the address from the earthquake aid requests**. Major two consecutive earthquakes hit southeast Turkey and Northern Syria on 06.02.2023. The earthquakes caused a lot of damage to the infrastructure and the people. The people who are in need of aid are posting their requests on `twitter`. The requests are only in ``Turkish``. <br> <br>

 The requests are in the form of tweets. The requests ideally contain the location of the person who is in need of aid. But of course, there are numerous tweets that contain location but those locations are not mentioning a rubble, but some sort of other needs like logistics, food, water, etc. <br> <br> 


 ## project structure

> **raw_data** : contains untransformed data <br>
> **preprocessed_data** : contains transformed data <br>
> **final_data** : contains the final data <br>
>> ETL:
>> 1. **clean_tweets.py** : gets the untransformed data and cleans it. Then stores >> it under preprocessed_data
>> 2. **Functions.py** : contains the functions used in the project
>>
> **api_caller.py** : contains the code for the api call to the model
 <br> <br>
 

 ## Data

 Data source is Twitter. Data was gathered by researchistanbul.com via Twitter API.

## Data Preprocessing
Tweets are cleared from #hashtags, @mentions and lowercased.

## Named Entity Recognition
For named entitiy recognition Huggingface's transformers library is used. The model used is `deprem-ml/deprem-ner-mdebertav3` which is a custom model specifically finetuned for address retrieveal purposes by **deprem-ml** team. 

### API Call
> To be filled by `Arda`

In order to bypass the rate limits and speed up the process, the huggingface model is being stored in a private resource group on Azure cloud.

## Results
The resulting datasets can be accessed at final_data folder.


## Contributors
- [Arda](https://github.com/aytekinar)
- [Melisa](https://github.com/melisaaltinsoy)
- [Giz]()
- [Tugberk](https://github.com/tugberkcapraz)


