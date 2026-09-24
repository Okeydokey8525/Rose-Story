import math

class Vector3:
    __slots__ = ['x', 'y', 'z']

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, other: 'Vector3') -> 'Vector3':
        if not isinstance(other, Vector3):
            return NotImplemented
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        if not isinstance(other, Vector3):
            return NotImplemented
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> 'Vector3':
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    # Reverse multiplication (scalar * Vector3)
    def __rmul__(self, scalar: float) -> 'Vector3':
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> 'Vector3':
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide Vector3 by zero")
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector3):
            return NotImplemented
        # Use math.isclose for floating point equality
        return (math.isclose(self.x, other.x, rel_tol=1e-9, abs_tol=1e-9) and
                math.isclose(self.y, other.y, rel_tol=1e-9, abs_tol=1e-9) and
                math.isclose(self.z, other.z, rel_tol=1e-9, abs_tol=1e-9))

    def dot(self, other: 'Vector3') -> float:
        if not isinstance(other, Vector3):
            raise TypeError("Dot product requires another Vector3")
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: 'Vector3') -> 'Vector3':
        if not isinstance(other, Vector3):
            raise TypeError("Cross product requires another Vector3")
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def length(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalized(self) -> 'Vector3':
        l = self.length()
        if l == 0:
            # Handle zero-vector gracefully by returning a new zero-vector
            return Vector3(0, 0, 0)
        return self / l

    def __str__(self) -> str:
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def __repr__(self) -> str:
        return f"Vector3({self.x}, {self.y}, {self.z})"
