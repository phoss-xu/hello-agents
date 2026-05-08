#!/usr/bin/python3
"""
# -*- coding: utf-8 -*-
# Author: Phoss.Xu
# Email: phosssuki@gmail.com
# CreateDate: 2026/04/14
# Description: 
"""

import requests


def get_weather(city: str) -> str:
    """
    通过调用wttr.in API 查询真实的天气信息。
    """
    url = f"https://wttr.in/{city}?format=j1"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        current_condition = data["current_condition"][0]
        weather_desc = current_condition["weatherDesc"][0]["value"]
        temp_c = current_condition["temp_C"]

        return f"{city}的天气是{weather_desc}，温度是{temp_c}℃。"
    except requests.RequestException as e:
        return f"获取天气信息失败: {e}"
    
    except (KeyError, IndexError) as e:
        return f"错误:解析天气数据失败，可能是城市名称无效 - {e}"

    

if __name__ == "__main__":
    print(get_weather("北京"))