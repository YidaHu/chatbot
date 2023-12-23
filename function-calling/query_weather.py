#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   query_weather_opanai.py
@Time    :   2023/06/16 01:06:38
@Author  :   Yida Hu
@Version :   1.0
@Desc    :   None
"""
import os
import json
import pprint
import openai
import requests
import pandas as pd

# OpenAI api key
openai.api_key = os.getenv("OPENAI_KEY")
# weather api key. https://lbs.amap.com/api/webservice/guide/api/weatherinfo
weather_key = os.getenv("WEATHER_KEY")


def get_cities():
    """Get cities info from excel file
    City information includes: adcode, city, citycode

    Returns:
        _type_: list
    """
    city_file_path = 'data/AMap_adcode_citycode_20210406.xlsx'
    df = pd.read_excel(city_file_path)
    df = df[df['citycode'].notnull()]
    df = df[['adcode', 'city', 'citycode']]
    df = df.rename(columns={
        'adcode': 'adcode',
        'city': 'city',
        'citycode': 'citycode'
    })
    df = df.to_dict(orient='records')
    return df


def get_weather(city_name: str):
    """Query weather info from amap api

    Args:
        city_name (str): city name

    Returns:
        _type_: list
    """
    url = "https://restapi.amap.com/v3/weather/weatherInfo?"

    params = {"key": weather_key, "city": "110000", "extensions": "all"}
    city_code = "110000"
    cities = get_cities()
    for city in cities:
        if city_name in city.get("city"):
            city_code = city.get("adcode")
            break
    params['city'] = city_code

    response = requests.get(url=url, params=params)
    pprint.pprint(response.json())
    return response.json().get("forecasts")[0].get("casts")


def run_conversation(question):
    """Run conversation with openai

    Args:
        question (_type_): User question

    Returns:
        _type_: OpenAI response
    """
    response = openai.ChatCompletion.create(
        model=os.getenv("OPENAI_MODEL_NAME"),
        messages=[{
            "role": "user",
            "content": question
        }],
        functions=[{
            "name": "get_weather",
            "description": "获取指定地区的当前天气情况",
            "parameters": {
                "type": "object",
                "properties": {
                    "city_name": {
                        "type": "string",
                        "description": "城市，例如：上海",
                    },
                },
                "required": ["city_name"],
            },
        }],
        function_call="auto",
    )
    print("response:", response)
    message = response["choices"][0]["message"]
    function_call = message.get("function_call")
    if function_call:
        arguments = function_call.get("arguments")
        arguments = json.loads(arguments)
        function_response = get_weather(city_name=arguments.get("city_name"), )
        function_response = json.dumps(function_response)

        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {
                    "role": "user",
                    "content": question
                },
                {
                    "role": "function",
                    "name": "get_weather1",
                    "content": function_response,
                },
            ],
        )
        print(second_response)
        return second_response
    else:
        return response


def main():
    question = "上海19号天气如何？"
    result = run_conversation(question)
    content = result.get("choices")[0].get("message").get("content")
    print("content:", content)


if __name__ == '__main__':
    main()
