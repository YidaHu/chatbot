#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   baidu.py
@Time    :   2023/10/23 14:47:21
@Author  :   Yida Hu
@Version :   1.0
@Desc    :   None
"""


from llm.chat_model import ChatModel


class BaiduChatModel(ChatModel):
    def __init__(self):
        pass

    def chat(self, message):
        # 调用Baidu的API
        response = "Baidu Response to: " + message
        return response
