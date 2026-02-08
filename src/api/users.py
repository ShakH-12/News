from fastapi import APIRouter, Request, HTTPException
from src.database import select
from src.dependencies import SessionDep
from src.models.users import UserModel
from src.schemas.users import UserLoginSchema, UserSchema
from src.auth.security import make_password, check_password, security

router = APIRouter()


@router.get("/users")
async def get_users(session: SessionDep):
	query = select(UserModel)
	users = await session.execute(query)
	return users.scalars().all()


@router.post("/register")
async def register(data: UserLoginSchema, session: SessionDep):
	query = select(UserModel).filter_by(username=data.username)
	user = await session.execute(query)
	user = user.scalars().first()
	if user:
		return HTTPException(status_code=400, detail="username already taked")
	
	user = UserModel(username=data.username, password=make_password(data.password), is_active=True)
	session.add(user)
	await session.commit()
	return user


@router.post("/login")
async def login(data: UserLoginSchema, session: SessionDep):
	query = select(UserModel).filter_by(username=data.username)
	user = await session.execute(query)
	user = user.scalars().first()
	if not user:
		return HTTPException(status_code=404, detail="user not found")
	
	if check_password(data.password, user.password):
		token = security.create_access_token(uid=str(user.id))
		return {"access_token": token}
	return HTTPException(status_code=400, detail="password didn't match")


@router.get("/profile")
async def profile(request: Request, session: SessionDep):
	query = select(UserModel).filter_by(id=request.state.user)
	user = await session.execute(query)
	return user.scalars().first()



