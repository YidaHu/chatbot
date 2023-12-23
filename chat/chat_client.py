#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   chat_client.py
@Time    :   2023/10/23 14:51:51
@Author  :   Yida Hu
@Version :   1.0
@Desc    :   None
"""
from agent.agent_factory import AgentFactory
from llm.chat_factory import ChatModelFactory


class ChatClient:
    def __init__(self):
        self.factory = ChatModelFactory()

    def completion(self, question, model_type, agent_type, chat_type, prompt_type):
        chat_model = self.factory.get_chat_model(model_type)
        agent = AgentFactory(agent_type, chat_type, prompt_type).get_agent(chat_model.llm)
        return chat_model.chat(question, agent)
