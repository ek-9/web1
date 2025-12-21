from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from week9.config.database import Base
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    nickname = Column(String(20), unique=True, nullable=False)
    profile_image = Column(String(255))

    posts = relationship("Post", back_populates="author")

    # 작성한 댓글
    comments = relationship("Comment", back_populates="user")

    # 좋아하는 게시글 -> N : N 구조 별도, 테이블 생성
    likes = relationship("PostLike", back_populates="user")
