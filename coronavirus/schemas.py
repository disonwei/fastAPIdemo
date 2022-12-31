# -*- coding: utf-8 -*-
# @Time : 2022/12/30
# @Author : Dison

from datetime import datetime
from datetime import date as date_
from pydantic import BaseModel


class CreateData(BaseModel):
	date: date_
	confiremd: int = 0
	deaths: int = 0
	recovered: int = 0


class ReadData(CreateData):
	id: int
	city_id: int
	updated_at: datetime
	created_at: datetime

	class Config:
		orm_mode = True


class CreateCity(BaseModel):
	province: str
	country: str
	country_code: str
	country_population: int


class ReadCity(CreateCity):
	id: int
	updated_at: datetime
	create_At: datetime

	class Config:
		orm_mode = True
