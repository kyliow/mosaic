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
        self._create_zones(grid_data=grid_data, simulation_input=simulation_input)
        self._create_stations(grid_data=grid_data, simulation_input=simulation_input)

    def _create_zones(
        self, grid_data: pandas.DataFrame, simulation_input: SimulationInputUI
    ):

        # Find all void locations (values 1 or 3)
        void_mask = grid_data.isin([1, 3]).to_numpy()
        rows, cols = void_mask.shape
        voids = []

        # Use boolean array to track processed cells
        processed = numpy.zeros_like(void_mask, dtype=bool)

        # Scan unprocessed void cells
        void_positions = numpy.argwhere(numpy.logical_and(void_mask, ~processed))

        for start_y, start_x in void_positions:
            if processed[start_y, start_x]:
                continue

            # Expand right
            end_x = start_x
            while end_x + 1 < cols and void_mask[start_y, end_x + 1]:
                end_x += 1

            # Expand down
            end_y = start_y
            while end_y + 1 < rows:
                is_valid = True
                for x in range(start_x, end_x + 1):
                    if not void_mask[end_y + 1, x]:
                        is_valid = False
                        break
                if not is_valid:
                    break
                end_y += 1

            # Mark as processed
            processed[start_y : end_y + 1, start_x : end_x + 1] = True

            void = InputVoid(
                from_=Coordinates(x=int(start_x), y=int(start_y), z=0),
                to=Coordinates(x=int(end_x), y=int(end_y), z=simulation_input.z_size),
            )
            voids.append(void)

        zone = InputZone(
            max_x=grid_data.shape[1] - 1,
            max_y=grid_data.shape[0] - 1,
            max_z=simulation_input.z_size,
            voids=voids,
        )
        self.zones = [zone]

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

    def to_json(self, save: bool = False, filename: str = "reset-2.json") -> str:
        json_str = json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=True, indent=4
        )

        if save:
            with open(filename, "w") as file:
                file.write(json_str)

        return json_str


class InputZone:
    def __init__(
        self,
        max_x: int,
        max_y: int,
        max_z: int,
        voids: List[InputVoid],
        name: str = "C",
    ):
        self.name = name
        self.fromX = 0
        self.toX = max_x
        self.fromY = 0
        self.toY = max_y
        self.fromZ = 0
        self.toZ = max_z
        self.voids = voids


class InputVoid:
    def __init__(self, from_: Coordinates, to: Coordinates):
        self.from_ = from_
        self.to = to


class InputStation:
    def __init__(self, code: int, drop: InputDropOrPick, pick: InputDropOrPick):
        self.code = code
        self.drop = [drop]
        self.pick = [pick]


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


class Coordinates:

    def __init__(self, x: int, y: int, z: int = 0):
        self.x = x
        self.y = y
        self.z = z
