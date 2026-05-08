#!/usr/bin/python3
"""
# -*- coding: utf-8 -*-
# Author: Phoss.Xu
# Email: phosssuki@gmail.com
# CreateDate: 2026/04/14
# Description: 
"""
import re
from hello_agent.llm import OpenAICompatibleClient
from hello_agent.config import OPENAI_MODEL, OPENAI_API_KEY, OPENAI_BASE_URL
from hello_agent.tools import available_tools
from hello_agent.prompt import AGENT_SYSTEM_PROMPT

def main():
    """主函数"""
    llm = OpenAICompatibleClient(
        model=OPENAI_MODEL,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL
    )

    # ---- 2. 初始化 ---
    user_prompt = "你好，请帮我查询下今天深圳的天气，然后根据天气推荐一个合适的旅游景点。"
    prompt_history = [f"用户请求: {user_prompt}"]

    print(f"用户输入: {user_prompt}\n" + "="*32)

    # --- 3.运行主循环 ---
    for i in range(5):
        print(f"--- 循环 {i+1} ---\n")
        # 3.1 构建Prompt
        full_prompt = "\n".join(prompt_history)

        # 3.2 调用LLM进行下思考
        llm_output = llm.generate(full_prompt, AGENT_SYSTEM_PROMPT)
        match = re.search(r'(Thought:.*?Action:.*?)(?=\n\s*(?:Thought:|Action:|Observation:)|\Z)', llm_output, re.DOTALL)
        if match:
            truncated = match.group(1).strip()
            if truncated != llm_output.strip():
                llm = truncated
                print("已截断多余的 Thought-Action 对")
            print(f"LLM Output:\n{llm_output}\n")
            prompt_history.append(llm_output)
        
        # 解析并执行
        action_match = re.search(f"Action:(.*)", llm_output, re.DOTALL)
        if not action_match:
            observation = "错误: 未能解析到 Action 字段。请确保你的回复严格遵循 'Thought: ... Action: ...' 的格式。"
            observation_str = f"Observation: {observation}"
            print(f"{observation_str}\n" + "="*40)
            prompt_history.append(observation_str)
            continue
        action_str = action_match.group(1).strip()
        if action_str.startswith("Finish"):
            finish_match = re.match(r"Finish\[(.*)\]\Z", action_str, re.DOTALL)
            final_answer = finish_match.group(1) if finish_match else action_str
            print(f"任务完成，最终答案: {final_answer}")
            break
        
        tool_name = re.search(r"(\w+)\(", action_str).group(1)
        args_str = re.search(r"\((.*)\)", action_str).group(1)
        kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_str))

        if tool_name in available_tools:
            observation = available_tools[tool_name](**kwargs)
        else:
            observation = f"错误:未定义的工具 '{tool_name}'"

        # 3.4. 记录观察结果
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)

        
        
