#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   azure.py
@Time    :   2023/10/23 14:46:26
@Author  :   Yida Hu
@Version :   1.0
@Desc    :   None
"""

from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
import os
import datetime
from langchain.schema import SystemMessage
from langchain.chat_models import AzureChatOpenAI
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.chains import LLMMathChain
from agent.tools.weather import RealWeatherTool
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from llm.chat_model import ChatModel


class AzureChatModel(ChatModel):
    def __init__(self):
        super(AzureChatModel, self).__init__()
        self.llm = AzureChatOpenAI(
            openai_api_version="2023-07-01-preview",
            deployment_name='gpt-4-1106-Preview',
            openai_api_type="azure",
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
        )
        self.llm_math_chain = LLMMathChain.from_llm(llm=self.llm, verbose=True)

    def chat(self, message, agent):
        log = "Azure Response to: " + message
        print(log)
        res = agent.run(message)
        return res
