# GPTFineTuningCloningProfessor
My final project for my machine learning class which involved creating a digital clone of my professor to do a lecture on any subject in her style.

Presentation with example [here](https://www.canva.com/design/DAFwDr9fkmY/Pwx2M4g0UaEKbCcZ7bBhCw/view?utm_content=DAFwDr9fkmY&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=haaa8789343)!

Dr. Parlett's YouTube to see for reference on eery accuracy: https://www.youtube.com/@ChelseaPelleriti/videos

Generated script for lectures by testing from scratch LSTM as well as fine tuning a GPT model. The text data was scraped from Dr. Parlett's YouTube lectures using the Youtube API to grab the auto generated captions. This data was then cleaned and transformed into a prompt-answer JSON format to then be fed into fine tuning an instance of the davinci model using OpenAI's API. Tested out different variations of transformation to find most optimal outputs from fine tuned model.

Facecam generated using Synesthesia and inputting a still image captured from her videos.

Audio generated using audio clips from her YouTube as well as the fine tuned GPT generated script on ElevenLabs.

