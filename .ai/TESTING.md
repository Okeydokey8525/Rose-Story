# Testing Strategy

This document outlines the testing approach for the Rose Garden project.

## Error Handling & Debugging Policy

When encountering an error:
1. **Reproduce**: Consistently trigger the error.
2. **Identify Root Cause**: Inspect logs and state to find the exact origin.
3. **Fix Root Cause**: Implement the localized fix.
4. **Run Again**: Confirm the error is resolved.
5. **Regression Check**: Ensure the fix did not break surrounding functionality.

- **Do NOT guess and change**: Avoid randomly modifying multiple locations to "test" a fix.
- **State your hypothesis**: If the cause is unknown, clearly state your hypothesis before exploring or modifying code.

## Testing Guidelines

- **Unit Testing Math/Logic**: Ensure math systems (Vector3, matrices) have tests verifying their output.
- **Visual/Manual Testing**: The custom Pygame renderer will require visual testing (running the game) to confirm triangles, depth, and projections render correctly.
- **Validation**: Never declare a task "complete" without executing the code and verifying it works.
