"""
Adapers for numeric types.
"""

# Copyright (C) 2020 The Psycopg Team

import codecs
import struct
from decimal import Decimal
from typing import Tuple

from ..adapt import Dumper, Loader
from .oids import builtins

INT2_OID = builtins["int2"].oid
INT4_OID = builtins["int4"].oid
INT8_OID = builtins["int8"].oid
FLOAT8_OID = builtins["float8"].oid
NUMERIC_OID = builtins["numeric"].oid

_encode = codecs.lookup("ascii").encode
_decode = codecs.lookup("ascii").decode

_int2_struct = struct.Struct("!h")
_int4_struct = struct.Struct("!i")
_int8_struct = struct.Struct("!q")
_oid_struct = struct.Struct("!I")
_float4_struct = struct.Struct("!f")
_float8_struct = struct.Struct("!d")


@Dumper.text(int)
def dump_int(obj: int) -> Tuple[bytes, int]:
    # We don't know the size of it, so we have to return a type big enough
    return _encode(str(obj))[0], NUMERIC_OID


def dump_binary_int(obj: int) -> Tuple[bytes, int]:
    if -0x8000 <= obj <= 0x7FFF:
        return _int2_struct.pack(obj), INT2_OID
    if -0x80000000 <= obj <= 0x7FFFFFFF:
        return _int4_struct.pack(obj), INT4_OID

    # TODO: must return numeric if it doesn't fit in 64 bits either
    return _int8_struct.pack(obj), INT8_OID


# These functions are not registered automatically: to use on demand
def dump_binary_int2(obj: int) -> Tuple[bytes, int]:
    return _int2_struct.pack(obj), INT2_OID


def dump_binary_int4(obj: int) -> Tuple[bytes, int]:
    return _int4_struct.pack(obj), INT4_OID


def dump_binary_int8(obj: int) -> Tuple[bytes, int]:
    return _int8_struct.pack(obj), INT8_OID


@Dumper.text(float)
def dump_float(obj: float) -> Tuple[bytes, int]:
    # Float can't be bigger than this instead
    return _encode(str(obj))[0], FLOAT8_OID


@Dumper.binary(float)
def dump_binary_float(obj: float) -> Tuple[bytes, int]:
    return _float8_struct.pack(obj), FLOAT8_OID


@Dumper.text(Decimal)
def dump_decimal(obj: Decimal) -> Tuple[bytes, int]:
    return _encode(str(obj))[0], NUMERIC_OID


_bool_dump = {
    True: (b"t", builtins["bool"].oid),
    False: (b"f", builtins["bool"].oid),
}
_bool_binary_dump = {
    True: (b"\x01", builtins["bool"].oid),
    False: (b"\x00", builtins["bool"].oid),
}


@Dumper.text(bool)
def dump_bool(obj: bool) -> Tuple[bytes, int]:
    return _bool_dump[obj]


@Dumper.binary(bool)
def dump_binary_bool(obj: bool) -> Tuple[bytes, int]:
    return _bool_binary_dump[obj]


@Loader.text(builtins["int2"].oid)
@Loader.text(builtins["int4"].oid)
@Loader.text(builtins["int8"].oid)
@Loader.text(builtins["oid"].oid)
def load_int(data: bytes) -> int:
    return int(_decode(data)[0])


@Loader.binary(builtins["int2"].oid)
def load_binary_int2(data: bytes) -> int:
    rv: int = _int2_struct.unpack(data)[0]
    return rv


@Loader.binary(builtins["int4"].oid)
def load_binary_int4(data: bytes) -> int:
    rv: int = _int4_struct.unpack(data)[0]
    return rv


@Loader.binary(builtins["int8"].oid)
def load_binary_int8(data: bytes) -> int:
    rv: int = _int8_struct.unpack(data)[0]
    return rv


@Loader.binary(builtins["oid"].oid)
def load_binary_oid(data: bytes) -> int:
    rv: int = _oid_struct.unpack(data)[0]
    return rv


@Loader.text(builtins["float4"].oid)
@Loader.text(builtins["float8"].oid)
def load_float(data: bytes) -> float:
    # it supports bytes directly
    return float(data)


@Loader.binary(builtins["float4"].oid)
def load_binary_float4(data: bytes) -> float:
    rv: float = _float4_struct.unpack(data)[0]
    return rv


@Loader.binary(builtins["float8"].oid)
def load_binary_float8(data: bytes) -> float:
    rv: float = _float8_struct.unpack(data)[0]
    return rv


@Loader.text(builtins["numeric"].oid)
def load_numeric(data: bytes) -> Decimal:
    return Decimal(_decode(data)[0])


_bool_loads = {b"t": True, b"f": False}
_bool_binary_loads = {b"\x01": True, b"\x00": False}


@Loader.text(builtins["bool"].oid)
def load_bool(data: bytes) -> bool:
    return _bool_loads[data]


@Loader.binary(builtins["bool"].oid)
def load_binary_bool(data: bytes) -> bool:
    return _bool_binary_loads[data]
