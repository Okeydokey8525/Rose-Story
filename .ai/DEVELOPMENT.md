# Development Guidelines

This document outlines the standard development process and coding principles for the Rose Garden project.

## Development Cycle

Always adhere to the following workflow when developing new features or fixing bugs:

1. **INSPECT**: Understand the current state, read documentation and relevant code.
2. **PLAN**: Outline the steps needed to implement the feature or fix.
3. **IMPLEMENT**: Write the code incrementally.
4. **RUN**: Execute the code locally to ensure it functions in the environment.
5. **TEST**: Validate against regressions and ensure correct behavior.
6. **REVIEW**: Check code quality, structure, and readability.
7. **UPDATE DOC/TODO**: Keep documentation, changelogs, and TODO lists updated.

## Coding Principles

- **Readable and Maintainable**: Code should be clean, commented where necessary, and easy to follow.
- **Modular**: Build the systems (renderer, game logic, input) so they are decoupled where appropriate.
- **Testable**: Design functions and classes that can be easily validated.
- **Simplicity**: Do not introduce complex abstractions "just in case." Prioritize the MVP.
- **No Blind Coding**: Ensure you understand the problem and environment before writing code.
- **Preserve Working Code**: Do not delete or entirely rewrite functional code without identifying the specific reason and impact.

## Refactoring Policy

- Refactor only when it directly benefits the current task or resolves a known architectural debt.
- Ensure thorough testing before and after a refactor.
