import math
from vector3 import Vector3

class Camera:
    def __init__(self, position: Vector3 = None, fov: float = 90.0,
                 screen_width: int = 800, screen_height: int = 600,
                 near: float = 0.1, far: float = 1000.0):
        self.position = position if position is not None else Vector3(0, 0, 0)
        self.fov = fov
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.near = near
        self.far = far

        # Calculate aspect ratio and FOV scaling factor
        self.aspect_ratio = screen_width / screen_height if screen_height != 0 else 1.0
        # fov_rad is the vertical field of view
        fov_rad = math.radians(self.fov)
        self.fov_scale = 1.0 / math.tan(fov_rad / 2.0)

    def project(self, world_point: Vector3) -> tuple[float, float]:
        """
        Projects a 3D world coordinate into a 2D screen coordinate.
        Assumes the camera is looking down the positive Z axis for simplicity in this phase.
        Right-handed coordinate system: X is Right, Y is Down (Pygame screen space), Z is Forward.
        Returns None if the point is behind or exactly at the camera plane (z <= 0) to avoid division by zero
        and to handle clipping minimally.
        """
        # 1. Translate point to camera space
        # Here we just subtract the camera position.
        # Orientation is assumed fixed (looking down +Z) for this minimal implementation.
        cam_space = world_point - self.position

        # 2. Check if the point is behind the camera or too close (clipping)
        # Using a very small threshold if near is 0, otherwise use near plane.
        if cam_space.z < self.near:
            return None

        # 3. Perspective Projection
        # Divide by Z to create the perspective effect (things further away are smaller/closer to center)
        # Apply the FOV scale to adjust for the camera lens width
        x_proj = (cam_space.x * self.fov_scale) / cam_space.z

        # Adjust y projection by aspect ratio so circles don't look like ovals based on window size
        y_proj = (cam_space.y * self.fov_scale * self.aspect_ratio) / cam_space.z

        # 4. Convert to Screen Coordinates
        # Pygame coordinates: (0,0) is top-left.
        # Center of the screen is (width/2, height/2).
        # We map [-1, 1] normalized device coordinates to [0, width] and [0, height].
        screen_x = (x_proj + 1.0) * 0.5 * self.screen_width
        screen_y = (y_proj + 1.0) * 0.5 * self.screen_height

        return (screen_x, screen_y)
