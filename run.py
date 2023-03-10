# -*- coding: utf-8 -*-
# @Time : 2022/12/29
# @Author : Dison
import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from coronavirus import application
from tutorial import app03, app04, app05, app06, app07, app08

from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException

# 文档配置
app = FastAPI(
	title="FastApi tutorial and coronavirus Tracker Api Docs",
	description="FastApi 测试文档",
	version="1.0.0",
	docs_url="/docs",
	redoc_url="/redocs",
	# dependencies=[Depends(verify_token), Depends(verify_key)  全局依赖
)

# mount 表示将某个目录下一个完全独立的应用挂载过来，api不会显示在文档中
app.mount(path="/static", app=StaticFiles(directory="./coronavirus/static"), name="static")


# # 重写HTTPException异常处理
# @app.exception_handlers(StarletteHTTPException)
# async def http_exception_handler(request, exc):
# 	"""
#
# 	:param request: 不能省
# 	:param exc:
# 	:return:
# 	"""
# 	return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
#
#
# # 重写请求验证异常处理
# @app.exception_handlers(RequestValidationError)
# async def validation_exception_handler(request, exc):
# 	"""
#
# 	:param request:不能省
# 	:param exc:
# 	:return:
# 	"""
# 	return PlainTextResponse(str(exc), status_code=400)
#

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
	start_time = time.time()
	response = await call_next(request)
	process_time = time.time() - start_time
	# 添加自定义以"X-"开头的请求头
	response.headers["X-Process-Time"] = str(process_time)
	return response


app.add_middleware(
	CORSMiddleware,
	allow_origins=[
		"http://127.0.0.1",
		"http://127.0.0.1:8080",
	],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

app.include_router(app03, prefix="/chapter03", tags=["第三章 请求参数和验证"])
app.include_router(app04, prefix="/chapter04", tags=["第四章 响应处理和fastapi配置"])
app.include_router(app05, prefix="/chapter05", tags=["第五章 fastapi依赖注入系统"])
app.include_router(app06, prefix="/chapter06", tags=["第六章 安全、认证授权"])
app.include_router(app07, prefix="/chapter07", tags=["第七章 数据库操作目录文件设计"])
app.include_router(application, prefix="/coronavirus", tags=["新冠病毒疫情根据API"])
app.include_router(app08, prefix="/chapter08", tags=["第八章 中间件 cors 后台任务"])

if __name__ == '__main__':
	uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True, workers=1)

# /
# /coronavirus
# /tutorial
