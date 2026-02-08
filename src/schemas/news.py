from pydantic import BaseModel, Field
from fastapi import UploadFile


class CreateNewsSchema(BaseModel):
	# image: UploadFile
	title: str = Field(max_length=64)
	about: str = Field(max_length=124)
	text: str = Field(max_length=2000)
	category: int = Field(ge=0)


class NewsSchema(CreateNewsSchema):
	id: int = Field(ge=0)
	author: str
	created_at: str


class DeleteNewsSchema(BaseModel):
	id: int = Field(ge=0)



class CreateNewsCommentSchema(BaseModel):
	news: int = Field(ge=0)
	text: str = Field(max_length=1000, min_length=3)


class NewsCommentSchema(CreateNewsCommentSchema):
	id: int = Field(ge=0)
	sender: int = Field(ge=0)
	created_at: str


class CreateNewsCategorySchema(BaseModel):
	name: str = Field(max_length=24)


class NewsCategorySchema(CreateNewsCategorySchema):
	id: int = Field(ge=0)
