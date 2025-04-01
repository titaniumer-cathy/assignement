import requests
import json
from call_provider import CallProvider

"""
This is a script for accessing prompts stored on AWS S3.
"""

if __name__== "__main__" :
    url = "https://d8ktjjqrs0.execute-api.us-east-1.amazonaws.com/my-lambda"
    headers = {
        "Content-Type": "application/json"
    }
    # prompt_type should be one of the file name in config_files
    data = {
        "prompt_type": "translation",
        "language": "French",
        "input": "How's your day?"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print("prompt:",response.text)
    if response.status_code == 200:
        answer = getattr(CallProvider(), 'openai')('gpt-4o-mini', response.text)
        print('answer',answer)
    else: 
        print("error handling prompt")