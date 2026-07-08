from __future__ import annotations

import pytest

from phoenix_sdk import (
    ArtifactMetadata,
    CommandRequest,
    CommandResult,
    ExecutionContext,
    PhoenixPlugin,
    PluginCommand,
    PluginManifest,
    RequiresApproval,
    ResultStatus,
)


class EchoCommand:
    name = "echo"
    description = "Echoes the payload."

    def execute(self, request: CommandRequest) -> CommandResult:
        return CommandResult(
            status=ResultStatus.SUCCESS,
            message="ok",
            data={"payload": request.payload},
        )


class EchoPlugin:
    def __init__(self) -> None:
        self._command = EchoCommand()

    @property
    def manifest(self) -> PluginManifest:
        return PluginManifest(
            plugin_id="test.echo",
            name="Echo",
            version="0.1.0",
            description="Test plugin",
            commands=(self._command.name,),
        )

    def list_commands(self) -> tuple[EchoCommand, ...]:
        return (self._command,)

    def get_command(self, name: str) -> EchoCommand:
        if name != self._command.name:
            raise KeyError(name)
        return self._command


def test_plugin_protocol_runtime_check() -> None:
    plugin = EchoPlugin()

    assert isinstance(plugin, PhoenixPlugin)
    assert isinstance(plugin.get_command("echo"), PluginCommand)


def test_command_execution_contract() -> None:
    plugin = EchoPlugin()
    request = CommandRequest(
        command="echo",
        payload={"hello": "world"},
        context=ExecutionContext(request_id="req-1", dry_run=True),
    )

    result = plugin.get_command("echo").execute(request)

    assert result.status is ResultStatus.SUCCESS
    assert result.message == "ok"
    assert result.data["payload"]["hello"] == "world"


def test_mapping_fields_are_immutable() -> None:
    request = CommandRequest(command="echo", payload={"a": 1})

    with pytest.raises(TypeError):
        request.payload["a"] = 2  # type: ignore[index]


def test_result_supports_approval_and_artifacts() -> None:
    artifact = ArtifactMetadata(
        artifact_id="artifact-1",
        name="proposal.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        uri="file:///tmp/proposal.docx",
    )
    approval = RequiresApproval(
        reason="customer_output",
        summary="Human review required before sending customer document.",
    )

    result = CommandResult(
        status=ResultStatus.REQUIRES_APPROVAL,
        message="approval required",
        artifacts=(artifact,),
        approval=approval,
    )

    assert result.status is ResultStatus.REQUIRES_APPROVAL
    assert result.artifacts == (artifact,)
    assert result.approval is approval
