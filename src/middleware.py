from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import AuthenticationBackend, AuthCredentials, SimpleUser
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from src.auth.security import config
from typing import Callable
import time

from jose import jwt, JWTError
from src.database import select
from src.models.users import UserModel
from src.dependencies import SessionDep

SECRET_KEY = config.JWT_SECRET_KEY
ALGORITHM = "HS256"


class CheckRequestsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        start = time.perf_counter()
        '''
        print(f"🛡️ [MIDDLEWARE:{request.url}] Start request for {request.client.host}")

        print("--"*20, "\n\n")
        '''
        response = await call_next(request)
        '''
        print("\n\n", "--"*20)

        end = time.perf_counter() - start
        print(f"🛡️ [MIDDLEWARE:{request.url}] End request for {request.client.host}")
        print(f"🛡️ [MIDDLEWARE:{request.url}] Request time {end:.2f}")
        '''
        return response


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        return AuthCredentials(["authenticated"]), SimpleUser("guest")


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next, session=SessionDep):
        request.state.user = None  # по дефолту

        auth = request.headers.get("Authorization")
        if auth and auth.startswith("Bearer "):
            token = auth.split(" ")[1]
            
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_id = payload.get("sub")
                
                # query = select(UserModel).filter_by(id=user_id)
                # user = await session.execute(query)
                
                request.state.user = user_id # user.scalars().all()
                
            except JWTError:
                pass

        response = await call_next(request)
        return response


class GetMeMiddleware(BaseHTTPMiddleware):
	async def dispatch(self, request: Request, call_next: Callable, session=SessionDep):
		response = await call_next(request)
		'''
		# TEST MIDDLEWARE
		query = select(UserModel).filter_by(id=request.state.user)
		user = await session.execute(query)
		user = user.scalars().first()
		'''
		
		return response


