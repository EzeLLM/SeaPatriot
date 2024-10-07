import os
from groq import Groq
from dotenv import load_dotenv
import FuncHub
import re

load_dotenv()
GROQ_API_KEY = os.getenv('GROQAPI')

    

class Chatbot:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = "llama3-groq-70b-8192-tool-use-preview"  # You can change this to your preferred Groq model
        self.messages = FuncHub.open_json('dev/code/CONFIG/system_prompt.json')
        self.pattern = r'\{\s*"latitude": \d+\.\d+,\s*"longitude": \d+\.\d+,\s*"course": \d+\.\d+,\s*"source": ".*?",\s*"destination": ".*?",\s*"speed": ".*?",\s*"status": ".*?",\s*"address": ".*?",\s*"eta": ".*?",\s*"last_report": ".*?",\s*"last_retrieved": \d+\.\d+\s*\}'
        self.first = True
    def chat(self, user_input,ship_info):
        print(ship_info)
        # Add user message to the conversation history
        if self.first:
            self.messages[0]['content'] = self.messages[0]['content'].replace('<SHIP_INFO_JSON_TEXT>',ship_info)
            self.first = False
        else :
            self.messages[0]['content'] = re.sub(self.pattern, ship_info, self.messages[0]['content'])

        self.messages.append({"role": "user", "content": user_input})

        # Get response from Groq
        chat_completion = self.client.chat.completions.create(
            messages=self.messages,
            model=self.model,
            max_tokens=256,
            temperature=0.5,
        )

        # Extract the assistant's response
        assistant_response = chat_completion.choices[0].message.content

        # Add assistant's response to the conversation history
        self.messages.append({"role": "assistant", "content": assistant_response})

        return assistant_response

if __name__ == "__main__":
    chatbot = Chatbot()
    print("Simple Groq Chatbot. Type 'quit' to exit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        
        response = chatbot.chat(user_input,"""{
    "latitude": 37.86498,
    "longitude": 23.53933,
    "course": 337.2,
    "source": "Trieste, Italy",
    "destination": "Piraeus Anch., Greece",
    "speed": "0.0 kn",
    "status": "At anchor",
    "address": "Attica, Greece",
    "eta": "ATA: Oct 07, 02:59 UTC",
    "last_report": "Oct 07, 2024 10:13 UTC",
    "last_retrieved": 1728296210.6054919
}""")
        print(f"Chatbot: {response}")

    print("Goodbye!")