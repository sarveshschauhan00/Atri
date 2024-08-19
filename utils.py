from openai import OpenAI
from anthropic import Anthropic
import os
import json
import re


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
anthropic_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

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
            {"role": "user", "content": user_content}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content


def quick_bot(user_content, model="gpt-4o-mini", temperature=0.0, max_tokens=4096):
    system_content = """Quickly respond to the user query. Your output will be a json based on the user query."""
    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    # print(response)
    return json.loads(response.choices[0].message.content)


def claude_bot(data, temperature=0.7):
    response = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": data}
        ],
        # system=system_content,
        temperature=temperature
    )
    return response.content[0].text


def claude_bot2(system_content, data, temperature=0.7):
    response = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": data}
        ],
        system=system_content,
        temperature=temperature
    )
    return response.content[0].text

def tag_extractor(content, tag):
    return re.findall(fr'<{tag}>(.*?)</{tag}>', content, re.DOTALL)