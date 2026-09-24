from soil import SoilPlot, SoilState, SoilGrid

def water_plot(plot: SoilPlot):
    """
    Programmatic gameplay action to water a specific soil plot.
    Delegates to the existing SoilPlot state transition logic.
    Valid only if plot is PLANTED_DRY.
    Invalid attempts (EMPTY, PLANTED_WATERED, HARVESTABLE) will correctly raise a SoilTransitionError.
    """
    plot.transition_to(SoilState.PLANTED_WATERED)

def water_plot_by_index(grid: SoilGrid, index: int):
    """
    Waters a soil plot retrieved via its index in the SoilGrid.
    """
    plot = grid.get_plot_by_index(index)
    water_plot(plot)

def water_plot_by_coord(grid: SoilGrid, row: int, col: int):
    """
    Waters a soil plot retrieved via its grid coordinates in the SoilGrid.
    """
    plot = grid.get_plot(row, col)
    water_plot(plot)

from rose import Rose, RoseStage

class HarvestEligibilityError(Exception):
    """Raised when attempting to mark a plot harvestable before the rose is in BLOOM."""
    pass

def mark_harvestable(rose: Rose):
    """
    Synchronizes the Rose's visual lifecycle with the underlying SoilPlot state.
    If the Rose has reached BLOOM, the plot transitions to HARVESTABLE.
    """
    if rose.stage != RoseStage.BLOOM:
        raise HarvestEligibilityError(f"Cannot mark harvestable: Rose is only at {rose.stage.name}")

    rose.plot.transition_to(SoilState.HARVESTABLE)

def harvest_plot(plot: SoilPlot):
    """
    Programmatic gameplay action to harvest a specific soil plot.
    Delegates to the existing SoilPlot state transition logic.
    Valid only if plot is HARVESTABLE. Transitions to EMPTY.
    """
    plot.transition_to(SoilState.EMPTY)
