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


llm = AzureChatOpenAI(
    openai_api_type="azure",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()],
)

llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
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
# tools = [RealWeatherTool()]

template = """
充当AI万能助手，通过交互为用户提供实际的帮助和支持。 
作为AI万能助手，您可以利用现代AI技术自动分析用户请求 
和输入，并根据您的需要提供适当的信息和建议。 
如果用户的问题中没有任务参数，则不会调用该工具。 
如果调用该工具，它应该从用户输入信息或上下文中提取尽可能多的参数。 
当前时间为:
""" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
agent_kwargs = {
    "system_message": SystemMessage(content=template)
}
memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    agent_kwargs=agent_kwargs,
    memory=memory,
)


def chat(prompt: str, temperature=0.8):
    res = agent.run(prompt)
    return res
