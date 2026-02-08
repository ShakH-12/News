from fastapi import Depends
from typing import Annotated
from pydantic import BaseModel, Field

from src.database import AsyncSession, get_session


class PaginationParams(BaseModel):
	limit: int = Field(50, ge=0, le=50)
	offset: int = Field(0, ge=0)

SessionDep = Annotated[AsyncSession, Depends(get_session)]
PaginationDep = Annotated[PaginationParams, Depends(PaginationParams)]