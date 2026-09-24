from enum import Enum, auto
from vector3 import Vector3
from garden import Garden

class SoilState(Enum):
    EMPTY = auto()
    PLANTED_DRY = auto()
    PLANTED_WATERED = auto()
    HARVESTABLE = auto()

class SoilTransitionError(Exception):
    """Raised when an invalid state transition is attempted on a soil plot."""
    pass

class SoilPlot:
    def __init__(self, index: int, position: Vector3):
        self.index = index
        self.position = position
        self.state = SoilState.EMPTY

    def transition_to(self, new_state: SoilState):
        """
        Enforces the linear state transition of the soil:
        Empty -> Planted-Dry -> Planted-Watered -> Harvestable -> (Back to Empty via harvest)
        """
        valid_transitions = {
            SoilState.EMPTY: [SoilState.PLANTED_DRY],
            SoilState.PLANTED_DRY: [SoilState.PLANTED_WATERED],
            SoilState.PLANTED_WATERED: [SoilState.HARVESTABLE],
            SoilState.HARVESTABLE: [SoilState.EMPTY]
        }

        if new_state in valid_transitions[self.state]:
            self.state = new_state
        else:
            raise SoilTransitionError(f"Cannot transition from {self.state.name} to {new_state.name}")

class SoilGrid:
    def __init__(self, garden: Garden):
        self.cols = garden.cols
        self.rows = garden.rows
        self.plots = []

        # Create a plot for each garden cell deterministically
        for i, pos in enumerate(garden.cell_positions):
            self.plots.append(SoilPlot(index=i, position=pos))

    def get_plot_by_index(self, index: int) -> SoilPlot:
        if 0 <= index < len(self.plots):
            return self.plots[index]
        raise IndexError("Plot index out of bounds")

    def get_plot(self, row: int, col: int) -> SoilPlot:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            index = (row * self.cols) + col
            return self.plots[index]
        raise IndexError("Plot coordinates out of bounds")

    def set_plot_state(self, index: int, new_state: SoilState):
        plot = self.get_plot_by_index(index)
        plot.transition_to(new_state)
