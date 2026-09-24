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

        # Phase 4: Minimal Demonstration Setup
        self.camera = Camera(screen_width=self.width, screen_height=self.height)
        self.renderer = Renderer(self.camera, self.screen)

        # A simple triangle placed in front of the camera (Z = 5)
        self.test_mesh = Mesh(
            vertices=[
                Vector3(0, -2, 5),    # Top
                Vector3(-2, 2, 5),    # Bottom Left
                Vector3(2, 2, 5)      # Bottom Right
            ],
            faces=[(0, 1, 2)]
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        # Update game state here
        pass

    def render(self):
        # Clear screen
        self.screen.fill(self.bg_color)

        # Draw everything here
        self.renderer.render_mesh(self.test_mesh, color=(255, 100, 100))

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
