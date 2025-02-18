# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: gfs.proto
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
    'gfs.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tgfs.proto\x12\x03gfs\"\x1e\n\rStringMessage\x12\r\n\x05value\x18\x01 \x01(\t\"\x1f\n\x0b\x46ileRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\"0\n\x0c\x46ileResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\" \n\x0c\x43hunkRequest\x12\x10\n\x08\x63hunk_id\x18\x01 \x01(\t\"J\n\rChunkResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x17\n\x0f\x61vailable_space\x18\x03 \x01(\x03\"?\n\x0bReadRequest\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0e\n\x06offset\x18\x02 \x01(\x03\x12\x0e\n\x06length\x18\x03 \x01(\x05\"-\n\x0cReadResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\x32\x80\x03\n\x14MasterServerToClient\x12\x33\n\tListFiles\x12\x12.gfs.StringMessage\x1a\x12.gfs.StringMessage\x12\x31\n\nCreateFile\x12\x10.gfs.FileRequest\x1a\x11.gfs.FileResponse\x12\x31\n\nAppendFile\x12\x10.gfs.FileRequest\x1a\x11.gfs.FileResponse\x12\x34\n\x0b\x43reateChunk\x12\x11.gfs.ChunkRequest\x1a\x12.gfs.ChunkResponse\x12/\n\x08ReadFile\x12\x10.gfs.ReadRequest\x1a\x11.gfs.ReadResponse\x12\x31\n\nDeleteFile\x12\x10.gfs.FileRequest\x1a\x11.gfs.FileResponse\x12\x33\n\x0cUndeleteFile\x12\x10.gfs.FileRequest\x1a\x11.gfs.FileResponse2\xdc\x01\n\x13\x43hunkServerToClient\x12/\n\x06\x43reate\x12\x11.gfs.ChunkRequest\x1a\x12.gfs.ChunkResponse\x12\x36\n\rGetChunkSpace\x12\x11.gfs.ChunkRequest\x1a\x12.gfs.ChunkResponse\x12/\n\x06\x41ppend\x12\x11.gfs.ChunkRequest\x1a\x12.gfs.ChunkResponse\x12+\n\x04Read\x12\x10.gfs.ReadRequest\x1a\x11.gfs.ReadResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gfs_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_STRINGMESSAGE']._serialized_start=18
  _globals['_STRINGMESSAGE']._serialized_end=48
  _globals['_FILEREQUEST']._serialized_start=50
  _globals['_FILEREQUEST']._serialized_end=81
  _globals['_FILERESPONSE']._serialized_start=83
  _globals['_FILERESPONSE']._serialized_end=131
  _globals['_CHUNKREQUEST']._serialized_start=133
  _globals['_CHUNKREQUEST']._serialized_end=165
  _globals['_CHUNKRESPONSE']._serialized_start=167
  _globals['_CHUNKRESPONSE']._serialized_end=241
  _globals['_READREQUEST']._serialized_start=243
  _globals['_READREQUEST']._serialized_end=306
  _globals['_READRESPONSE']._serialized_start=308
  _globals['_READRESPONSE']._serialized_end=353
  _globals['_MASTERSERVERTOCLIENT']._serialized_start=356
  _globals['_MASTERSERVERTOCLIENT']._serialized_end=740
  _globals['_CHUNKSERVERTOCLIENT']._serialized_start=743
  _globals['_CHUNKSERVERTOCLIENT']._serialized_end=963
# @@protoc_insertion_point(module_scope)
