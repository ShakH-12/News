from fastapi import APIRouter, Request, HTTPException, UploadFile, Form
from fastapi.responses import FileResponse
from datetime import datetime, timedelta

from src.database import select, update, delete
from src.dependencies import SessionDep, PaginationDep

from src.models.news import (
    NewsModel,
    NewsCommentModel,
    NewsLikesModel,
    NewsCategoryModel
)
from src.schemas.news import (
    CreateNewsSchema,
    NewsSchema,
    CreateNewsCommentSchema,
    DeleteNewsSchema,
    NewsCommentSchema,
    CreateNewsCategorySchema
)
import secrets

router = APIRouter()


@router.get("/news")
async def get_news(session: SessionDep, pagination: PaginationDep, category_id: int = None, news_id: int = None):
	if news_id:
		query = select(NewsModel).filter_by(id=news_id)
		news = await session.execute(query)
		news = news.scalars().first()
		if not news:
			return HTTPException(status_code=404, detail="news not found")
		return news

	query = select(NewsModel).limit(pagination.limit).offset(pagination.offset)
	news = await session.execute(query)
	return news.scalars().all()


@router.post("/news")
async def post_news(
       request: Request,
       session: SessionDep,
       image: UploadFile,
       category_id: int = Form(),
       title: str = Form(),
       about: str = Form(),
       text: str = Form()
   ):
   	
	user_id = request.state.user
	if not user_id:
		return HTTPException(status_code=429, detail="permission denied")
	
	query = select(NewsCategoryModel).filter_by(id=category_id)
	category = await session.execute(query)
	category = category.scalars().first()
	
	if not category:
		return HTTPException(status_code=404, detail="category not found")
	
	key = secrets.token_urlsafe(5)
	path = f"media/images/{key}_{image.filename}"
	with open(path, "wb") as file:
		file.write(image.file.read())
	
	news = NewsModel(
	    author=user_id,
	    category=category.id,
	    image=path,
	    title=title,
	    about=about,
	    text=text,
	    created_at=datetime.now()
	)
	session.add(news)
	await session.commit()
	return news


@router.delete("/news")
async def delete_news(data: DeleteNewsSchema, session: SessionDep):
	query = select(NewsModel).filter_by(id=data.id)
	news = await session.execute(query)
	if not news.scalars().first():
		return HTTPException(status_code=404, detail="news not found")
		
	query = delete(NewsModel).where(NewsModel.id==data.id)
	await session.execute(query)
	await session.commit()
	return {"ok": True}


@router.get("/news/comments")
async def get_news_comments(session: SessionDep, pagination: PaginationDep):
	query = select(NewsCommentModel).limit(pagination.limit).offset(pagination.offset)
	comments = await session.execute(query)
	return comments.scalars().all()


@router.post("/news/comments")
async def create_news_comment(request: Request, data: CreateNewsCommentSchema, session: SessionDep):
	user_id = request.state.user
	if not user_id:
		return HTTPException(status_code=429, detail="permission denied")
	
	comment = NewsCommentModel(
	    news=data.news,
	    sender=user_id,
	    text=data.text,
	    created_at=datetime.now()
	)
	session.add(comment)
	await session.commit()
	return comment


@router.get("/news/categories")
async def get_categories(session: SessionDep, pagination: PaginationDep):
	query = select(NewsCategoryModel).limit(pagination.limit).offset(pagination.offset)
	categories = await session.execute(query)
	return categories.scalars().all()


@router.post("/news/categories")
async def create_category(data: CreateNewsCategorySchema, session: SessionDep):
	category = NewsCategoryModel(name=data.name)
	session.add(category)
	await session.commit()
	return category


@router.get("/media/images/{filename}")
async def get_image(filename: str):
	return FileResponse(f"media/images/{filename}")
