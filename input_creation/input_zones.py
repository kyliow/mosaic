from __future__ import annotations

import json
from typing import List

import numpy
import pandas

from ui.simulation_input import SimulationInputUI


class InputZonesAndStations:
    def __init__(
        self, grid_data: pandas.DataFrame, simulation_input: SimulationInputUI
    ):
        self._create_stations(grid_data=grid_data, simulation_input=simulation_input)

    def _create_zones(self, grid_data: pandas.DataFrame):
        pass

    def _create_stations(
        self, grid_data: pandas.DataFrame, simulation_input: SimulationInputUI
    ):
        # Usually the height of station is 2 bins above ground
        station_height = simulation_input.z_size - 2

        uncleaned_stations = numpy.sort(
            grid_data.copy()[grid_data >= 10].stack().values
        )

        grid_data_array = grid_data.to_numpy()

        count = 1
        stations: List[InputStation] = []
        for station_value in uncleaned_stations:
            y, x = numpy.argwhere(grid_data_array == station_value)[0].tolist()
            if station_value % 10 == 0:
                drop = InputDropOrPick(
                    coordinates=Coordinates(x=x, y=y, z=station_height),
                    capacity=simulation_input.drop_capacity,
                )
                pick = InputDropOrPick(
                    coordinates=Coordinates(x=x, y=y, z=station_height),
                    capacity=simulation_input.pick_capacity,
                )
                station = InputStation(code=count, drop=drop, pick=pick)
                stations.append(station)
                count += 1
            else:
                if station_value % 10 == 1:
                    drop = InputDropOrPick(
                        coordinates=Coordinates(x=x, y=y, z=station_height),
                        capacity=simulation_input.drop_capacity,
                    )
                else:
                    pick = InputDropOrPick(
                        coordinates=Coordinates(x=x, y=y, z=station_height),
                        capacity=simulation_input.pick_capacity,
                    )
                    station = InputStation(code=count, drop=drop, pick=pick)
                    stations.append(station)
                    count += 1

        self.stations = stations

    def to_json(self, save: bool = False, filename: str = "reset-5.json") -> str:
        json_str = json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=True, indent=4
        )

        if save:
            with open(filename, "w") as file:
                file.write(json_str)

        return json_str


class InputStation:
    def __init__(self, code: int, drop: InputDropOrPick, pick: InputDropOrPick):
        self.code = code
        self.drop = [drop]
        self.pick = [pick]

    # def to_json(self) -> str:
    #     json_str = json.dumps(
    #         self, default=lambda o: o.__dict__, sort_keys=True, indent=4
    #     )
    #     return json_str


class InputDropOrPick:
    # FIXME: What should be the value of capacity, hardware index, and zone group?
    def __init__(
        self,
        coordinates: Coordinates,
        capacity: int = 1,
        hardware_index: int = 1,
        zone_group: str = "C",
    ):
        self.capacity = capacity
        self.hardwareIndex = hardware_index
        self.zoneGroup = zone_group
        self.coordinate = coordinates

    # def copy(self) -> InputDropOrPick:
    #     return InputDropOrPick(
    #         capacity=self.capacity,
    #         hardware_index=self.hardwareIndex,
    #         zone_group=self.zoneGroup,
    #         coordinates=self.coordinate.copy(),
    #     )

    # def to_json(self) -> str:
    #     json_str = json.dumps(
    #         self, default=lambda o: o.__dict__, sort_keys=True, indent=4
    #     )
    #     return json_str


class Coordinates:

    def __init__(self, x: int, y: int, z: int = 0):
        self.x = x
        self.y = y
        self.z = z

    # def copy(self) -> Coordinates:
    #     return Coordinates(x=self.x, y=self.y, z=self.z)

    # def to_json(self) -> str:
    #     json_str = json.dumps(
    #         self, default=lambda o: o.__dict__, sort_keys=True, indent=4
    #     )
    #     return json_str
