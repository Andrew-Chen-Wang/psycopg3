"""
psycopg3 libpq wrapper

This package exposes the libpq functionalities as Python objects and functions.

The real implementation (the binding to the C library) is
implementation-dependant but all the implementations share the same interface.
"""

# Copyright (C) 2020 The Psycopg Team

from .enums import (
    ConnStatus,
    PollingStatus,
    ExecStatus,
    TransactionStatus,
    Ping,
    DiagnosticField,
    EventId,
)
from .encodings import py_codecs
from .misc import error_message

from . import pq_ctypes as pq_module

PGconn = pq_module.PGconn
PGresult = pq_module.PGresult
PQerror = pq_module.PQerror
Conninfo = pq_module.Conninfo

__all__ = (
    "ConnStatus",
    "PollingStatus",
    "TransactionStatus",
    "ExecStatus",
    "Ping",
    "DiagnosticField",
    "EventId",
    "PGconn",
    "Conninfo",
    "PQerror",
    "error_message",
    "py_codecs",
)
