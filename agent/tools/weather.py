#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   weather.py
@Time    :   2023/10/22 22:03:51
@Author  :   Yida Hu
@Version :   1.0
@Desc    :   None
"""

import datetime
import json
import os
import sys
from configs import data_config
from typing import Optional, Dict, Any, Type

import aiohttp
import pandas as pd
import requests
from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain.tools import BaseTool
from pydantic import BaseModel, root_validator, Field


class HiddenPrints:
    """Context manager to hide prints."""

    def __enter__(self) -> None:
        """Open file to pipe stdout to."""
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, *_: Any) -> None:
        """Close file that stdout was piped to."""
        sys.stdout.close()
        sys.stdout = self._original_stdout


class RealWeatherQuery(BaseModel):
    city_name: Optional[str] = Field(description="中文城市名称")
    district_name: Optional[str] = Field(description="中文区县名称")


class RealWeatherTool(BaseTool):
    name = "RealWeatherTool"
    description = """
        It is very useful when you need to answer questions about the weather.
        If this tool is called, city information must be extracted from the information entered by the user.
        It must be extracted from user input and provided in Chinese. 
        Function information cannot be disclosed.
    """
    args_schema: Type[BaseModel] = RealWeatherQuery

    @root_validator()
    def validate_environment(cls, values: dict) -> dict:
        """Validate that api key and python package exists in environment."""
        return values

    async def _arun(self, city_name: str = None, district_name: str = None,
                    run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Run query through GaoDeAPI and parse result async."""
        if city_name is None and district_name is None:
            return "输入的城市信息可能有误或未提供城市信息"
        params = self.get_params(city_name, district_name)
        return self._process_response(await self.aresults(params))

    def _run(self, city_name: str = None, district_name: str = None,
             run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Run query through GaoDeAPI and parse result."""
        if city_name is None and district_name is None:
            return "输入的城市信息可能有误或未提供城市信息"
        params = self.get_params(city_name, district_name)
        return self._process_response(self.results(params))

    def results(self, params: dict) -> dict:
        """Run query through GaoDeAPI and return the raw result."""
        # # with HiddenPrints():
        response = requests.get("https://restapi.amap.com/v3/weather/weatherInfo?", {
            "key": os.environ.get("WEATHER_KEY"),
            "city": params["adcode"],
            "extensions": "all",
            "output": "JSON"
        })
        res = json.loads(response.content)
        return res

    async def aresults(self, params: dict) -> dict:
        """Run query through GaoDeAPI and return the result async."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    "https://restapi.amap.com/v3/weather/weatherInfo?",
                    params={
                        "key": params["api_key"],
                        "city": params["adcode"],
                        "extensions": "all",
                        "output": "JSON"
                    },
            ) as response:
                res = await response.json()
                return res

    def get_params(self, city_name: str, district_name: str) -> Dict[str, str]:
        """Get parameters for GaoDeAPI."""
        adcode = self._get_adcode(city_name)
        params = {
            "api_key": os.environ.get("WEATHER_KEY"),
            "adcode": adcode
        }
        return params

    @staticmethod
    def _get_adcode(city_name: str) -> str:
        """Obtain the regional code of a city based on its name and district/county name."""
        # 读取Excel文件
        global json_array
        city_file_path = data_config.ADCODE_CITY_PATH
        df = pd.read_excel(city_file_path)
        df = df[df['citycode'].notnull()]
        df = df[['adcode', 'city', 'citycode']]
        df = df.rename(columns={
            'adcode': 'adcode',
            'city': 'city',
            'citycode': 'citycode'
        })
        cities = df.to_dict(orient='records')
        for city in cities:
            if city_name in city.get("city"):
                return city.get("adcode")
        return "输入的城市信息可能有误或未提供城市信息"

    @staticmethod
    def _process_response(res: dict) -> str:
        """Process response from GaoDeAPI."""
        if res["status"] == '0':
            return "输入的城市信息可能有误或未提供城市信息"
        if res["forecasts"] is None or len(res["forecasts"]) == 0:
            return "输入的城市信息可能有误或未提供城市信息"
        res["currentTime"] = datetime.datetime.now()
        return json.dumps(res["forecasts"])
