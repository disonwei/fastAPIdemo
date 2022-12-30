# -*- coding: utf-8 -*-
# @Time : 2022/12/29
# @Author : Dison
from typing import Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel

from passlib.context import CryptContext
from jose import JWTError, jwt

app06 = APIRouter()

"""密码模式和 OAuth2PasswordBearer """

# 请求token的url地址 http://127.0.0.1:8000/chapter06/token
# OAuth2PasswordBearer 是接受url作为参数的一个类 客户端向该url发送username与password
# fastAPI回检测请求的Authorization头信息，如果没有找到Authorization头信息或者头信息不是Bearer token 会返回401状态码
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/chapter06/token")


@app06.get("oauth2_password_bearer")
async def oauth2_password_bearer(token: str = Depends(oauth2_schema)):
	return {"token": token}


"""基于password 和Bearer token的Oauth2认证"""

fake_users_db = {
	"john snow": {
		"username": "john show",
		"full_name": "john show",
		"email": "jogn@example.com",
		"hashed_password": "fakehashed11",
		"disabled": False
	},
	"alice": {
		"username": "alice",
		"full_name": "alice",
		"email": "alice@example.com",
		"hashed_password": "fakehashed22",
		"disabled": True
	}
}


def fake_hash_password(password: str):
	return "fakehashed" + password


class User(BaseModel):
	username: str
	email: Optional[str] = None
	full_name: Optional[str] = None
	disabled: Optional[bool] = None


class UserInDB(User):
	hashed_password: str


@app06.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
	user_dict = fake_users_db.get(form_data.username)
	if not user_dict:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect user"
		)
	user = UserInDB(**user_dict)
	hashed_password = fake_hash_password(form_data.password)
	if not hashed_password == user.hashed_password:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
		)
	return {"access_token": user.username, "token_type": "bearer"}


def get_user(db, username: str):
	if username in db:
		user_dict = db[username]
		return UserInDB(**user_dict)


def fake_decode_token(token: str):
	user = get_user(fake_users_db, token)
	return user


async def get_current_user(token: str = Depends(oauth2_schema)):
	user = fake_decode_token(token)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid authentication credentials",
			headers={"WWW-Authenticate": "Bearer"}
		)
	return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
	if current_user.disabled:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
	return current_user


@app06.get("/user/me")
async def read_users_me(curent_user: User = Depends(get_current_active_user)):
	return curent_user


"""基于json web tokens 的认证  jwt """

fake_users_db = {
	"john snow": {
		"username": "john show",
		"full_name": "john show",
		"email": "jogn@example.com",
		"hashed_password": "fakehashed11",
		"disabled": False
	},
	"alice": {
		"username": "alice",
		"full_name": "alice",
		"email": "alice@example.com",
		"hashed_password": "3ea5fae550e237a2d2b4c2e38def6aac",
		"disabled": False
	}
}

# 生成秘钥 openssl rand -hex 32
SECRET_KEY = "68a3dd7054eaa0349d0c64f75d8977dbef2b94da497d1e5ae9e65100e99fa650"
ALGORITHM = "HS256"  # 算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 访问令牌过期时间


class Token(BaseModel):
	"""返回给用户的token"""
	access_token: str
	token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/chapter06/jwt/token")


def verity_password(plain_password: str, hash_password: str):
	"""对密码进行校验"""
	return pwd_context.verify(plain_password, hash_password)


def jwt_get_user(db, username: str):
	if username in db:
		user_dict = db[username]
		return UserInDB(**user_dict)


def jwt_authenticate_user(db, username: str, password: str):
	user = jwt_get_user(db=db, username=username)
	if not user:
		return False
	if not verity_password(plain_password=password, hash_password=user.hashed_password):
		return False
	return user


def created_access_token(data: dict, expires_delta: Optional[timedelta] = None):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=15)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt


@app06.post("/jwt/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
	user = jwt_authenticate_user(db=fake_users_db, username=form_data.username, password=form_data.password)
	if not user:
		raise HTTPException(
			status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"
					 }
		)
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = created_access_token(
		data={"sub": user.username}, expires_delta=access_token_expires
	)
	return {"access_token": access_token, "token_type": "bearer"}


async def jwt_get_current_user(token: str = Depends(oauth2_schema)):
	credentials_exception = HTTPException(
		status.HTTP_401_UNAUTHORIZED,
		detail="校验失败",
		headers={"WWW-Authenticate": "Bearer"}
	)
	try:
		payload = jwt.decode(
			token=token, key=SECRET_KEY, algorithms=[ALGORITHM]
		)
		username = payload.get("sub")
		if username is None:
			raise credentials_exception
	except JWTError:
		raise credentials_exception

	user = jwt_get_user(db=fake_users_db, username=username)

	if user is None:
		raise credentials_exception
	return user


async def jwt_get_current_active_user(current_user: User = Depends(jwt_get_current_user)):
	if current_user.disabled:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="没有激活的用户"
		)
	return current_user



@app06.get("/jwt/user/me")
async def jwt_read_users_me(curent_user: User = Depends(jwt_get_current_active_user)):
	return curent_user
