from vector3 import Vector3
from mesh import Mesh
from rose import RoseStage

def generate_rose_mesh(stage: RoseStage, position: Vector3) -> Mesh:
    """
    Generates a simple, procedural 3D Mesh representing the given RoseStage.
    All geometry is offset by the given world position.
    """
    vertices = []
    faces = []

    # Base height offset to sit on top of the soil
    base_y = position.y - 0.1 # Pygame Y is down, so negative is UP

    if stage == RoseStage.SEED:
        # A tiny pyramid
        size = 0.2
        vertices = [
            Vector3(position.x, base_y - size, position.z), # Top
            Vector3(position.x - size, base_y, position.z - size),
            Vector3(position.x + size, base_y, position.z - size),
            Vector3(position.x + size, base_y, position.z + size),
            Vector3(position.x - size, base_y, position.z + size)
        ]
        faces = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1)]

    elif stage == RoseStage.SPROUT:
        # A small thin upright triangle
        height = 0.5
        width = 0.2
        vertices = [
            Vector3(position.x, base_y - height, position.z), # Tip
            Vector3(position.x - width, base_y, position.z),
            Vector3(position.x + width, base_y, position.z)
        ]
        faces = [(0, 1, 2)]

    elif stage == RoseStage.YOUNG_PLANT:
        # A taller plant with a leaf
        height = 1.0
        width = 0.3
        vertices = [
            Vector3(position.x, base_y - height, position.z), # Tip
            Vector3(position.x - width, base_y, position.z - width),
            Vector3(position.x + width, base_y, position.z + width),
            Vector3(position.x - width*2, base_y - height/2, position.z) # Leaf
        ]
        faces = [(0, 1, 2), (0, 1, 3)]

    elif stage == RoseStage.BUD:
        # A tall plant with a bulb on top
        height = 1.5
        width = 0.3
        bulb_size = 0.4
        vertices = [
            Vector3(position.x, base_y - height, position.z), # Stem top
            Vector3(position.x - width, base_y, position.z - width),
            Vector3(position.x + width, base_y, position.z + width),
            # Bulb vertices (diamond)
            Vector3(position.x, base_y - height - bulb_size, position.z), # Bulb top
            Vector3(position.x - bulb_size, base_y - height, position.z),
            Vector3(position.x + bulb_size, base_y - height, position.z)
        ]
        faces = [
            (0, 1, 2), # Stem
            (3, 4, 5), (0, 4, 5) # Bulb
        ]

    elif stage == RoseStage.BLOOM:
        # A tall plant with a wide bloom
        height = 1.8
        width = 0.3
        bloom_w = 0.8
        bloom_h = 0.6
        vertices = [
            Vector3(position.x, base_y - height, position.z), # Stem top
            Vector3(position.x - width, base_y, position.z - width),
            Vector3(position.x + width, base_y, position.z + width),
            # Bloom (wide star/diamond)
            Vector3(position.x, base_y - height - bloom_h, position.z), # Top petal
            Vector3(position.x - bloom_w, base_y - height - bloom_h/2, position.z), # Left
            Vector3(position.x + bloom_w, base_y - height - bloom_h/2, position.z), # Right
            Vector3(position.x, base_y - height + bloom_h/2, position.z) # Bottom petal
        ]
        faces = [
            (0, 1, 2), # Stem
            (3, 4, 6), (3, 6, 5) # Bloom
        ]

    return Mesh(vertices, faces)

def get_rose_color(stage: RoseStage) -> tuple[int, int, int]:
    """Returns the primary render color for a given rose stage."""
    if stage == RoseStage.SEED:
        return (139, 69, 19) # SaddleBrown
    elif stage == RoseStage.SPROUT:
        return (144, 238, 144) # LightGreen
    elif stage == RoseStage.YOUNG_PLANT:
        return (34, 139, 34) # ForestGreen
    elif stage == RoseStage.BUD:
        return (255, 105, 180) # HotPink
    elif stage == RoseStage.BLOOM:
        return (255, 0, 0) # Red
    return (255, 255, 255)
