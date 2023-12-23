#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   openai.py
@Time    :   2023/10/23 14:48:14
@Author  :   Yida Hu
@Version :   1.0
@Desc    :   None
"""

from llm.chat_model import ChatModel


class OpenAIChatModel(ChatModel):
    def __init__(self):
        pass

    def chat(self, message):
        # 调用OpenAI的API
        response = "OpenAI Response to: " + message
        return response
