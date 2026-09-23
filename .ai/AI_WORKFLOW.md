# AI Workflow and Token Policy

This document defines how AI agents must operate within this repository. **Token optimization and accuracy are paramount.**

## Core Principles

- **Small Context, High Accuracy**: Keep the context small but sufficient. Do not sacrifice correctness to save tokens.
- **Targeted Reading**: Read only the necessary files. Do not dump the entire repository into the context.
- **Cache & Reuse**: Do not re-read files if they haven't changed. Reuse search results and file contents from the current session.
- **Incremental Verification**: Verify small points of data rather than requesting large summaries.

## Task Classification & Work Budget

- **SMALL Task** (Typo, small bug, rename, small UI tweak):
  - Do directly.
  - Inspect minimally, edit, test.
  - **No Subagents**.

- **MEDIUM Task** (New mechanic, module, modifying a few related files):
  - Inspect relevant files. Make a short plan. Implement. Test.
  - Consider a subagent *only* if it genuinely reduces time/context (e.g., separate research while coding).

- **LARGE Task** (Designing renderer, heavy refactor, complex debugging):
  - Architecture inspection -> split tasks.
  - Subagents are permitted if tasks are strictly independent.
  - Implement and test in parts.

- **RESEARCH/COMPLEX**:
  - Can use specialized subagents for distinct scope discovery.

## Subagent Policy

- **Do NOT spawn subagents just to look "professional."**
- Each subagent must have a precise, 1-sentence mission.
- Subagents must have strict boundaries (specific folders/files).
- Only use subagents when tasks are truly independent and parallel execution reduces total work.

## Validation Rule

- **Never skip validation.** Do not cut corners on testing to save tokens.
- Execute targeted checks, build/test, fix, and perform final verification.
