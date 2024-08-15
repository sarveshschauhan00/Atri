from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def content_extractor(content):
    items = []
    flag = 0
    start, end = 0, 0
    for i in range(len(content)):
        if content[i:i+3] == "```":
            if flag == 0:
                start = i+3
                flag = 1
            elif flag==1:
                end = i
                flag = 2
            if flag==2:
                items.append(content[start:end])
                flag = 0
    return items


def gpt_bot(system_content, user_content, model="gpt-4o", temperature=0.2, max_tokens=4000):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content


def quick_bot(user_content, model="gpt-4o-mini", temperature=0.2, max_tokens=4000):
    system_content = """Quickly respond to the user query."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    # print(response)
    return response.choices[0].message.content