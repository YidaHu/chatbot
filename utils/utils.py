#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   utils.py
@Time    :   2023/10/19 23:53:14
@Author  :   Yida Hu
@Version :   1.0
@Desc    :   None
"""


def get_prompt_template(type: str, name: str):
    '''
    加载模板内容
    '''

    from configs import prompt_config
    import importlib
    importlib.reload(prompt_config)
    return prompt_config.DEFAULT_PROMPT
