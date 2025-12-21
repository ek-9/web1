from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from week9.config.database import Base
import datetime

class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, index=True)
    # 1. DB 컬럼 명시 (SQL 스키마)
    author_id = Column(Integer, ForeignKey("users.id"))

    title = Column(String(26), nullable=False)
    content = Column(Text, nullable=False)

    liked = Column(Integer, default=0)
    view = Column(Integer, default=0)

    created = Column(
        DateTime,
        default=datetime.datetime.now,
        nullable=False,
    )

    content_image = Column(String(255))
    # 2. 파이썬 객체 관계 명시 (ORM)
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    likes = relationship("PostLike", back_populates="post")

