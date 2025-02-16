import json

import numpy
import pandas

from parameters import Parameters
class InputSMObstacles:
    def __init__(self, grid_data: pandas.DataFrame):
        self._create_stacks(grid_data=grid_data)
        self.zoneGroup = Parameters.ZONE_NAME
        self.isSkycarAccessible = False

    def _create_stacks(self, grid_data: pandas.DataFrame):
        void_mask = grid_data.isin([1, 3]).to_numpy()

        # Get coordinates where void_mask is True
        coordinates = numpy.argwhere(void_mask)
        
        # Create InputStack objects for each coordinate
        self.stacks = [
            InputStack(x=int(col), y=int(row)) 
            for row, col in coordinates
        ]

    def to_json(self, save: bool = False, filename: str = "reset-3.json") -> str:
        json_str = json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=True, indent=4
        )

        if save:
            with open(filename, "w") as file:
                file.write(json_str)

        return json_str

class InputStack:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
