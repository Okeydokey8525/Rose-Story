# Architecture & Technical Design

This document details the software architecture required to build a 3D game using only Python and Pygame.

## Core Principle

The project is built entirely on Pygame. It uses a custom-built 3D software renderer. **External 3D engines are strictly forbidden.**

## Incremental 3D Engine Architecture

The 3D engine will be built from the ground up, following these incremental milestones:

1. **Math Fundamentals**:
   - Vector3 structures for positioning.
   - Matrix operations for transformations (Translation, Rotation, Scaling).
2. **Camera & Projection**:
   - A virtual Camera to determine the viewpoint.
   - Perspective Projection math to map 3D coordinates to the 2D Pygame surface.
3. **Rendering Pipeline**:
   - `Mesh` representation (vertices, edges, faces).
   - Triangle rasterization (drawing filled polygons in Pygame).
   - Depth handling (Z-buffering or painter's algorithm) to correctly order objects front-to-back.
4. **Lighting**:
   - Basic directional or flat lighting for depth perception.

## Game Logic Structure

- **Game Engine Loop**: Handles events, updates game state, and calls the renderer.
- **Scene Management**: Holds the entities (Soil grid, Roses, Camera).
- **Entity Component / OOP**: Entities in the world (e.g., Rose plants) handle their own state (growth timer, watered status) and provide rendering data to the 3D pipeline.
- **Input System**: Translates 2D mouse clicks on the screen into 3D world interactions (raycasting against the soil grid).
