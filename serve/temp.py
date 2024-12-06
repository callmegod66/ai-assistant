# -*- coding: utf-8 -*-
# @time    : 2024/11/5 11:29
# @author  : bingfei

import pandas as pd
from openai import OpenAI
import json


if __name__ == '__main__':
    client = OpenAI(
        api_key="sk-5886deba6f204750bd5b6dea86dc35d5",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务的base_url
    )
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': '你是谁？'}],
    )
    response = json.loads(completion.model_dump_json())
    print(response.get("choices")[0].get("message").get("content"))
