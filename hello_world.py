# -*- coding: utf-8 -*-
# @Time : 2022/12/29
# @Author : Dison
from typing import Optional

from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()


class CityInfo(BaseModel):
	province: str
	country: str
	is_affected: Optional[bool] = None  # 与bool区别是可以不传 null


# @app.get("/")
# def hello_world():
# 	return {"hellow": "world"}
#
#
# @app.get("/city/{city}")
# def result(city: str, query_string: Optional[str] = None):
# 	return {"city": city, "query_string": query_string}
#
#
# # 启动 uvicorn hello_world:app --reload
#
# @app.put("/city/{city}")
# def result(city: str, city_info: CityInfo):
# 	return {"city": city, "country": city_info.country, "is_affected": city_info.is_affected}


# 异步方式
@app.get("/")
async def hello_world():
	return {"hellow": "world"}


@app.get("/city/{city}")
async def result(city: str, query_string: Optional[str] = None):
	return {"city": city, "query_string": query_string}


# 启动 uvicorn hello_world:app --reload

@app.put("/city/{city}")
async def result(city: str, city_info: CityInfo):
	return {"city": city, "country": city_info.country, "is_affected": city_info.is_affected}
