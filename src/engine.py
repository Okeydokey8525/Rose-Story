import pygame
import sys

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
