#%%
#Imports necesssary packages
import openai
import subprocess
import pandas as pd
import os
import random
#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

openai.api_key = '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'


#Inputs the script files
dfIN = pd.read_csv('VideoScriptsNoNoise.csv')

dfIN.head()


#%%
#Cleans all of the data

#Decided only to use CPSC 393 videos since there are no coding videos which may confuse gpt
#df = dfIN.drop(dfIN[dfIN.Class == 392].index)




df = dfIN.drop('Script', axis = 1)
#df = df.drop('Class', axis = 1)

#Get rid of all unnecessary title words (only need the topic)
df['Title'] = df['Title'].str.replace('CPSC 392','')
df['Title'] = df['Title'].str.replace('CPSC 393','')
df['Title'] = df['Title'].str.replace('In','in')
df['Title'] = df['Title'].str.replace('intro','Intro')
df['Title'] = df['Title'].str.replace('Lecture','')
df['Title'] = df['Title'].str.replace('|','')
df['Title'] = df['Title'].str.replace('\d+','')
df['Title'] = df['Title'].str.replace('Part','')
df['Title'] = df['Title'].str.replace('Pt.','')




#Decided to test without the part information
#Remove the part information
df['Title'] = df['Title'].str.replace('I','')
df['Title'] = df['Title'].str.replace('Neural Networks and Optimization V','Neural Networks and Optimization')
#Fixes lost I's
#df['Title'] = df['Title'].str.replace('ntro','Intro')


#Removes leading white space and newline characters
df['Title'] = df['Title'].str.strip()
df['ScriptNoNoise'] = df['ScriptNoNoise'].str.replace('\n', ' ')
df['ScriptNoNoise'] = df['ScriptNoNoise'].str.strip()
#df['ScriptNoNoise'] = (df['ScriptNoNoise'].str + ('END'))


#Creates the prompt to give gpt

#Turns out gpt doesn't like that long of a prompt and wants the simplest prompt possible
#df['Prompt'] = 'Give me a detailed and in depth lecture on ' + df['Title'] + ' in the style of my machine learning professor Chelsea'

#Changed to the following
df['Prompt'] = df['Title']

#Decided to remove Autoencoder lecture to test and compare generated lecture vs actual lecture
df = df.drop(44).reset_index()

#Remove first bit of intro text since it will be reintroduced later after more processing
df['ScriptNoNoise'] = df['ScriptNoNoise'].str.split(n=10).str[10]





#Creates a csv of only the data that gpt needs
prepared_data = df.loc[:,['Prompt','ScriptNoNoise']]





#%%
#USE THIS FOR RANDOM SEED GENERATION MODEL V2



#Need around 500 examples
#prompt + completion can't exceed 2048 tokens
#Decided to grab 500 examples of about 900 tokens

#Create a new df based on random samples of 900 tokens from the 

prompts = []
completions = []

tokenSize = 300

indices = range(df['Title'].size)
numOfSamples = df['Title'].size

numOfGenerations = range(500)

for num in numOfGenerations:
    
    randint = random.randint(0, numOfSamples - 1)
    
    sample = prepared_data.iloc[randint]
    
    title = sample['Prompt']
    prompts.append(title)
    
    text = sample['ScriptNoNoise']
    textTokenized = text.split()
    textSize = len(textTokenized)
    
    start = 0
    end = tokenSize
    
    if textSize > tokenSize:
        start = random.randint(0, textSize - tokenSize + 1)
        end = start + tokenSize
    
    seed_text = ' '.join(textTokenized[start:end])
    
    seed_text = seed_text + 'END'
    
    completions.append('hello and welcome to your ' + title + ' lecture ' + seed_text)


prepared_data_seeded = pd.DataFrame({'prompt':prompts, 'completion':completions})
prepared_data_seeded.to_csv('prepared_dataSeeded300NoAE.csv',index=False)

#%%
#USE THIS FOR SIMPLY CUTTING OFF LAST CHUNK OF LECTURE SO THAT GPT WILL ACCEPT IT MODEL V1


#Cut off at 1500 words
#Keep normal 50 lecture scripts

for row in range(prepared_data['ScriptNoNoise'].size):
    prepared_data['ScriptNoNoise'].iloc[row] = ' '.join(prepared_data['ScriptNoNoise'].iloc[row].split()[0:1500])
    
prepared_data['ScriptNoNoise'] = prepared_data['ScriptNoNoise'] + 'END'

prepared_data = prepared_data.rename(columns={"Prompt": "prompt", "ScriptNoNoise": "completion"})
prepared_data.to_csv('prepared_dataNoAE1500.csv',index=False)


#%%

## prepared_data.csv --> prepared_data_prepared.json
#Reformats into a json file
subprocess.run('openai tools fine_tunes.prepare_data --file prepared_data.csv --quiet'.split())

#%%

## Start fine-tuning
#Calls the api to actually fine tune
subprocess.run('openai api fine_tunes.create --training_file prepared_data_prepared.jsonl --model davinci --suffix "ChelseaLecturesV2"'.split())


#%%


#prompt MUST END WITH ' ->'
#maxTokens max is 256

#V1 IS GENERATED FROM SIMPLY CUTTING OFF ALL WORDS IN LECTURE PAST 1500 TOKENS
def generate_response_V1(prompt, temp, maxTokens):

    response = openai.Completion.create(
    model="davinci:ft-dylan:chelsealectures-2023-05-10-03-54-06", #ft-d4aLlShZHr81bjgHdsG9NCoH   ft-klhm:superhero-2023-02-01-14-56-48
    prompt=prompt,
    temperature=temp,
    max_tokens=maxTokens,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["END"]
    )
    
    return response

#V1 IS GENERATED FROM GRABBING 500 RANDOM SEEDS OF TEXT FROM THE LECTURES THAT ARE 300 TOKENS LONG
#HAD A LOT MORE EXAMPLES TO GIVE TO GPT, BUT THE SEEDS COULD BE SNATCHED FROM THE MIDDLE OF A LECTURE AND NOT QUITE MAKE SENSE
#WITHOUT THE SURROUNDING CONTEXT
def generate_response_V1(prompt, temp, maxTokens):

    response = openai.Completion.create(
    model="davinci:ft-dylan:chelsealectures-2023-05-10-03-54-06", #ft-d4aLlShZHr81bjgHdsG9NCoH   ft-klhm:superhero-2023-02-01-14-56-48
    prompt=prompt,
    temperature=temp,
    max_tokens=maxTokens,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["END"]
    )
    
    return response

#%%

test = generate_response_V1('Autoencoders ->',0.7,256)