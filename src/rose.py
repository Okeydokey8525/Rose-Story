from enum import Enum, auto
from soil import SoilPlot

class RoseStage(Enum):
    SEED = auto()
    SPROUT = auto()
    YOUNG_PLANT = auto()
    BUD = auto()
    BLOOM = auto()

class RoseTransitionError(Exception):
    """Raised when an invalid growth stage transition is attempted on a Rose."""
    pass

from soil import SoilState

# Simple deterministic placeholder values for development.
# Each stage requires exactly 10.0 units of elapsed time to progress.
STAGE_DURATION = 10.0

class Rose:
    def __init__(self, plot: SoilPlot):
        """
        Initializes a new Rose associated with a specific SoilPlot.
        The initial growth stage is always SEED.
        """
        self.plot = plot
        self.position = plot.position
        self.stage = RoseStage.SEED
        self.growth_progress = 0.0

    def update(self, delta_time: float):
        """
        Advances the Rose's growth deterministically based on explicit elapsed time.
        Growth only occurs if the associated SoilPlot is PLANTED_WATERED.
        """
        if self.plot.state != SoilState.PLANTED_WATERED:
            return

        if self.stage == RoseStage.BLOOM:
            return

        self.growth_progress += delta_time

        # Process thresholds sequentially, preserving remaining elapsed time
        while self.growth_progress >= STAGE_DURATION and self.stage != RoseStage.BLOOM:
            self.grow()
            self.growth_progress -= STAGE_DURATION

            if self.stage == RoseStage.BLOOM:
                self.growth_progress = 0.0
                break

    def grow(self):
        """
        Advances the Rose strictly to the next sequential visual growth stage.
        Raises RoseTransitionError if attempting to grow past BLOOM.
        """
        valid_transitions = {
            RoseStage.SEED: RoseStage.SPROUT,
            RoseStage.SPROUT: RoseStage.YOUNG_PLANT,
            RoseStage.YOUNG_PLANT: RoseStage.BUD,
            RoseStage.BUD: RoseStage.BLOOM
        }

        if self.stage in valid_transitions:
            self.stage = valid_transitions[self.stage]
        else:
            raise RoseTransitionError(f"Cannot grow past {self.stage.name}")
