#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   attentive_secretary.py
@Time    :   2023/10/23 15:10:06
@Author  :   Yida Hu
@Version :   1.0
@Desc    :   None
"""

from langchain.agents import Tool
from langchain.chains import LLMMathChain
from agent.tools.weather import RealWeatherTool


class Assistant:
    def __init__(self, llm):
        self.llm = llm

    def tools(self):
        llm_math_chain = LLMMathChain.from_llm(llm=self.llm, verbose=True)
        tools = [
            Tool(
                name="Calculator",
                func=llm_math_chain.run,
                description="根据用户输入的数学问题，返回计算结果",
            ),
            Tool(
                name="Weather",
                func=RealWeatherTool().run,
                description="根据用户输入的城市信息，返回该城市的天气信息",
            ),
        ]
        return tools
