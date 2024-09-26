from openai import AzureOpenAI

class OpenAIAPI:
    def __init__(self, endpoint, api_key, api_version):
        self._client = AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version=api_version)
        self._messages = [{"role": "system", "content": "You are an AI assistant that helps people find information."}]

    def _add_to_messages(self, role, content):
        self._messages.append(
            {
              "role": role,
              "content": content
            }
        )

    @property
    def history(self):
        return self._messages
    
    @property
    def system_prompt(self):
        return [m for m in self._messages if m['role'] == "system"]

    @system_prompt.setter
    def system_prompt(self, value):
        index = [i for i, m in enumerate(self._messages) if m['role'] == "system"][0]
        self._messages[index]['content'] = value

    def record_response(self, assistant_reponse):
        self._add_to_messages("assistant", assistant_reponse)

    def stream_response(self, user_query, ignore_history=False):
        self._add_to_messages("user", user_query)
        if not ignore_history:
            messages = self._messages
        else:
            messages = self.system_prompt + [{"role": "user", "content": user_query}]

        response = self._client.chat.completions.create(
            stream=True,
            messages=messages, 
            model="gpt4o")
        
        for chunk in response:
            if len(chunk.choices) > 0:
                yield chunk.choices[0].delta.content if chunk.choices[0].delta.content is not None else ""


if __name__=='__main__':
    import os 
    ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
    API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
    API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION")
    ai = OpenAIAPI(endpoint=ENDPOINT, api_key=API_KEY, api_version=API_VERSION)
    ai.system_prompt = "You are an AI assistant that helps people find information, but you talk in jive."
    print(ai.system_prompt)
    while True:
        user_query = input("\nQuery? ")
        if user_query == "exit" or user_query == "quit":
            break
        reply = ""
        for chunk in ai.stream_response(user_query):
            reply += chunk
            print(chunk, end="")
        ai.record_response(reply)
    
    print(ai.history)
