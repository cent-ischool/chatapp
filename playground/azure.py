from openai import AzureOpenAI

if __name__ == '__main__':
    ENDPOINT = "https://ist256-openai-instance.openai.azure.com/"
    API_KEY = "3cfc103aeff5407b842b277def615a1c"
    API_VERSION = "2024-05-01-preview"
    client = AzureOpenAI(azure_endpoint=ENDPOINT, api_key=API_KEY, api_version=API_VERSION)

    def stream_response(messages: list[str]):
        response = client.chat.completions.create(
            stream=True,
            messages=messages, 
            model="gpt4o")
        
        for chunk in response:
            if len(chunk.choices) > 0:
                yield chunk.choices[0].delta.content if chunk.choices[0].delta.content is not None else ""

    messages = [ {
        "role": "system",
        "content": "You are an AI assistant that helps people find information."
    }]

    query = "How many different ways can one cook an egg and what are the advantages of each?"
    response = ""
    messages.append({"role": "user", "content": query})
    for chunk in stream_response(messages):
        response +=chunk
        print(chunk, end="")

    # for chunk in stream_response(messages):
    #     print(chunk)

    # response = client.chat.completions.create(
    #     stream=True,
    #     messages=[{"role": "user", "content": "How many different ways can one cook an egg and what are the advantages of each?"}],
    #     model="gpt4o"
    # )

    # for chunk in response:
    #     if len(chunk.choices) > 0:
    #         yield chunk.choices[0].delta.content

    