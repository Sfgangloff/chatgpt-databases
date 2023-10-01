import openai
  
openai.api_key = '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'

FILE = "molecular_biology.csv"
SUBJECT = "molecular biology"

text = open(FILE, "r").read()
words = text.split('\n')
words = words[1:-1]

prompts = []

for word in words:
    prompts.append(f"I am a {SUBJECT} student. Evaluate the difficulty of understanding {word} with a number between 0 and 20")

replies = []

messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]

for prompt in prompts:
    message = prompt

    messages.append({"role":"user","content":message})

    chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
        
    reply = chat.choices[0].message.content
    replies.append(reply)

for reply in replies:
    print(reply)