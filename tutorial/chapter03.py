# -*- coding: utf-8 -*-
# @Time : 2022/12/29
# @Author : Dison
from enum import Enum
from typing import Optional, List

from fastapi import APIRouter, Path, Query

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
