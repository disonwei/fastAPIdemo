# -*- coding: utf-8 -*-
# @Time : 2022/12/30
# @Author : Dison

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, BigInteger, Date, DateTime, ForeignKey, func

from coronavirus.database import Base


class City(Base):
	__tablename__ = "city"
	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	province = Column(String(100), unique=True, nullable=False, comment="省\直辖市")
	country = Column(String(100), nullable=False, comment="国家")
	country_code = Column(String(100), nullable=False, comment="国家代码")
	country_population = Column(BigInteger, nullable=False, comment="人口")
	# Data 是关联的类名    back_populates 反向查询的字段
	data = relationship("Data", back_populates="city")

	created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
	updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

	# __mapper_args__ = {
	# 	# 默认正序，倒序加上.desc()方法
	# 	"order_by": country_code
	# }

	def __repr__(self):
		return f"{self.country}_{self.province}"


class Data(Base):
	__tablename__ = "data"
	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	# ForeignKey里的 字符串格式不是类名.属性名 是表名.属性名
	city_id = Column(Integer, ForeignKey("city.id"), comment="省\直辖市")
	date = Column(Date, nullable=False, comment="数据日期")
	confirmed = Column(BigInteger, default=0, nullable=False, comment="确诊数量")
	deaths = Column(BigInteger, default=0, nullable=False, comment="死亡数量")
	recovered = Column(BigInteger, default=0, nullable=False, comment="痊愈数量")
	# City 是关联类名
	city = relationship("City", back_populates="data")

	# __mapper_args__ = {
	# 	# 默认正序，倒序加上.desc()方法
	# 	"order_by": date.desc()
	# }

	def __repr__(self):
		return f"{repr(self.country)}_确诊{self.confirmed}"
