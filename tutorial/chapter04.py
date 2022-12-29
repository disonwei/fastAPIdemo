# -*- coding: utf-8 -*-
# @Time : 2022/12/29
# @Author : Dison

from typing import Optional, List, Union
from fastapi import APIRouter, status, Form, File, UploadFile
from pydantic import BaseModel, EmailStr

app04 = APIRouter()

""" 响应模型 """


class UserIn(BaseModel):
	username: str
	password: str
	email: EmailStr
	mobile: str = "10086"
	address: str = None
	full_name: Optional[str] = None


class UserOut(BaseModel):
	username: str
	email: EmailStr
	mobile: str = "10086"
	address: str = None
	full_name: Optional[str] = None


users = {
	"user01": {"username": "user01", "password": "123123", "email": "user01@example.com"},
	"user02": {"username": "user02", "password": "123123", "email": "user02@example.com", "address": "beijing",
			   "full_name": "zhang san"}
}


# path operation 路径操作
@app04.post("/response_model", response_model=UserOut, response_model_exclude_unset=True)
async def response_model(user: UserIn):
	"""
	response_model_exclude_unset=True 表示默认值不包含在响应中，仅包含实际给的值，
	:param user:
	:return:
	"""
	print(user.password)  # password不会被返回
	return users["user01"]


@app04.post(
	"/response_model/attributes",
	response_model=UserOut,
	# response_model=Union[UserIn, UserOut]  # Union 取并集
	# response_model=List[UserOut]  # 返回一个列表
	response_model_include=["username", "email"],  # 返回包含的字段
	response_model_exclude=["mobile"]  # 排除字段返回
)
async def response_model_attributes(user: UserIn):
	# del user.password
	return user


# return [user,user]


""" 响应状态码 """


@app04.post("/status_code", status_code=200)
async def status_code():
	return {"status_code": 200}


@app04.post("/status_attribute", status_code=status.HTTP_200_OK)
async def status_attribute():
	print(type(status.HTTP_200_OK))
	return {"status_code": status.HTTP_200_OK}


"""  表单数据处理 """


@app04.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):  # 定义表单参数
	"""用 Form类需要 python-multipart"""
	return {"username": username}


""" 单文件 多文件上传以及参数详解"""


@app04.post("/file")
async def file_1(file: bytes = File(...)):
	"""使用File类 文件内容已bytes形式读入内存 适合上传小文件"""
	return {"file_size": len(file)}


@app04.post("/upload_files")
async def upload_files(files: List[UploadFile] = File(...)):
	"""
	使用UploadFile的优势
	1. 文件存储在内存中，使用内存达到阈值后，被保存在磁盘中
	2. 适合图片、视频大文件
	3. 可以获取上传的文件元数据，如文件名、创建时间等
	4. 有文件对象的异步接口
	5. 上传的文件是python文件对象，可以使用write() read() seek() close()
	:param files:
	:return:
	"""

	for file in files:
		contents = await file.read()
		print(contents)
	return {"filename": files[0].filename, "content_type": files[0].content_type}
