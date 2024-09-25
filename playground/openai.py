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
            "max_tokens": max_tokens        
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
        self.payload['stream'] = False
        self._append_message_to_payload("user", user_text)
        response = requests.post(self.endpoint, headers=self.headers, json=self.payload)
        response.raise_for_status()
        data = response.json()
        assistant_text = data['choices'][0]['message']['content']
        self._append_message_to_payload("assistant", assistant_text)
        return assistant_text

    def stream_response(self, user_text):
        self.payload['stream'] = True
        self._append_message_to_payload("user", user_text)
        s = requests.Session()
        with s.post(self.endpoint, headers=self.headers, json=self.payload, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    data = line.decode('utf-8')
                    print(data['data'])
                    # assistant_text = data['choices'][0]['message']['content']
                    # self._append_message_to_payload("assistant", assistant_text)
                    # return assistant_text
                
        # response.raise_for_status()
        # data = response.json()
        # assistant_text = data['choices'][0]['message']['content']
        # self._append_message_to_payload("assistant", assistant_text)
        # return assistant_text


if __name__=='__main__':
    pass 

    