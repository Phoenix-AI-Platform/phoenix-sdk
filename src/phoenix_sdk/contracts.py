"""Stable plugin contracts for the Phoenix AI Platform.

This module intentionally contains interfaces and small immutable data containers
only. It must not depend on Phoenix Core internals or plugin-specific business
logic.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Protocol, runtime_checkable


class ResultStatus(StrEnum):
    """Normalized command result status values."""

    SUCCESS = "success"
    REQUIRES_APPROVAL = "requires_approval"
    FAILED = "failed"


def _immutable_mapping(values: Mapping[str, Any] | None = None) -> Mapping[str, Any]:
    """Return a shallow immutable mapping for SDK data containers."""

    return MappingProxyType(dict(values or {}))


@dataclass(frozen=True, slots=True)
class PluginManifest:
    """Static plugin metadata exposed to Phoenix."""

    plugin_id: str
    name: str
    version: str
    description: str
    commands: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=_immutable_mapping)

    def __post_init__(self) -> None:
        object.__setattr__(self, "commands", tuple(self.commands))
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata))


@dataclass(frozen=True, slots=True)
class ExecutionContext:
    """Context supplied by Phoenix when invoking plugin commands."""

    request_id: str
    actor_id: str | None = None
    workspace_id: str | None = None
    dry_run: bool = False
    metadata: Mapping[str, Any] = field(default_factory=_immutable_mapping)

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata))


@dataclass(frozen=True, slots=True)
class CommandRequest:
    """Structured command input passed to a plugin command."""

    command: str
    payload: Mapping[str, Any] = field(default_factory=_immutable_mapping)
    context: ExecutionContext | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "payload", _immutable_mapping(self.payload))


@dataclass(frozen=True, slots=True)
class RequiresApproval:
    """Approval request returned when a command must not proceed automatically."""

    reason: str
    summary: str
    payload: Mapping[str, Any] = field(default_factory=_immutable_mapping)

    def __post_init__(self) -> None:
        object.__setattr__(self, "payload", _immutable_mapping(self.payload))


@dataclass(frozen=True, slots=True)
class ArtifactMetadata:
    """Metadata describing an artifact produced by a plugin command."""

    artifact_id: str
    name: str
    media_type: str
    uri: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=_immutable_mapping)

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", _immutable_mapping(self.metadata))


@dataclass(frozen=True, slots=True)
class CommandResult:
    """Normalized command result returned by a plugin command."""

    status: ResultStatus
    message: str
    data: Mapping[str, Any] = field(default_factory=_immutable_mapping)
    artifacts: tuple[ArtifactMetadata, ...] = ()
    approval: RequiresApproval | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "status", ResultStatus(self.status))
        object.__setattr__(self, "data", _immutable_mapping(self.data))
        object.__setattr__(self, "artifacts", tuple(self.artifacts))


@runtime_checkable
class PluginCommand(Protocol):
    """Executable command exposed by a Phoenix plugin."""

    name: str
    description: str

    def execute(self, request: CommandRequest) -> CommandResult:
        """Execute the command with structured input and return a result."""


@runtime_checkable
class PhoenixPlugin(Protocol):
    """Protocol every Phoenix plugin must satisfy."""

    @property
    def manifest(self) -> PluginManifest:
        """Return static plugin metadata."""

    def list_commands(self) -> Sequence[PluginCommand]:
        """Return commands exposed by this plugin."""

    def get_command(self, name: str) -> PluginCommand:
        """Return a command by name or raise a plugin-defined lookup error."""
