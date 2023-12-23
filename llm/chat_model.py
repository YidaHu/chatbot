#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   chat_model.py
@Time    :   2023/10/23 14:45:07
@Author  :   Yida Hu
@Version :   1.0
@Desc    :   None
"""

from abc import ABC, abstractmethod


class ChatModel(ABC):
    @abstractmethod
    def chat(self, prompt):
        pass
