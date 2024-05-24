from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

db = SQLAlchemy()

class User(db.Model):
    userid: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100))