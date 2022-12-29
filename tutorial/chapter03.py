# -*- coding: utf-8 -*-
# @Time : 2022/12/29
# @Author : Dison
from enum import Enum
from typing import Optional, List
from datetime import date

from fastapi import APIRouter, Path, Query, Cookie, Header

from pydantic import BaseModel, Field

app03 = APIRouter()

""" 路径参数和数字验证"""


@app03.get("/path/parameters")
def path_params01():
	return {"message": "this is message"}


@app03.get("/path/{parameters}")
def path_params01(parameters: str):
	return {"message": parameters}


class CityName(str, Enum):
	Beijing = "Beijing China"
	Shanghai = "Shanghai China"


@app03.get("/enum/{city}")  # 枚举类型参数
async def latest(city: CityName):
	if city == CityName.Shanghai:
		return {"city_name": city, "confiremd": 1492, "death": 7}
	if city == CityName.Beijing:
		return {"city_name": city, "confiremd": 971, "death": 9}
	return {"city_name": city, "latest": "unknown"}


@app03.get("/files/{file_path:path}")  # 通过path paramters传递文件路径
def filepath(file_path: str):
	return f"the file path is {file_path}"


# 路径参数验证
@app03.get("path/{num}")
def path_params_validate(num: int = Path(..., title="your number", description="不可描述", ge=1, le=10)):
	return {"num": num}


""" 查询参数和字符串验证"""


@app03.get("/query")
def page_limit(page: int = 1, limit: Optional[int] = None):
	if limit:
		return {"page": page, "limit": limit}
	return {"page": page}


@app03.get("/query/bool/conversion")
def type_conversion(param: bool = False):
	return param


# 字符串验证
@app03.get("/query/validations")
def query_params_validate(value: str = Query(..., min_length=8, max_length=16, regex="^a"),
						  values: List[str] = Query(default=["v1", "v2"], alias="alias_name")
						  ):
	# 多个查询参数列表参数别名
	return value, values


"""  请求体和字段 """


class CityInfo(BaseModel):
	name: str = Field(..., example="Beijing")  # example是注解作用 不会验证
	country: str
	country_code: str = None  # 给默认值
	country_population: int = Field(default=800, title="人口数量", description="国家人口数量", ge=800)

	class Config:
		schema_extra = {
			"example": {
				"name": "Shanghai",
				"country": "China",
				"country_code": "CN",
				"country_population": 140000000,

			}
		}


@app03.post("/request_body/city")
def city_info(city: CityInfo):
	print(city.name, city.country)
	return city.dict()


""" 多参数混合"""


@app03.put("/request_body/city/{name}")
def mix_city_info(
		name: str,
		city01: CityInfo,
		city02: CityInfo,  # body可以定义多个
		confirmed: int = Query(ge=0, description="确诊数", default=0),
		death: int = Query(ge=0, description="死亡数", default=0)

):
	if name == "Shanghai":
		return {"Shanghai": {"confirmed": confirmed, "death": death}}
	return city01.dict(), city02.dict()


"""  数据格式嵌套的请求体 """


class Data(BaseModel):
	city: List[CityInfo] = None  # 定义数据格式嵌套的请求体
	date: date
	confirmed: int = Field(ge=0, description="确诊数", default=0)
	death: int = Field(ge=0, description="死亡数", default=0)
	recovered: int = Field(ge=0, description="痊愈数", default=0)


@app03.put("request_body/nested")
def nested_models(data: Data):
	return data


""" cookie 和Header 参数 """


@app03.get("/cookie")  # 效果只能通过postman测试
def cookie(cookie_id: Optional[str] = Cookie(None)):  # 定义Cookie参数需要使用Cookie类
	return {"cookie_id": cookie_id}


@app03.get("header")
def header(user_agent: Optional[str] = Header(None, convert_underscores=True),
		   x_token: List[str] = Header(None)
		   ):
	"""

	:param user_agent:  convert_underscores 转换参数  user_agent -> user-agent
	:param x_token:  x_token包含多个值的列表
	:return:
	"""

	return {"User-Agent": user_agent, "x_token": x_token}
