import datetime
import os
from langchain.chat_models import AzureChatOpenAI

import requests
from flask import request, Flask
from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage

from agent.tools.weather import RealWeatherTool

llm = AzureChatOpenAI(
    openai_api_version=os.environ.get("OPENAI_API_VERSION"),
    azure_deployment=os.environ.get("AZURE_DEPLOYMENT"),
)

app = Flask(__name__)


# system 预设
template = """
Act as an AI versatile assistant, providing practical assistance and support to users through interaction. 
As an AI versatile assistant, you can utilize modern AI technology to automatically analyze user requests 
and inputs, and provide appropriate information and suggestions based on your needs. 
If there are no task parameters in the user's question, the tool will not be called. 
If the tool is called, it should extract as many parameters as possible from user input information or context.
The current time is：
""" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 添加缓存保存上下文记忆
memory = ConversationBufferMemory(memory_key="history", return_messages=True)

# 加载自定义工具
tools = [RealWeatherTool()]

agent_kwargs = {
    "system_message": SystemMessage(content=template)
}

agent_chain = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True, memory=memory,
                               agent_kwargs=agent_kwargs)


@app.route("/webhook/event", methods=['POST'])
def event():  # AI聊天
    # 接口请求参数
    json_data = request.get_json()
    print(memory.load_memory_variables({}))
    answer = agent_chain.run(json_data['question'])
    json_send_message = {"msgtype": "text", "text": {"content": answer}}
    print(json_send_message)
    return answer


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18888, debug=True)
