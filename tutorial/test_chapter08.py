# -*- coding: utf-8 -*-
# @Time : 2022/12/31
# @Author : Dison

from fastapi.testclient import TestClient

from run import app

"""测试用例 """

client = TestClient(app)


# test 开头 pytest 规范
def test_run_bg_task():
	response = client.post(url="chapter08/background_tasks?framework=FastAPI")
	assert response.status_code == 200
	assert response.json() == {"message": "任务已经在后台运行"}


def test_dependency_run_bg_task():
	response = client.post(url="chapter08/dependency/background_tasks")
	assert response.status_code == 200
	assert response.json() is None
