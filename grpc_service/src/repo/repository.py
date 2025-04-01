from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from grpc_service.src.models.post import PostDB

class PostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, post: PostDB):
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def get(self, post_id: int):
        result = await self.session.execute(select(PostDB).where(PostDB.id == post_id))
        return result.scalar_one_or_none()

    async def update(self, post_id: int, **kwargs):
        stmt = update(PostDB).where(PostDB.id == post_id).values(**kwargs).returning(PostDB)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete(self, post_id: int):
        stmt = delete(PostDB).where(PostDB.id == post_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return True

    async def list_paginated(self, page: int, count: int):
        result = await self.session.execute(
            select(PostDB).offset((page - 1) * count).limit(count)
        )
        return result.scalars().all()
