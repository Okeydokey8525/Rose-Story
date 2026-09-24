from vector3 import Vector3

class Mesh:
    def __init__(self, vertices: list[Vector3] = None, faces: list[tuple[int, int, int]] = None):
        """
        A minimal mesh representation.
        vertices: list of Vector3 points in 3D space.
        faces: list of tuples, where each tuple contains 3 integer indices pointing to the vertices list.
        """
        self.vertices = vertices if vertices is not None else []
        self.faces = faces if faces is not None else []
