import pygame
from soil import SoilPlot
from rose import Rose

class UI:
    def __init__(self, surface: pygame.Surface, font: pygame.font.Font):
        """
        Minimal UI layer for displaying game state.
        Reads state only. Does not mutate gameplay or hold duplicate states.
        """
        self.surface = surface
        self.font = font

        # UI configuration
        self.panel_rect = pygame.Rect(20, 20, 300, 140)

        # Create a transparent surface for the panel
        self.panel_surf = pygame.Surface((self.panel_rect.width, self.panel_rect.height), pygame.SRCALPHA)
        self.panel_color = (30, 30, 30, 210) # Dark gray with alpha
        self.border_color = (200, 200, 200, 255)
        self.text_color = (240, 240, 240)    # Soft White
        self.highlight_color = (255, 215, 0) # Gold

    def render(self, plot: SoilPlot = None, rose: Rose = None):
        """
        Renders the informational UI overlay onto the pygame surface.
        """
        # Draw background panel with transparency
        self.panel_surf.fill((0, 0, 0, 0))
        pygame.draw.rect(self.panel_surf, self.panel_color, self.panel_surf.get_rect(), border_radius=8)
        pygame.draw.rect(self.panel_surf, self.border_color, self.panel_surf.get_rect(), width=2, border_radius=8)
        self.surface.blit(self.panel_surf, self.panel_rect.topleft)

        # Prepare text strings
        title_text = "Rose Garden (Demo)"

        plot_text = "Plot: None"
        if plot:
            # Clean up enum names for display
            state_str = plot.state.name.replace("_", " ").title()
            plot_text = f"Soil: {state_str}"

        rose_text = "Rose: None"
        if rose:
            stage_str = rose.stage.name.replace("_", " ").title()
            rose_text = f"Stage: {stage_str}"

        instructions_text = "State continuously loops for visual demo."

        # Render text surfaces
        title_surf = self.font.render(title_text, True, self.highlight_color)
        plot_surf = self.font.render(plot_text, True, self.text_color)
        rose_surf = self.font.render(rose_text, True, self.text_color)
        inst_surf = self.font.render(instructions_text, True, (150, 150, 150))

        # Blit to main surface
        self.surface.blit(title_surf, (self.panel_rect.x + 15, self.panel_rect.y + 15))
        self.surface.blit(plot_surf, (self.panel_rect.x + 15, self.panel_rect.y + 50))
        self.surface.blit(rose_surf, (self.panel_rect.x + 15, self.panel_rect.y + 75))
        self.surface.blit(inst_surf, (self.panel_rect.x + 15, self.panel_rect.y + 105))
