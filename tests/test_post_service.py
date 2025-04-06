import os
import sys
import pytest
from sqlalchemy.exc import NoResultFound

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../grpc_service/src')))


from unittest.mock import AsyncMock, MagicMock
from grpc import StatusCode
# import posts_service_pb2 as pb2
from grpc_service.src import posts_service_pb2 as pb2

from service.posts_service import PostService


from datetime import datetime




@pytest.mark.asyncio
async def test_create_post(mocker):
    session = AsyncMock()
    session.__aenter__.return_value = session
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()

    now = datetime.utcnow()

    # создаём мок post
    mock_post = MagicMock()
    mock_post.id = 1
    mock_post.title = "Test Post"
    mock_post.description = "This is a test"
    mock_post.creator_id = 1
    mock_post.private = False
    mock_post.tags = ["test", "grpc"]
    mock_post.created_at = now
    mock_post.updated_at = now
    mock_post.to_proto.return_value = pb2.Post(
        id=1,
        title="Test Post",
        description="This is a test",
        creator_id=1,
        private=False,
        tags=["test", "grpc"],
        created_at=now.isoformat(),
        updated_at=now.isoformat()
    )

    #Внутри refresh подставляем мокнутые поля
    session.refresh.side_effect = lambda post: post.__dict__.update(mock_post.__dict__)

    mocker.patch("service.posts_service.async_session", return_value=session)

    service = PostService()
    context = MagicMock()
    request = pb2.CreatePostRequest(
        title="Test Post",
        description="This is a test",
        creator_id=1,
        private=False,
        tags=["test", "grpc"]
    )

    response = await service.CreatePost(request, context)

    assert response.post.title == "Test Post"
    assert response.post.creator_id == 1
    assert response.post.tags == ["test", "grpc"]


@pytest.mark.asyncio
async def test_get_post_found(mocker):
    post_mock = MagicMock()
    post_mock.private = False
    post_mock.creator_id = 1
    post_mock.to_proto.return_value = pb2.Post(
        id=1,
        title="Test",
        description="Description",
        creator_id=1,
        private=False,
        tags=["tag1"],
        created_at="2025-04-06T00:00:00",
        updated_at="2025-04-06T00:00:00"
    )

    mock_result = MagicMock()
    mock_result.scalar_one = AsyncMock(return_value=post_mock)

    session = AsyncMock()
    session.__aenter__.return_value = session
    session.execute.return_value = mock_result

    mocker.patch("service.posts_service.async_session", return_value=session)

    service = PostService()
    context = MagicMock()
    request = pb2.GetPostRequest(post_id=1)

    response = await service.GetPost(request, context)

    assert response.post.title == "Test"
    assert response.post.creator_id == 1






@pytest.mark.asyncio
async def test_update_post_unauthorized(mocker):
    post_mock = MagicMock()
    post_mock.id = 1
    post_mock.creator_id = 2

    mock_result = MagicMock()
    mock_result.scalar_one_or_none = AsyncMock(return_value=post_mock)

    session = AsyncMock()
    session.__aenter__.return_value = session
    session.execute.return_value = mock_result

    mocker.patch("service.posts_service.async_session", return_value=session)

    service = PostService()
    context = MagicMock()

    request = pb2.UpdatePostRequest(
        post_id=1,
        creator_id=1,  # <- не совпадает
        title="Updated",
        description="Updated desc",
        private=False,
        tags=[]
    )

    response = await service.UpdatePost(request, context)

    print(f"response type: {type(response)}")
    print(f"response: {response}")

    context.set_code.assert_called_once_with(StatusCode.PERMISSION_DENIED)
    context.set_details.assert_called_once_with("You are not the creator")

    assert isinstance(response, pb2.UpdatePostResponse)
    assert response.post.id == 0  # если пустой Post


@pytest.mark.asyncio
async def test_delete_post_success(mocker):
    post = MagicMock()
    post.creator_id = 1

    # 💡 scalar_one_or_none должен быть именно async
    mock_result = MagicMock()
    mock_result.scalar_one_or_none = AsyncMock(return_value=post)

    session = AsyncMock()
    session.__aenter__.return_value = session
    session.execute.return_value = mock_result
    session.delete.return_value = None
    session.commit.return_value = None

    # 👇 Путь должен совпадать с импортом в сервисе
    mocker.patch("service.posts_service.async_session", return_value=session)

    service = PostService()
    context = MagicMock()

    request = pb2.DeletePostRequest(post_id=1, creator_id=1)

    response = await service.DeletePost(request, context)

    assert isinstance(response, pb2.DeletePostResponse)
    assert response.success is True



@pytest.mark.asyncio
async def test_list_posts(mocker):
    mock_post = MagicMock()
    mock_post.to_proto.return_value = pb2.Post(id=1, title="Test", creator_id=1)

    mock_scalars = MagicMock()
    mock_scalars.all.return_value = [mock_post]

    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars

    session = AsyncMock()
    session.__aenter__.return_value = session
    session.execute.return_value = mock_result

    mocker.patch("service.posts_service.async_session", return_value=session)

    service = PostService()
    context = MagicMock()
    request = pb2.ListPostsRequest(page=1, count=10)

    response = await service.ListPosts(request, context)

    assert isinstance(response, pb2.ListPostsResponse)
    assert len(response.posts) == 1
    assert response.posts[0].title == "Test"



