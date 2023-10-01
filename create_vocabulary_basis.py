import openai
import re
  
openai.api_key = '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'

SUBJECT = "molecular biology"

def create_vocabulary_basis(subject:str):

    messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]
    message = f"Give me a list of words related with {subject}"

    messages.append({"role":"user","content":message})

    chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
        
    reply = chat.choices[0].message.content
    terms = reply.split(',')
    text_to_add = ""
    for term in terms: 
        pattern = r'\d+\.\s+'
        text_to_add += re.sub(pattern, '', term) + '\n'
        text_to_add = text_to_add.lower()

    text_file = open("molecular_biology.csv", "w")
    text_file.write("WORD\n")
    text_file.write(text_to_add)
    text_file.close()

if __name__ == "__main__":
    create_vocabulary_basis(subject=SUBJECT)
