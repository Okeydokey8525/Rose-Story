# Project Roadmap & TODO

Current Phase: **Phase 0**

## Phases

- [x] **Phase 0 — Repository Setup**
  - *Criteria*: Initial documentation, `.gitignore`, and AI rules are correctly established and merged without contradictions.

- [ ] **Phase 1 — Basic Pygame Window**
  - *Criteria*: Running the main script opens a blank window that can be closed properly. A basic event loop is running at a stable framerate.

- [ ] **Phase 2 — 3D Math**
  - *Criteria*: Vector3 and Matrix classes are implemented. Unit tests verify basic translation, rotation, and scaling math.

- [ ] **Phase 3 — Camera + Projection**
  - *Criteria*: A virtual Camera class is implemented. Projection logic correctly maps 3D coordinates (x, y, z) to 2D screen coordinates (x, y).

- [ ] **Phase 4 — Basic 3D Renderer**
  - *Criteria*: A Mesh class can hold vertices and faces. The renderer successfully draws filled triangles onto the Pygame surface with correct depth ordering (e.g., Painter's algorithm).

- [ ] **Phase 5 — Garden Ground**
  - *Criteria*: A static 3D ground plane is rendered correctly in the scene, establishing the base environment.

- [ ] **Phase 6 — Soil Grid**
  - *Criteria*: An interactable grid of soil patches is rendered. Raycasting or a similar method correctly maps a 2D mouse click to the specific 3D soil tile.

- [ ] **Phase 7 — Rose Lifecycle Core**
  - *Criteria*: The basic state machine for a soil patch (Empty, Planted, Harvestable) is implemented and can be advanced.

- [ ] **Phase 8 — Watering & Player Actions**
  - *Criteria*: The player can click to PLANT a seed (Empty -> Planted-Dry). The player can click to WATER (Planted-Dry -> Planted-Watered).

- [ ] **Phase 9 — Growth / Time**
  - *Criteria*: Planted-Watered soil automatically advances the rose's visual growth stage over time (Seed -> Sprout -> ... -> Bloom). Once blooming, the state becomes Harvestable.

- [ ] **Phase 10 — Harvest**
  - *Criteria*: The player can click a Harvestable plant to collect it, resetting the soil patch back to Empty.

- [ ] **Phase 11 — Basic UI**
  - *Criteria*: Simple on-screen text displays the current tool, action prompts, and general status.

- [ ] **Phase 12 — Save / Load**
  - *Criteria*: The garden's state (soil states, plant growth levels) can be saved to a local file and successfully restored upon restarting the game.

- [ ] **Phase 13 — Polish**
  - *Criteria*: Visuals are tweaked, primitive meshes are refined (procedural generation), and timings are balanced for a cozy feel.