from src.database import Base, Mapped, mapped_column


class UserModel(Base):
	__tablename__ = "users"
	
	id: Mapped[int] = mapped_column(primary_key=True)
	username: Mapped[str]
	password: Mapped[str]
	is_active: Mapped[bool]

