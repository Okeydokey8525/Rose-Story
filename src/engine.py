import pygame
import sys

from camera import Camera
from renderer import Renderer
from mesh import Mesh
from vector3 import Vector3

class GameEngine:
    def __init__(self, width: int = 800, height: int = 600, fps: int = 60):
        pygame.init()
        pygame.display.set_caption("Rose Garden")

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = False

        # Simple background color (a soft sky blue/gray or dirt brown placeholder)
        self.bg_color = (135, 206, 235)  # Sky blue placeholder

        # Phase 13 Polish
        # Move camera for a better isometric-style overview
        self.camera = Camera(position=Vector3(3, -7, -3), screen_width=self.width, screen_height=self.height)
        self.renderer = Renderer(self.camera, self.screen)

        from garden import Garden
        from soil import SoilGrid, SoilState
        from rose import Rose, STAGE_DURATION
        from actions import water_plot, mark_harvestable, harvest_plot
        from ui import UI

        # Center the garden grid visually
        self.garden = Garden(cols=4, rows=3, cell_size=2.0, origin=Vector3(-4, 0, 5))
        self.soil_grid = SoilGrid(self.garden)

        # We will keep a few roses to demonstrate the growth pipeline
        self.roses = []
        for i in range(4):
            plot = self.soil_grid.get_plot_by_index(i)
            # Cycle through initial states for visual variety
            plot.transition_to(SoilState.PLANTED_DRY)
            plot.transition_to(SoilState.PLANTED_WATERED)
            rose = Rose(plot)
            # Offset their starting growth so they look different immediately
            rose.update(i * STAGE_DURATION * 0.8)
            self.roses.append(rose)

        self.demo_plot = self.soil_grid.get_plot_by_index(0)
        self.demo_rose = self.roses[0]

        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)
        self.ui = UI(self.screen, self.font)

        # We need this to advance growth in the demo loop
        self.last_ticks = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        from soil import SoilState
        from rose import RoseStage
        from actions import harvest_plot

        current_ticks = pygame.time.get_ticks()
        delta_time = (current_ticks - self.last_ticks) / 1000.0 # seconds
        self.last_ticks = current_ticks

        # Demo Loop: Continuously grow roses, then harvest and replant so the screen isn't static
        for rose in self.roses:
            if rose.plot.state == SoilState.PLANTED_WATERED:
                rose.update(delta_time)
                if rose.stage == RoseStage.BLOOM:
                    # When bloom is reached, automatically mark harvestable for the demo loop
                    from actions import mark_harvestable
                    mark_harvestable(rose)
            elif rose.plot.state == SoilState.HARVESTABLE:
                # Harvest it back to empty
                harvest_plot(rose.plot)
            elif rose.plot.state == SoilState.EMPTY:
                # Plant a new one to keep the loop going
                rose.plot.transition_to(SoilState.PLANTED_DRY)
                rose.plot.transition_to(SoilState.PLANTED_WATERED)
                rose.stage = RoseStage.SEED
                rose.growth_progress = 0.0

    def render(self):
        from soil import SoilState
        from rose_visuals import generate_rose_mesh, get_rose_color

        # Clear screen
        self.screen.fill(self.bg_color)

        # 1. Draw the underlying base garden geometry (dirt)
        # Using the private generated mesh for the continuous layer
        self.renderer.render_mesh(self.garden._generate_mesh(), color=(101, 67, 33), wireframe_color=None)

        # 2. Draw individual soil plots based on state
        for plot in self.soil_grid.plots:
            plot_mesh = self.garden.get_plot_mesh(plot.index)
            color = (139, 69, 19) # Default EMPTY (SaddleBrown)

            if plot.state == SoilState.PLANTED_DRY:
                color = (205, 133, 63) # Lighter dry soil
            elif plot.state == SoilState.PLANTED_WATERED:
                color = (80, 50, 20) # Darker wet soil
            elif plot.state == SoilState.HARVESTABLE:
                color = (218, 165, 32) # Goldenrod glow

            self.renderer.render_mesh(plot_mesh, color=color, wireframe_color=(50, 30, 10))

        # 3. Draw Roses
        for rose in self.roses:
            if rose.plot.state in [SoilState.PLANTED_DRY, SoilState.PLANTED_WATERED, SoilState.HARVESTABLE]:
                mesh = generate_rose_mesh(rose.stage, rose.position)
                color = get_rose_color(rose.stage)
                self.renderer.render_mesh(mesh, color=color)

        # Draw UI
        self.ui.render(self.demo_plot, self.demo_rose)

        # Update display
        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)

        self.cleanup()

    def cleanup(self):
        pygame.quit()
        sys.exit()
