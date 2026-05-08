#!/usr/bin/python3
"""
# -*- coding: utf-8 -*-
# Author: Phoss.Xu
# Email: phosssuki@gmail.com
# CreateDate: 2026/04/14
# Description: 
"""
from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

class OpenAICompatibleClient:
    """
    一个用于调用兼容OPENAI接口的LLM服务的客户端
    """
    def __init__(self, model: str, api_key: str, base_url: str = "https://api.openai.com/v1"):
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, prompt: str, system_prompt: str) -> str:
        """调用LLM API来生成回应。"""
        print("正在调用LLM")

        try:
            messages = [
                ChatCompletionSystemMessageParam(role='system', content=system_prompt),
                ChatCompletionUserMessageParam(role='user', content=prompt),    
            ]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False
            )
            answer = response.choices[0].message.content
            print("大语言模型响应成功")
            return answer
        except Exception as e:
            print(f"错误: 调用LLM失败 - {e}")
            return "错误：调用语言模型服务时出错。"
    