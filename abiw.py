from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

news = []

class NewsSchema(BaseModel):
	about: str
	text: str


@app.get("/api/news")
async def get_news():
	return news


@app.post("/api/news")
async def create_news(data: NewsSchema):
	if not data.about or not data.text:
		return HTTPException(status_code=400, detail="about penen text qayqta, qayaqqa qarap otirsan sawatsiz")
	
	data = {"about": data.about, "text": data.text}
	news.append(data)
	return {"success": True, "msg": "Mnawin bolaadi", "data": data}

  


