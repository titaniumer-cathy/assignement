from openai import OpenAI
import os


class CallProvider:

    def openai(self, model_name, prompt):
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        completion = client.chat.completions.create(
        model=model_name,
        messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return(completion.choices[0].message.content)
    
    ### Todo: Add other providers