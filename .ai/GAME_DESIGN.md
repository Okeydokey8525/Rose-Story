# Game Design

This document details the core gameplay mechanics and design for the Rose Garden MVP.

## Core Gameplay Loop & Player Actions

The core gameplay consists of player actions interacting with the soil grid:
- **PLANT**: The player plants a seed in empty soil.
- **WATER**: The player waters planted soil.
- **HARVEST**: The player collects a fully grown rose, resetting the soil.

## Soil States

The logic state of a soil patch governs what actions can be taken and what visuals are displayed:
1. **Empty**: No plant exists. Only PLANT action is valid.
2. **Planted - Dry**: A plant exists but growth is halted until watered. Only WATER action is valid.
3. **Planted - Watered**: A plant exists and is actively growing. Time advances its visual growth stage.
4. **Harvestable**: The plant has reached its final growth stage. Only HARVEST action is valid.

## Rose Visual Growth Stages

A rose progresses through the following distinct visual stages as time passes in the `Planted - Watered` soil state:
1. **Seed**: Visually bare or small seed indicator.
2. **Sprout**: Initial growth.
3. **Young Plant**: Growing foliage.
4. **Bud**: Preparing to flower.
5. **Bloom**: Fully grown flower. Reaching this visual stage transitions the Soil State to `Harvestable`.

## Interaction Model

- **Camera**: Observes the garden from a fixed or limited perspective.
- **Player Input**: Interacts directly with the soil grid (e.g., clicking on a soil patch to plant, water, or harvest).
- **Time/Growth**: Plants advance through their visual growth stages over time, provided their soil state is `Planted - Watered`.