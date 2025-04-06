# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: posts_service.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'posts_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13posts_service.proto\x12\x05posts\"\x91\x01\n\x04Post\x12\n\n\x02id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x12\n\ncreator_id\x18\x04 \x01(\x05\x12\x12\n\ncreated_at\x18\x05 \x01(\t\x12\x12\n\nupdated_at\x18\x06 \x01(\t\x12\x0f\n\x07private\x18\x07 \x01(\x08\x12\x0c\n\x04tags\x18\x08 \x03(\t\"j\n\x11\x43reatePostRequest\x12\r\n\x05title\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x12\n\ncreator_id\x18\x03 \x01(\x05\x12\x0f\n\x07private\x18\x04 \x01(\x08\x12\x0c\n\x04tags\x18\x05 \x03(\t\"/\n\x12\x43reatePostResponse\x12\x19\n\x04post\x18\x01 \x01(\x0b\x32\x0b.posts.Post\"{\n\x11UpdatePostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x0f\n\x07private\x18\x04 \x01(\x08\x12\x0c\n\x04tags\x18\x05 \x03(\t\x12\x12\n\ncreator_id\x18\x06 \x01(\x05\"/\n\x12UpdatePostResponse\x12\x19\n\x04post\x18\x01 \x01(\x0b\x32\x0b.posts.Post\"8\n\x11\x44\x65letePostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x12\n\ncreator_id\x18\x02 \x01(\x05\"%\n\x12\x44\x65letePostResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"5\n\x0eGetPostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x12\n\ncreator_id\x18\x02 \x01(\x05\",\n\x0fGetPostResponse\x12\x19\n\x04post\x18\x01 \x01(\x0b\x32\x0b.posts.Post\"C\n\x10ListPostsRequest\x12\x0c\n\x04page\x18\x01 \x01(\x05\x12\r\n\x05\x63ount\x18\x02 \x01(\x05\x12\x12\n\ncreator_id\x18\x03 \x01(\x05\"/\n\x11ListPostsResponse\x12\x1a\n\x05posts\x18\x01 \x03(\x0b\x32\x0b.posts.Post2\xd0\x02\n\x0bPostService\x12\x41\n\nCreatePost\x12\x18.posts.CreatePostRequest\x1a\x19.posts.CreatePostResponse\x12\x41\n\nUpdatePost\x12\x18.posts.UpdatePostRequest\x1a\x19.posts.UpdatePostResponse\x12\x41\n\nDeletePost\x12\x18.posts.DeletePostRequest\x1a\x19.posts.DeletePostResponse\x12\x38\n\x07GetPost\x12\x15.posts.GetPostRequest\x1a\x16.posts.GetPostResponse\x12>\n\tListPosts\x12\x17.posts.ListPostsRequest\x1a\x18.posts.ListPostsResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'posts_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_POST']._serialized_start=31
  _globals['_POST']._serialized_end=176
  _globals['_CREATEPOSTREQUEST']._serialized_start=178
  _globals['_CREATEPOSTREQUEST']._serialized_end=284
  _globals['_CREATEPOSTRESPONSE']._serialized_start=286
  _globals['_CREATEPOSTRESPONSE']._serialized_end=333
  _globals['_UPDATEPOSTREQUEST']._serialized_start=335
  _globals['_UPDATEPOSTREQUEST']._serialized_end=458
  _globals['_UPDATEPOSTRESPONSE']._serialized_start=460
  _globals['_UPDATEPOSTRESPONSE']._serialized_end=507
  _globals['_DELETEPOSTREQUEST']._serialized_start=509
  _globals['_DELETEPOSTREQUEST']._serialized_end=565
  _globals['_DELETEPOSTRESPONSE']._serialized_start=567
  _globals['_DELETEPOSTRESPONSE']._serialized_end=604
  _globals['_GETPOSTREQUEST']._serialized_start=606
  _globals['_GETPOSTREQUEST']._serialized_end=659
  _globals['_GETPOSTRESPONSE']._serialized_start=661
  _globals['_GETPOSTRESPONSE']._serialized_end=705
  _globals['_LISTPOSTSREQUEST']._serialized_start=707
  _globals['_LISTPOSTSREQUEST']._serialized_end=774
  _globals['_LISTPOSTSRESPONSE']._serialized_start=776
  _globals['_LISTPOSTSRESPONSE']._serialized_end=823
  _globals['_POSTSERVICE']._serialized_start=826
  _globals['_POSTSERVICE']._serialized_end=1162
# @@protoc_insertion_point(module_scope)
