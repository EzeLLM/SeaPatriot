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
        self.pattern = r'\{\s*"latitude": \d+\.\d+,\s*"longitude": \d+\.\d+,\s*"course": \d+\.\d+,\s*"source": ".*?",\s*"destination": ".*?",\s*"speed": ".*?",\s*"status": ".*?",\s*"address": ".*?",\s*"eta": ".*?",\s*"last_report": ".*?",\s*"last_retrieved": \d+\.\d+\s*\}'
        # Dictionary to hold user-specific chat history
        self.user_histories = {}

    def get_user_history(self, chat_id):
        """Retrieve or initialize the conversation history for a user."""
        if chat_id not in self.user_histories:
            self.user_histories[chat_id] = FuncHub.open_json('dev/code/CONFIG/system_prompt.json')
        return self.user_histories[chat_id]

    def chat(self, user_input, ship_info, chat_id):
        """Chat method to handle user-specific conversations."""
        # Get the conversation history for the user
        messages = self.get_user_history(chat_id)
        
        # Update ship info in the initial system message
        if len(messages) == 1:
            messages[0]['content'] = messages[0]['content'].replace('<SHIP_INFO_JSON_TEXT>', ship_info)
        else:
            messages[0]['content'] = re.sub(self.pattern, ship_info, messages[0]['content'])
        
        # Add the user's message to the conversation
        messages.append({"role": "user", "content": user_input})
        
        # Get response from Groq
        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            max_tokens=256,
            temperature=0.5,
        )

        # Extract the assistant's response
        assistant_response = chat_completion.choices[0].message.content

        # Add the assistant's response to the conversation history
        messages.append({"role": "assistant", "content": assistant_response})

        # Save the updated history back for the user
        self.user_histories[chat_id] = messages

        return assistant_response
