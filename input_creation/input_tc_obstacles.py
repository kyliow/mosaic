import pandas
import json


class InputTCObstacles:
    def __init__(self, grid_data: pandas.DataFrame):
        self.type = "Pillar"
        self.skycar_sid = 0
        self.error_id = 0

        self.two_d = self._find_tc_obstacles(grid_data=grid_data)

    def _find_tc_obstacles(self, grid_data: pandas.DataFrame) -> list[str]:
        # Find all void locations (values 2 or 3)
        void_mask = grid_data.isin([2, 3]).to_numpy()
        rows, cols = void_mask.shape
        return [f"{x},{y}" for x in range(rows) for y in range(cols) if void_mask[x, y]]

    def to_json(self, save: bool = False, filename: str = "reset-6.json") -> str:
        json_str = json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=True, indent=4
        )

        if save:
            with open(filename, "w") as file:
                file.write(json_str)

        return json_str
