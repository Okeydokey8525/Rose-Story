import pygame
from camera import Camera
from mesh import Mesh

class Renderer:
    def __init__(self, camera: Camera, surface: pygame.Surface):
        """
        Minimal 3D Software Renderer.
        """
        self.camera = camera
        self.surface = surface

    def render_mesh(self, mesh: Mesh, color: tuple[int, int, int] = (255, 255, 255)):
        """
        Projects and draws the faces of a mesh onto the Pygame surface.
        """
        for face in mesh.faces:
            # 1. Gather the 3 vertices for the current triangle face
            try:
                v1 = mesh.vertices[face[0]]
                v2 = mesh.vertices[face[1]]
                v3 = mesh.vertices[face[2]]
            except IndexError:
                # If face indices are invalid, skip this face
                continue

            # 2. Project vertices to 2D screen coordinates
            p1 = self.camera.project(v1)
            p2 = self.camera.project(v2)
            p3 = self.camera.project(v3)

            # 3. Handle clipping/rejection gracefully
            # If any vertex in the triangle is behind the camera (returns None),
            # we skip drawing the entire triangle for this minimal phase to prevent crashes/artifacts.
            if p1 is None or p2 is None or p3 is None:
                continue

            # 4. Draw the triangle
            # Draw filled polygon (triangle)
            pygame.draw.polygon(self.surface, color, [p1, p2, p3])
            # Draw wireframe outline so the shape is clearly visible even without lighting
            pygame.draw.polygon(self.surface, (0, 0, 0), [p1, p2, p3], width=1)
