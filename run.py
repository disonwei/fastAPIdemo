# -*- coding: utf-8 -*-
# @Time : 2022/12/29
# @Author : Dison

import uvicorn
from fastapi import FastAPI

from tutorial import app03, app04, app05, app06, app07, app08

app = FastAPI()

app.include_router(app03, prefix="/chapter03", tags=["第三章 请求参数和验证"])
app.include_router(app04, prefix="/chapter04", tags=["第四章 响应处理和fastapi配置"])
app.include_router(app05, prefix="/chapter05", tags=["第五章 fastapi依赖注入系统"])

if __name__ == '__main__':
	uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True, workers=1)

# /
# /coronavirus
# /tutorial
