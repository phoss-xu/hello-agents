#!/usr/bin/python3
"""
# -*- coding: utf-8 -*-
# Author: Phoss.Xu
# Email: phosssuki@gmail.com
# CreateDate: 2026/04/14
# Description: 
"""

from tavily import TavilyClient
from hello_agent.config import TAVILY_API_KEY

def get_attraction(city: str, weather: str) -> str:
    """
    根据城市和天气，使用Tavily Search API 搜索并返回优化后的景点推荐。
    """
    api_key = TAVILY_API_KEY
    if not api_key:
        raise ValueError("Tavily API key is not configured")
    
    tavily = TavilyClient(api_key)

    query = f"'{city}' 在'{weather}'天气下最值得去的旅游景点推荐及理由"

    try:
        response = tavily.search(query=query, search_depth="basic", include_answer=True)

        if response.get("answer"):
            return response['answer']

        # 如果没有综合性回答，则格式化原始结果
        formatted_results = []
        for result in response.get("results", []):
            formatted_results.append(f"- {result.get('title', '无标题')}: {result.get('content', '无摘要')}")
        
        if not formatted_results:
            return "没有找到适合的景点推荐"
        
        return f"根据天气情况，{city}最值得去的旅游景点推荐及理由如下:\n" + "\n".join(formatted_results)
    except Exception as e:
        return f"错误: 搜索景点推荐失败 - {e}"

if __name__ == "__main__":
    print(get_attraction("北京", "晴天"))
