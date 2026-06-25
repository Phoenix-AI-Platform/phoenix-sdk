[copilot-instructions.md](https://github.com/user-attachments/files/29357248/copilot-instructions.md)
# Phoenix Copilot Instructions

You are working inside the Phoenix AI Platform.

Always follow the Phoenix Constitution in `phoenix-docs`:

- `00_VISION.md`
- `01_MISSION.md`
- `02_PRINCIPLES.md`
- `03_ARCHITECTURE.md`
- `04_PLUGIN_STANDARD.md`
- `05_CODING_STANDARD.md`
- `06_ROADMAP.md`
- `adr/`

Core rules:

1. AI should complete work, not merely answer questions.
2. Humans remain in control.
3. Phoenix Core owns orchestration and shared services only.
4. Plugins own domain-specific business logic.
5. Keep Core small.
6. Every feature must save measurable time.
7. Every feature must become a reusable capability.
8. Natural language starts workflows; structured data executes them.
9. Professional output is non-negotiable.
10. Do not hardcode personal machine paths, secrets, or one-off assumptions.

Before implementing meaningful changes:

- Identify which repo/module owns the change.
- Keep changes small and reviewable.
- Add or update tests when behavior changes.
- Update docs or ADRs if architecture changes.
- State assumptions clearly in PR descriptions.

Do not put plugin-specific business logic into Phoenix Core.


Repository-specific guidance:

This repository defines the stable plugin contract.

Keep the SDK small, boring, and explicit.

Do not expose Phoenix Core internals.

Focus on:

- Plugin interface
- Command interface
- Result format
- Context object
- Approval request
- Artifact metadata
- Manifest schema

Every SDK change should consider backward compatibility.
