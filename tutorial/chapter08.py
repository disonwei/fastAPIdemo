# -*- coding: utf-8 -*-
# @Time : 2022/12/29
# @Author : Dison
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends

app08 = APIRouter()

"""middleware 中间件  run.py"""

# 带yield的依赖的退出部分的代码和后台任务再中间件之后运行


"""后台任务"""


def bg_task(framework: str):
	with open("README.md", mode="a") as f:
		f.write(f"## {framework} 框架精讲")


@app08.post("/background_tasks")
async def run_bg_task(framework: str, background_task: BackgroundTasks):
	"""

	:param framework: 被调用的后台任务函数的参数
	:param background_task: FastAPI.BackgroundTasks
	:return: 
	"""
	background_task.add_task(bg_task, framework)
	return {"message": "任务已经在运行"}


def continue_write_readme(background_tasks: BackgroundTasks, q: Optional[str] = None):
	if q:
		background_tasks.add_task(bg_task, "使用依赖注入方式 后台任务")
	return q


@app08.post("/dependency/background_tasks")
async def dependency_run_bg_task(q: str = Depends(continue_write_readme)):
	if q:
		return {"message": "任务已经在后台运行"}
