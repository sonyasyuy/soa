from datetime import datetime
import posts_service_pb2 as pb2
from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP, ARRAY
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class PostDB(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    creator_id = Column(Integer, nullable=False)
    private = Column(Boolean, default=False)
    tags = Column(ARRAY(String))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_proto(self):
        from posts_service_pb2 import Post  # импорт внутри функции, чтобы избежать циклов
        return Post(
            id=self.id,
            title=self.title,
            description=self.description,
            creator_id=self.creator_id,
            private=self.private,
            tags=self.tags,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat()
        )


class PostModel:
    _id_counter = 1

    def __init__(self, title, description, creator_id, private, tags):
        self.id = PostModel._id_counter
        PostModel._id_counter += 1
        self.title = title
        self.description = description
        self.creator_id = creator_id
        self.private = private
        self.tags = tags
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def to_proto(self):
        return pb2.Post(
            id=self.id,
            title=self.title,
            description=self.description,
            creator_id=self.creator_id,
            private=self.private,
            tags=self.tags or [],
            created_at=self.created_at.isoformat() if self.created_at else "",
            updated_at=self.updated_at.isoformat() if self.updated_at else "",
        )

