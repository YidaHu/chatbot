#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   chat_factory.py
@Time    :   2023/10/23 14:49:07
@Author  :   Yida Hu
@Version :   1.0
@Desc    :   None
"""
from llm.openai import OpenAIChatModel
from llm.azure import AzureChatModel
from llm.baidu import BaiduChatModel
from llm.glm import GLMChatModel


class ChatModelFactory:
    def get_chat_model(self, model_type):
        if model_type == "openai":
            return OpenAIChatModel()
        elif model_type == "azure":
            return AzureChatModel()
        elif model_type == "baidu":
            return BaiduChatModel()
        elif model_type == "glm":
            return GLMChatModel()
        else:
            raise ValueError("Unknown chat model type: {}".format(model_type))
