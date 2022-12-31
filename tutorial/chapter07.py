# -*- coding: utf-8 -*-
# @Time : 2022/12/29
# @Author : Dison

from fastapi import APIRouter, Depends, Request

"""多目录结构设计"""


async def get_user_agent(request: Request):
	print(request.headers["User-Agent"])


app07 = APIRouter(
	prefix="/bigger_applications",
	tags=["第7章"],
	dependencies=[Depends(get_user_agent)],
	responses={200: {"description": "good job!"}}
)


@app07.get("/bigger_applications")
async def bigger_applications():
	return {"message": "bIGGER"}
