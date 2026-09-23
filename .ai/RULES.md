# Project Rules

This document outlines the strict, non-negotiable rules for the Rose Garden project.

## 1. 3D Renderer Constraint
- **No External 3D Engines**: You must NOT use Unity, Godot, Panda3D, Ursina, Unreal, or any other external 3D engine.
- **Pure Python & Pygame**: The 3D renderer must be built entirely from scratch using Python and Pygame.
- **Incremental Implementation**: The 3D engine should be built incrementally. Do not over-engineer the renderer from the beginning. Start with Vector3, Camera, Perspective Projection, Mesh, Triangle Rendering, Depth handling, and basic lighting.

## 2. Minimal Viable Product (MVP) Scope Constraint
- **Focus strictly on the Rose**: The core loop revolves only around planting, watering, and harvesting a rose on empty soil.
- **Do not add unrequested features**: Do not add multiplayer, combat, free-roaming character controllers, complex inventory, shops, multiple flower types, farming automation, or online systems unless specifically requested.
- **Camera limitation**: The camera observes the garden, and the player interacts directly with the soil grid. There is no free-roaming character.

## 3. Asset Policy
- Use procedural geometry, primitive meshes, and simple generated visuals for the MVP.
- Do not mass-download external assets without permission.
- If external assets are needed: cite the source, verify the license, and specify the usage purpose.
- Do not commit trash, cache, or unnecessary generated files.

## 4. Git Policy
- Make small, meaningful commits.
- Avoid vague commit messages like "update", "fix", or "changes".
- Use the `.gitignore` effectively to keep the repo clean of cache and temporary files.

## 5. File Constraints & Modification
- Do not blindly write code. Follow the `INSPECT -> PLAN -> IMPLEMENT -> RUN -> TEST -> REVIEW` cycle.
- Do not rewrite the entire project to fix a small bug.
- Do not delete functioning code unless the reason is clearly identified.
- Do not create abstractions "just in case" they are needed later. Keep it simple and focused on the immediate roadmap phase.
