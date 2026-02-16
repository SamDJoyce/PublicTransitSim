from typing import Dict, Optional

# ====================== #
# ===== Stop Class ===== #
# ====================== #
class Stop:
    pass

# ======================= #
# ===== Route Class ===== #
# ======================= #
class Route:
    #   =============
    # || Constructor ||
    #   =============
    def __init__(self, route_id: int, segments: Dict[str, Optional[int]]):

        # Check to ensure there are at least 2 stops
        if len(segments) < 2 :
            raise ValueError("Route must have at least 2 stops")
        stops = list(segments.keys())

        # Check to ensure there is a final stop (no travel time)
        if segments[stops[-1]] is not None:
            raise ValueError("Final stop must have travel time = None")

        self.route_id = route_id
        self._segments = segments
        self._stops = stops

    #   =================
    # || Getters/Setters ||
    #   =================

    def stops(self):
        return self._stops

    def number_of_stops(self) -> int:
        return len(self._stops)

    def is_last_stop(self, index: int) -> bool:
        return index == len(self._stops) - 1

    def has_next_stop(self, index: int) -> bool:
        return index < len(self._stops) - 1

    def get_travel_time(self, index: int) -> int:
        """
        Returns the travel time from stop[index]
        to stop[index+1]
        """
        stop_name = self._stops[index]
        travel_time = self._segments[stop_name]

        if travel_time is None:
            raise ValueError("This is the final stop. No travel time")
        return travel_time

    def get_total_route_duration(self):
        duration = 0
        for stop, travel_time in self._segments.items():
            if travel_time is not None:
                duration += travel_time
        return duration

    def get_next_stop(self, index: int) -> str:

        if index < 0 or index >= len(self._stops):
            raise IndexError("Index out of range")

        if self.is_last_stop(index):
            raise ValueError("This is the final stop. No next stop exists.")
        return self._stops[index+1]