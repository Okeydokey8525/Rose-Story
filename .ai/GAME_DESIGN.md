# Game Design

This document details the core gameplay mechanics and design for the Rose Garden MVP.

## Core Gameplay Loop

The game loop is a continuous cycle of tending to roses on a soil grid:
1. `EMPTY SOIL`
2. `PLANT`
3. `WATER`
4. `GROW`
5. `BUD`
6. `BLOOM`
7. `HARVEST`
8. `REPLANT` (Returns to Empty Soil)

## Rose Lifecycle Stages

A rose progresses through the following distinct stages:
1. **Seed**: Planted in the soil.
2. **Sprout**: Initial growth after watering.
3. **Young Plant**: Growing foliage.
4. **Bud**: Preparing to flower.
5. **Bloom**: Fully grown flower, ready for harvest.
6. **Harvest**: The act of collecting the rose and clearing the soil.

## Interaction Model

- **Camera**: Observes the garden.
- **Player Input**: Interacts directly with the soil grid (e.g., clicking on a soil patch to plant, water, or harvest).
- **Time/Growth**: Plants advance through their lifecycle stages over time, provided they are adequately cared for (e.g., watered).
