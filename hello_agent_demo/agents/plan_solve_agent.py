# -*- coding: utf-8 -*-
"""
File: plan_solve_agent.py
Author: Auto Header
Date: 2026-04-29
Copyright (c) 2026 Auto Header
"""

import ast

from hello_agent_demo.prompts.plan_execute import (
    EXECUTOR_PROMPT_TEMPLATE,
    PLANNER_PROMPT_TEMPLATE,
)


class Planner:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def plan(self, question):
        """
        根据用户问题生成一个行动计划。
        """
        prompt = PLANNER_PROMPT_TEMPLATE.format(question=question)

        # 为了生成计划，我们构建一个简单的消息列表
        messages = [
            {"role": "user", "content": prompt},
        ]
        print("--- 正在生成计划 ---")
        # 使用流式输出来获取完整的计划
        response_text = self.llm_client.think(messages=messages) or ""

        print(f"✅ 计划已生成:\n{response_text}")

        # 解析LLM输出的列表字符串
        try:
            # 找到```python和```之间的内容
            plan_str = response_text.split("```python")[1].split("```")[0].strip()
            # 使用ast.literal_eval来安全地执行字符串，将其转换为Python列表
            plan = ast.literal_eval(plan_str)
            return plan if isinstance(plan, list) else []
        except (ValueError, SyntaxError, IndexError) as e:
            print(f"❌ 解析计划时出错: {e}")
            print(f"原始响应: {response_text}")
            return []
        except Exception as e:
            print(f"❌ 解析计划时发生未知错误: {e}")
            return []


class Executor:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def execute(self, question, plan, history=[]):
        """
        根据计划和历史执行下一步。
        """
        history = ""  # 用于存储历史步骤和结果的字符串
        response_text = ""
        print("\n--- 正在执行计划 ---")
        for i, step in enumerate(plan):
            print(f"\n->正在执行步骤{i + 1}/{len(plan)}: {step}")
            prompt = EXECUTOR_PROMPT_TEMPLATE.format(
                question=question,
                plan=plan,
                history=history,
                current_step=step,
            )

            messages = [
                {"role": "user", "content": prompt},
            ]

            response_text = self.llm_client.think(messages=messages) or ""

            # 更新历史记录，为下一步做准备
            history += f"\n步骤{i + 1}: {step}\n结果: {response_text}\n\n"
            print(f"✅ 步骤 {i + 1} 已完成，结果: {response_text}")

        # 循环结束后，最后一步的响应就是最终答案
        final_answer = response_text
        return final_answer


class PlanAndSolveAgent:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.planner = Planner(llm_client)
        self.executor = Executor(llm_client)

    def solve(self, question):
        """
        运行智能体的完整流程:先规划，后执行。
        """
        print(f"\n--- 开始处理问题 ---\n问题: {question}")
        # 1. 调用规划器生成计划
        plan = self.planner.plan(question)

        # 检查计划是否成功生成
        if not plan:
            print("\n--- 任务终止 --- \n无法生成有效的行动计划。")
            return

        # 2. 调用执行器执行计划
        final_answer = self.executor.execute(question, plan)

        print(f"\n--- 任务完成 ---\n最终答案: {final_answer}")


if __name__ == "__main__":
    from hello_agent_demo.LLM.hello_agent_llm import HelloAgentsLLM

    llm_client = HelloAgentsLLM()
    plan_and_solve_agent = PlanAndSolveAgent(llm_client)
    question = "一个水果店周一卖出了15个苹果。周二卖出的苹果数量是周一的两倍。周三卖出的数量比周二少了5个。请问这三天总共卖出了多少个苹果？"
    plan_and_solve_agent.solve(question)
