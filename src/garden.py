from vector3 import Vector3
from mesh import Mesh

class Garden:
    def __init__(self, cols: int = 4, rows: int = 3, cell_size: float = 2.0, origin: Vector3 = None):
        """
        Creates a spatial grid for the garden.
        cols: Number of cells along the X axis.
        rows: Number of cells along the Z axis (depth into the screen).
        cell_size: The world-space size of a single square cell.
        origin: The starting world position of the top-left corner of the grid.
        """
        self.cols = cols
        self.rows = rows
        self.cell_size = cell_size
        self.origin = origin if origin is not None else Vector3(0, 0, 0)

        self.cell_positions = self._generate_cell_positions()
        self.mesh = self._generate_mesh()

    def _generate_cell_positions(self) -> list[Vector3]:
        """
        Generates the deterministic center position of every cell in the grid.
        Cells are ordered row by row (Z axis first, then X axis).
        """
        positions = []
        half_size = self.cell_size / 2.0

        for r in range(self.rows):
            for c in range(self.cols):
                # Calculate the center of the cell based on the origin
                x = self.origin.x + (c * self.cell_size) + half_size
                y = self.origin.y # Flat ground
                z = self.origin.z + (r * self.cell_size) + half_size
                positions.append(Vector3(x, y, z))

        return positions

    def get_plot_mesh(self, index: int) -> Mesh:
        """
        Generates the visual geometry for a single garden cell.
        Useful for rendering individual plots with different colors based on SoilState.
        """
        r = index // self.cols
        c = index % self.cols

        x0 = self.origin.x + (c * self.cell_size)
        x1 = x0 + self.cell_size
        z0 = self.origin.z + (r * self.cell_size)
        z1 = z0 + self.cell_size
        y = self.origin.y

        # Shrink the plot slightly so grid lines form naturally between cells
        pad = self.cell_size * 0.05
        x0 += pad
        x1 -= pad
        z0 += pad
        z1 -= pad

        top_left = Vector3(x0, y, z0)
        top_right = Vector3(x1, y, z0)
        bottom_left = Vector3(x0, y, z1)
        bottom_right = Vector3(x1, y, z1)

        return Mesh(
            vertices=[top_left, top_right, bottom_left, bottom_right],
            faces=[(0, 1, 2), (1, 3, 2)]
        )

    def _generate_mesh(self) -> Mesh:
        """
        Generates the continuous underlying ground geometry for the entire garden grid.
        This represents the dirt/grass underneath the active plots.
        """
        x0 = self.origin.x
        x1 = self.origin.x + (self.cols * self.cell_size)
        z0 = self.origin.z
        z1 = self.origin.z + (self.rows * self.cell_size)
        y = self.origin.y

        vertices = [
            Vector3(x0, y, z0),
            Vector3(x1, y, z0),
            Vector3(x0, y, z1),
            Vector3(x1, y, z1)
        ]

        return Mesh(vertices, faces=[(0, 1, 2), (1, 3, 2)])
