# -*- coding: utf-8 -*-
# @Time : 2022/12/30
# @Author : Dison

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./coronavirus.sqlite3"

engine = create_engine(
	#  echo=True 表示引擎将用repr()函数记录所有语句以及参数到日志
	# "check_same_thread": False 让建立的对象任意线程都使用，只有sqlite使用
	SQLALCHEMY_DATABASE_URL, encoding="utf-8", echo=True,
	connect_args={"check_same_thread": False}
)

# crud 是用会话 session进行的，所以必须先创建会话，每一个SessionLocal实例是一个数据库session
# flush()是指发送数据库语句到数据库，但数据库不一定执行写入磁盘
# commit()指提交事务，将变更保存到数据库文件
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)

# 创建基本的映射类
Base = declarative_base(bind=engine, name="Base")
