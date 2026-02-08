from pydantic import BaseModel, Field


class UserLoginSchema(BaseModel):
	username: str = Field(max_length=32, min_length=3)
	password: str = Field(min_length=3)


class UserSchema(UserLoginSchema):
	id: int = Field(ge=0)
	is_actibe: bool

