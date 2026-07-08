# Phoenix SDK

Stable plugin contract package for the Phoenix AI Platform.

## Purpose

`phoenix-sdk` defines the small, explicit interfaces that Phoenix plugins implement.

The SDK should remain boring and stable. It should not contain plugin-specific business logic or Phoenix Core internals.

## Current Scope

SDK Contract Foundation v0.1 includes:

- Plugin interface
- Command interface
- Result format
- Context object
- Approval request
- Artifact metadata
- Manifest schema

## Design Rules

- Contract-first development.
- Backward compatibility matters.
- Deterministic workflows should remain inspectable.
- Plugins own domain-specific business logic.
- Phoenix Core owns orchestration and shared services only.
- Platform-level knowledge lives in `phoenix-pks`.

## Project Knowledge

Canonical Phoenix project state, architecture, decisions, roadmap, and agent guidance live in:

`Phoenix-AI-Platform/phoenix-pks`

Repository-specific SDK details belong here.

## Development

This package currently has no runtime dependencies.

Run tests with:

```bash
python -m pytest
```
