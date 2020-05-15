"""
Protocol objects representing different implementations of the same classes.
"""

# Copyright (C) 2020 The Psycopg Team

import codecs
from typing import Any, Callable, Dict, Generator, Iterable, List, Mapping
from typing import Optional, Sequence, Tuple, Type, TypeVar, Union
from typing import TYPE_CHECKING
from typing_extensions import Protocol

from . import pq

if TYPE_CHECKING:
    from .connection import BaseConnection  # noqa
    from .cursor import BaseCursor  # noqa
    from .adapt import Dumper, Loader  # noqa
    from .waiting import Wait, Ready  # noqa

# Part of the module interface (just importing it makes mypy unhappy)
Format = pq.Format

EncodeFunc = Callable[[str], Tuple[bytes, int]]
DecodeFunc = Callable[[bytes], Tuple[str, int]]

Query = Union[str, bytes]
Params = Union[Sequence[Any], Mapping[str, Any]]


# Waiting protocol types

RV = TypeVar("RV")
PQGen = Generator[Tuple[int, "Wait"], "Ready", RV]


# Adaptation types

AdaptContext = Union[None, "BaseConnection", "BaseCursor", "Transformer"]

MaybeOid = Union[Optional[bytes], Tuple[Optional[bytes], int]]
DumpFunc = Callable[[Any], MaybeOid]
DumperType = Union[Type["Dumper"], DumpFunc]
DumpersMap = Dict[Tuple[type, Format], DumperType]

LoadFunc = Callable[[bytes], Any]
LoaderType = Union[Type["Loader"], LoadFunc]
LoadersMap = Dict[Tuple[int, Format], LoaderType]


class Transformer(Protocol):
    def __init__(self, context: AdaptContext = None):
        ...

    @property
    def connection(self) -> Optional["BaseConnection"]:
        ...

    @property
    def codec(self) -> codecs.CodecInfo:
        ...

    @property
    def pgresult(self) -> Optional["pq.proto.PGresult"]:
        ...

    @pgresult.setter
    def pgresult(self, result: Optional["pq.proto.PGresult"]) -> None:
        ...

    @property
    def dumpers(self) -> DumpersMap:
        ...

    @property
    def loaders(self) -> LoadersMap:
        ...

    def set_row_types(self, types: Sequence[Tuple[int, Format]]) -> None:
        ...

    def dump_sequence(
        self, objs: Iterable[Any], formats: Iterable[Format]
    ) -> Tuple[List[Optional[bytes]], List[int]]:
        ...

    def dump(self, obj: None, format: Format = Format.TEXT) -> MaybeOid:
        ...

    def get_dump_function(self, src: type, format: Format) -> DumpFunc:
        ...

    def lookup_dumper(self, src: type, format: Format) -> DumperType:
        ...

    def load_row(self, row: int) -> Optional[Tuple[Any, ...]]:
        ...

    def load_sequence(
        self, record: Sequence[Optional[bytes]]
    ) -> Tuple[Any, ...]:
        ...

    def load(self, data: bytes, oid: int, format: Format = Format.TEXT) -> Any:
        ...

    def get_load_function(self, oid: int, format: Format) -> LoadFunc:
        ...

    def lookup_loader(self, oid: int, format: Format) -> LoaderType:
        ...
