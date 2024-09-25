import requests
import os
import json

class OpenAIAPI:
    def __init__(self, endpoint, api_key) -> None:
        self.endpoint = endpoint
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "api-key": api_key
        }
        self.system_text = "you are a helpful assistant"
        self.payload = {}

    def start_conversation(self, temperature=0.5, top_p=0.95, max_tokens=1000):
        self.payload = {
            "messages": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "text",
                            "text": self.system_text
                        }
                    ]
                }
            ],
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens,
            "stream": False
        }

    def _append_message_to_payload(self, role, content):
        self.payload['messages'].append(
            {
              "role": role,
              "content": [
                  {
                      "type": "text",
                      "text": content
                  }
              ]
            }
        )

        
    def generate_response(self, user_text):
        self._append_message_to_payload("user", user_text)
        response = requests.post(self.endpoint, headers=self.headers, json=self.payload)
        response.raise_for_status()
        data = response.json()
        assistant_text = data['choices'][0]['message']['content']
        self._append_message_to_payload("assistant", assistant_text)
        return assistant_text
    

if __name__=='__main__':
    pass
    # Configuration
    # ENDPOINT = os.environ.get("OPENAI_ENDPOINT")
    # API_KEY = os.environ.get("OPENAI_API_KEY")

    # ai = OpenAIAPI(ENDPOINT, API_KEY)
    # ai.system_text = "You are a helpful AI assistant who speaks in old english."
    # ai.start_conversation()
    # print("?? Can you do math?")
    # response = ai.generate_response("Can you do math?")
    # print(response)
    # print("?? What is 9 times 9?")
    # response = ai.generate_response("What is 9 times 9?")
    # print(response)
    # print("?? Can you substract 10 from the last number?")
    # response = ai.generate_response("Can you substract 10 from the last number?")
    # print(response)
    