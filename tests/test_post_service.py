import pytest
from unittest.mock import AsyncMock, MagicMock
from grpc import StatusCode
from grpc_service.src.service.posts_service import PostService
from grpc_service.src import posts_service_pb2 as pb2


@pytest.fixture
def service():
    return PostService(repository=MagicMock())


def test_create_post(service):
    request = pb2.CreatePostRequest(
        title="Test Post",
        description="This is a test",
        creator_id=1,
        private=False,
        tags=["test", "grpc"]
    )
    context = MagicMock()

    response = service.CreatePost(request, context)

    assert isinstance(response, pb2.CreatePostResponse)
    assert response.post.title == "Test Post"
    assert response.post.creator_id == 1
    assert response.post.tags == ["test", "grpc"]


def test_get_post_found(service):
    post = MagicMock()
    post.to_proto.return_value = pb2.Post(id=1, title="Hello", creator_id=1)

    service.repository.get.return_value = post

    request = pb2.GetPostRequest(post_id=1)
    context = MagicMock()

    response = service.GetPost(request, context)

    assert isinstance(response, pb2.GetPostResponse)
    assert response.post.title == "Hello"


def test_get_post_not_found(service):
    service.repository.get.return_value = None

    request = pb2.GetPostRequest(post_id=1)
    context = MagicMock()

    response = service.GetPost(request, context)

    context.set_code.assert_called_with(StatusCode.NOT_FOUND)
    context.set_details.assert_called_once()
    assert response == pb2.GetPostResponse()


def test_update_post_unauthorized(service):
    post = MagicMock()
    post.creator_id = 2  # not the same as request.creator_id

    service.repository.get.return_value = post

    request = pb2.UpdatePostRequest(
        post_id=1,
        creator_id=1,
        title="Updated",
        description="Updated desc",
        private=False,
        tags=[]
    )
    context = MagicMock()

    response = service.UpdatePost(request, context)

    context.set_code.assert_called_with(StatusCode.PERMISSION_DENIED)
    assert response == pb2.UpdatePostResponse()


def test_delete_post_success(service):
    post = MagicMock()
    post.creator_id = 1
    service.repository.get.return_value = post

    request = pb2.DeletePostRequest(post_id=1, creator_id=1)
    context = MagicMock()

    response = service.DeletePost(request, context)

    assert response.success is True


def test_list_posts(service):
    mock_post = MagicMock()
    mock_post.to_proto.return_value = pb2.Post(id=1, title="Test", creator_id=1)

    service.repository.list_paginated.return_value = [mock_post]

    request = pb2.ListPostsRequest(page=1, count=10)
    context = MagicMock()

    response = service.ListPosts(request, context)

    assert len(response.posts) == 1
    assert response.posts[0].title == "Test"
