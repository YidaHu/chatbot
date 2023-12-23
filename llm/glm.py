#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   glm.py
@Time    :   2023/10/23 14:47:52
@Author  :   Yida Hu
@Version :   1.0
@Desc    :   None
"""


from llm.chat_model import ChatModel


class GLMChatModel(ChatModel):
    def __init__(self):
        pass

    def chat(self, message):
        # 调用GLM的API
        response = "GLM Response to: " + message
        return response
