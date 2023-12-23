import os
import uuid
import streamlit as st
from streamlit_chatbox import ChatBox
from datetime import datetime
from chat.chat_client import ChatClient

from configs.model_config import HISTORY_LEN, TEMPERATURE

chat_box = ChatBox(
    assistant_avatar=os.path.join(
        "img",
        "chatbot_icon.png"
    )
)


def get_messages_history(history_len: int, content_in_expander: bool = False):
    '''
    返回消息历史。
    content_in_expander控制是否返回expander元素中的内容，一般导出的时候可以选上，传入LLM的history不需要
    '''

    def filter(msg):
        content = [x for x in msg["elements"] if x._output_method in ["markdown", "text"]]
        if not content_in_expander:
            content = [x for x in content if not x._in_expander]
        content = [x.content for x in content]

        return {
            "role": msg["role"],
            "content": "\n\n".join(content),
        }

    return chat_box.filter_history(history_len=history_len, filter=filter)


# st.title("ChatGPT-like clone")
st.set_page_config(
    "Chatbot",
    os.path.join("img", "chatbot_icon.png"),
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/YidaHu/chatbot',
        'Report a bug': "https://github.com/YidaHu/chatbot/issues",
        'About': "欢迎使用 ChatBot！"
    }
)
st.session_state.setdefault("conversation_ids", {})
st.session_state["conversation_ids"].setdefault(chat_box.cur_chat_name, uuid.uuid4().hex)
st.session_state.setdefault("file_chat_id", None)
default_model = 'azure'
now = datetime.now()
with st.sidebar:
    st.image(
        os.path.join(
            "img",
            "log.png"
        ),
        use_column_width=True
    )
    st.caption(
        f"""<p align="right">YidaHu    当前版本：1.0</p>""",
        unsafe_allow_html=True,
    )
    # 多会话
    index = 0
    conversation_name = 'default'
    chat_box.use_chat_name(conversation_name)
    conversation_id = st.session_state["conversation_ids"][conversation_name]

    index_dialogue = {
        "LLM 对话": "chat",
        "Agent 对话": "agent_chat"
    }
    index_agent = {
        "贴心小秘书": "assistant",
        "查天气": "weather",
        "订餐": "booking"
    }
    llm_list = ['openai', 'azure', 'baidu', 'glm']

    def on_dialogue_change():
        mode = st.session_state.dialogue_mode
        text = f"已切换到 {mode} 对话模式。"
        st.toast(text)

    def on_llm_change():
        mode = st.session_state.llm_mode
        st.toast(f"已切换到 {mode} 模型。")

    def on_agent_change():
        mode = st.session_state.agent_model
        text = f"已切换到 {mode} Agent。"
        st.toast(text)

    def llm_mode_format_func(x):
        return x

    dialogue_modes = ["LLM 对话", "Agent 对话"]
    if "dialogue_mode" not in st.session_state:
        st.session_state.dialogue_mode = dialogue_modes[0]
    dialogue_mode = st.selectbox("请选择对话模式：",
                                 dialogue_modes,
                                 index=0,
                                 format_func=llm_mode_format_func,
                                 on_change=on_dialogue_change,
                                 key="dialogue_mode",
                                 )
    if "llm_mode" not in st.session_state:
        st.session_state.llm_mode = llm_list[0]
    llm_mode = st.selectbox("请选择LLM模型：",
                            llm_list,
                            index,
                            format_func=llm_mode_format_func,
                            on_change=on_llm_change,
                            key="llm_mode",
                            )

    agent_list = ['贴心小秘书', '查天气', '订餐']
    if "agent_model" not in st.session_state:
        st.session_state.agent_model = agent_list[0]

    agent_model = st.selectbox(
        "请选择Agent：",
        agent_list,
        index=0,
        format_func=llm_mode_format_func,
        on_change=on_agent_change,
        key="agent_mode",
    )
    agent_name = st.session_state.agent_model
    temperature = st.slider("Temperature：", 0.0, 1.0, TEMPERATURE, 0.08)
    history_len = st.number_input("历史对话轮数：", 0, 20, HISTORY_LEN)
    if st.session_state.get("need_rerun"):
        st.session_state["need_rerun"] = False
        st.rerun()
    cols = st.columns(2)
    export_btn = cols[0]
    if cols[1].button(
            "清空对话",
            use_container_width=True,
    ):
        chat_box.reset_history()
        st.rerun()

    export_btn.download_button(
        "导出记录",
        "".join(chat_box.export2md()),
        file_name=f"{now:%Y-%m-%d %H.%M}_对话记录.md",
        mime="text/markdown",
        use_container_width=True,
    )

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("请问您想咨询什么问题？"):
    history = st.session_state.messages
    st.toast(history)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # for response in openai.ChatCompletion.create(
        #     model=st.session_state["openai_model"],
        #     messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        #     stream=True,
        # ):
        #     # 判断response.choices[0].delta.content存在与否，防止报错
        #     if response and response.choices and response.choices[0].delta and response.choices[0].delta.content:
        #         full_response += (response.choices[0].delta.content or "")
        #     message_placeholder.markdown(full_response + "▌")
        client = ChatClient()
        cur_dialogue_mode = index_dialogue[st.session_state.dialogue_mode]
        cur_llm_mode = st.session_state.llm_mode
        cur_agent_mode = index_agent[st.session_state.agent_model]
        for res in client.completion(prompt, cur_llm_mode, cur_agent_mode, cur_dialogue_mode, "DEFAULT"):
            full_response += (res or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
