from src.database import Base, Mapped, mapped_column


class NewsModel(Base):
	__tablename__ = "news"
	
	id: Mapped[int] = mapped_column(primary_key=True)
	author: Mapped[int]
	category: Mapped[int]
	image: Mapped[str]
	title: Mapped[str]
	about: Mapped[str]
	text: Mapped[str]
	created_at: Mapped[str]


class NewsCommentModel(Base):
	__tablename__ = "news comments"
	
	id: Mapped[int] = mapped_column(primary_key=True)
	news: Mapped[int]
	sender: Mapped[int]
	text: Mapped[str]
	created_at: Mapped[str]


class NewsLikesModel(Base):
	__tablename__ = "news likes"
	
	id: Mapped[int] = mapped_column(primary_key=True)
	news: Mapped[int]
	user: Mapped[int]
	created_at: Mapped[str]


class NewsCategoryModel(Base):
	__tablename__ = "news category"
	
	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str]


