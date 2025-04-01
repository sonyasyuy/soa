import grpc
from datetime import datetime

from posts_service_pb2 import (
    CreatePostResponse, GetPostResponse, UpdatePostResponse,
    DeletePostResponse, ListPostsResponse
)
import posts_service_pb2 as pb2
import posts_service_pb2_grpc as pb2_grpc

from models.post import PostDB
from repo.init_db import async_session

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

class PostService(pb2_grpc.PostServiceServicer):

    async def CreatePost(self, request, context):
        async with async_session() as session:
            post = PostDB(
                title=request.title,
                description=request.description,
                creator_id=request.creator_id,
                private=request.private,
                tags=list(request.tags),
            )
            session.add(post)
            await session.commit()
            await session.refresh(post)

            return pb2.CreatePostResponse(post=post.to_proto())

    async def GetPost(self, request, context):
        async with async_session() as session:
            try:
                result = await session.execute(select(PostDB).where(PostDB.id == request.post_id))
                post = result.scalar_one()
                return pb2.GetPostResponse(post=post.to_proto())
            except NoResultFound:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Post not found")
                return pb2.GetPostResponse()

    async def UpdatePost(self, request, context):
        async with async_session() as session:
            result = await session.execute(select(PostDB).where(PostDB.id == request.post_id))
            post = result.scalar_one_or_none()

            if not post:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Post not found")
                return pb2.UpdatePostResponse()

            if post.creator_id != request.creator_id:
                context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                context.set_details("You are not the creator")
                return pb2.UpdatePostResponse()

            post.title = request.title
            post.description = request.description
            post.private = request.private
            post.tags = list(request.tags)
            post.updated_at = datetime.utcnow()

            await session.commit()
            await session.refresh(post)

            return pb2.UpdatePostResponse(post=post.to_proto())

    async def DeletePost(self, request, context):
        async with async_session() as session:
            result = await session.execute(select(PostDB).where(PostDB.id == request.post_id))
            post = result.scalar_one_or_none()

            if not post:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Post not found")
                return pb2.DeletePostResponse(success=False)

            if post.creator_id != request.creator_id:
                context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                context.set_details("You are not the creator")
                return pb2.DeletePostResponse(success=False)

            await session.delete(post)
            await session.commit()

            return pb2.DeletePostResponse(success=True)

    async def ListPosts(self, request, context):
        async with async_session() as session:
            offset = (request.page - 1) * request.count
            result = await session.execute(select(PostDB).offset(offset).limit(request.count))
            posts = result.scalars().all()

            return pb2.ListPostsResponse(
                posts=[post.to_proto() for post in posts]
            )
