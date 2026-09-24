# Project Roadmap & TODO

Current Phase: **Phase 0**

## Phases

- [x] **Phase 0 — Repository Setup**
  - *Criteria*: Initial documentation, `.gitignore`, and AI rules are correctly established and merged without contradictions.

- [x] **Phase 1 — Basic Pygame Window**
  - *Criteria*: Running the main script opens a blank window that can be closed properly. A basic event loop is running at a stable framerate.

- [x] **Phase 2 — 3D Math**
  - *Criteria*: Vector3 and Matrix classes are implemented. Unit tests verify basic translation, rotation, and scaling math. *(Note: Matrix logic deferred to subsequent steps as per current Phase 2 scope strictly isolating Vector3).*

- [x] **Phase 3 — Camera + Projection**
  - *Criteria*: A virtual Camera class is implemented. Projection logic correctly maps 3D coordinates (x, y, z) to 2D screen coordinates (x, y).

- [x] **Phase 4 — Basic 3D Renderer**
  - *Criteria*: A Mesh class can hold vertices and faces. The renderer successfully draws filled triangles onto the Pygame surface with correct depth ordering (e.g., Painter's algorithm). *(Note: Depth ordering deferred to a later depth buffer/sorting phase as per strict boundaries. Render draws raw projected triangles).*

- [x] **Phase 5 — Garden Ground**
  - *Criteria*: A static 3D ground plane is rendered correctly in the scene, establishing the base environment.

- [x] **Phase 6 — Soil Grid**
  - *Criteria*: Logical soil states and a deterministic Soil Grid are implemented over the spatial Garden geometry. (Note: Mouse click raycasting deferred to interaction phase).

- [x] **Phase 7 — Rose Lifecycle Core**
  - *Criteria*: The basic state machine for a soil patch (Empty, Planted, Harvestable) is implemented and can be advanced. (Note: Advanced via Rose entity lifecycle per Phase 7 specs).

- [x] **Phase 8 — Watering & Player Actions**
  - *Criteria*: The fundamental programmatic gameplay action for WATER is defined, acting directly on the SoilGrid independently of Rose states. (Note: Interaction / Mouse clicking, and PLANTING explicitly deferred by Phase 8 prompt boundary).

- [x] **Phase 9 — Growth / Time**
  - *Criteria*: Planted-Watered soil automatically advances the rose's visual growth stage over time (Seed -> Sprout -> ... -> Bloom). Once blooming, the state becomes Harvestable. (Note: Transitioning SoilPlot to Harvestable is reserved for harvesting logic).

- [x] **Phase 10 — Harvest**
  - *Criteria*: The foundational programmatic gameplay action for HARVEST is defined. A Rose reaching BLOOM triggers the SoilPlot HARVESTABLE state, and the Harvest action securely transitions it back to EMPTY. (Note: Mouse interaction explicitly deferred).

- [x] **Phase 11 — Basic UI**
  - *Criteria*: Minimal, read-only UI layer implemented using Pygame. Safely retrieves and displays Game/Soil/Rose state globally to the player without modifying gameplay state or relying on complex plot selection mechanisms.

- [x] **Phase 12 — Save / Load**
  - *Criteria*: The garden's deterministic state (Soil states, Rose plot associations, Rose stages, and exact float growth progress) can be safely JSON-serialized to a local file and correctly restored programmatically. (Note: External save/load UI interaction deferred).

- [x] **Phase 13 — Polish**
  - *Criteria*: Visuals are tweaked, primitive meshes are refined (procedural generation), and timings are balanced for a cozy feel.