#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   api.py
@Time    :   2023/10/22 21:03:43
@Author  :   Yida Hu
@Version :   1.0
@Desc    :   None
"""

from fastapi import FastAPI
from pydantic import BaseModel
from chat.completion import chat as chat_msg


class Item(BaseModel):
    question: str


app = FastAPI()


@app.post("/chatbot/chat")
async def process_json(item: Item):
    # 在这里你可以处理接收到的 JSON 数据，这里只是简单返回接收到的数据
    ret = chat_msg(item.question)
    return ret
