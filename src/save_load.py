import json
import os
from garden import Garden
from soil import SoilGrid, SoilState
from rose import Rose, RoseStage

class SaveLoadError(Exception):
    """Raised when there is an error validating or parsing save game data."""
    pass

SAVE_VERSION = 1

def save_game(filepath: str, grid: SoilGrid, roses: list[Rose]):
    """
    Serializes the current logical game state to a JSON file.
    Only preserves:
      - SoilPlot states
      - Rose stages, plot associations, and growth progress
    Does NOT mutate any existing state.
    """
    data = {
        "version": SAVE_VERSION,
        "plots": [],
        "roses": []
    }

    for plot in grid.plots:
        data["plots"].append({
            "index": plot.index,
            "state": plot.state.name
        })

    for rose in roses:
        data["roses"].append({
            "plot_index": rose.plot.index,
            "stage": rose.stage.name,
            "growth_progress": rose.growth_progress
        })

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def load_game(filepath: str, garden: Garden) -> tuple[SoilGrid, list[Rose]]:
    """
    Deserializes a JSON save file and reconstructs the logical game state.
    Requires an active Garden layout to bind the SoilGrid to.
    Returns a new tuple: (SoilGrid, list[Rose])
    """
    if not os.path.exists(filepath):
        raise SaveLoadError(f"Save file not found: {filepath}")

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise SaveLoadError(f"Malformed JSON in save file: {e}")

    # Version check
    if data.get("version") != SAVE_VERSION:
        raise SaveLoadError(f"Unsupported save version: {data.get('version')}")

    # Reconstruct SoilGrid
    new_grid = SoilGrid(garden)

    # We must load plots exactly in index order to avoid silent shifting,
    # or process them by index mapped securely.
    loaded_plots = data.get("plots", [])
    if len(loaded_plots) != len(new_grid.plots):
        raise SaveLoadError("Save file grid dimensions do not match current garden geometry.")

    for p_data in loaded_plots:
        index = p_data.get("index")
        state_name = p_data.get("state")

        try:
            target_plot = new_grid.get_plot_by_index(index)
        except IndexError:
            raise SaveLoadError(f"Invalid plot index in save file: {index}")

        try:
            # Reconstruct authoritative state directly (bypassing strict linear transitions just for loading)
            target_plot.state = SoilState[state_name]
        except KeyError:
            raise SaveLoadError(f"Invalid SoilState in save file: {state_name}")

    # Reconstruct Roses
    new_roses = []
    loaded_roses = data.get("roses", [])
    for r_data in loaded_roses:
        plot_index = r_data.get("plot_index")
        stage_name = r_data.get("stage")
        progress = r_data.get("growth_progress", 0.0)

        try:
            target_plot = new_grid.get_plot_by_index(plot_index)
        except IndexError:
            raise SaveLoadError(f"Invalid plot association index for rose: {plot_index}")

        try:
            stage_enum = RoseStage[stage_name]
        except KeyError:
            raise SaveLoadError(f"Invalid RoseStage in save file: {stage_name}")

        new_rose = Rose(target_plot)
        new_rose.stage = stage_enum
        new_rose.growth_progress = float(progress)
        new_roses.append(new_rose)

    return new_grid, new_roses
