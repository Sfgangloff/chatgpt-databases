import openai
import re
import json 
  
openai.api_key = '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'

FILE = "molecular_biology.csv"
SUBJECT = "molecular biology"

text = open(FILE, "r").read()
words = text.split('\n')
words = words[1:-1]
word_list = ""
for word in words: 
    word_list += word + ","

prompt = f"For each of the words in the following list, give me 5 {SUBJECT} words related to it: {word_list}. Give your answer as a python dictionary"


messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]


messages.append({"role":"user","content":prompt})

chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    
reply = chat.choices[0].message.content
print(json.load(reply))
# with open("molecular_biology.csv",'a') as file:
    # dictionary = json.loads(reply)
    # for key in list(dictionary.keys()):
    #     for word in dictionary[key]:
    #         file.write(word+"\n")

# words = reply.split("\n")

# pattern = r'\d+\.\s+'

# filtered_list = [re.sub(pattern, "",word) for word in words]

# print(filtered_list)