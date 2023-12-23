

from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
import os
import datetime
from langchain.schema import SystemMessage
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from configs.prompt_config import PROMPT_TEMPLATES
from agent.assistant import Assistant


class AgentFactory:
    def __init__(self, agent_type, chat_type, prompt_type):
        self.agent_type = agent_type
        self.chat_type = chat_type
        self.prompt_type = prompt_type

    def get_agent(self, llm):
        if self.agent_type == "assistant":
            tool_list = Assistant(llm).tools()
        else:
            raise ValueError("Unknown agent type: {}".format(self.agent_type))

        agent_kwargs = {
            "system_message": SystemMessage(content=PROMPT_TEMPLATES["CHAT"]["DEFAULT"])
        }
        memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

        agent = initialize_agent(
            tool_list,
            llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            agent_kwargs=agent_kwargs,
            memory=memory,
        )
        return agent
