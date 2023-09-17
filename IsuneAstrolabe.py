from IsuneCalendar import Calendar, Year, Month, Day, Hour
import math
from typing_extensions import Self



class Astrolabe:
    pass

    # arcane core is at (0,0,0)

    # Each plane has a unique biome and terrain, which results in a different climate dedicated to it.
    # There is also a central divide of hemispheres within the axis of material planes.
    # On the northern hemisphere are Veka (air), Aspen (ice), Oshya (water) and Kipra (earth) where Winter starts its cycle in the month Srabuph.
    # In the southern hemisphere are Uthos (rock), Xidor (shadow), Iraz (fire), and Baruta (lighting) where Winter starts in the month Newird.


class Plane:
    # __slots__ = "name"

    def __init__(self, name, amplitude: float, period_in_hours: int, phase: float, color: str):
        self.name = name
        self.amplitude = amplitude
        self.period_in_hours = period_in_hours
        self.phase = period_in_hours * phase  # phase is given as portion of single orbit and should be in [0, 1]
        self.color = color

    def location_at_date(self, date: Calendar) -> tuple[float, float, float]:
        return self.location_from_hours(date.total_hours())

    def x_from_hours(self, hours: int) -> float:
        return self.location_from_hours(hours)[0]

    def y_from_hours(self, hours: int) -> float:
        return self.location_from_hours(hours)[1]

    def z_from_hours(self, hours: int) -> float:
        return self.location_from_hours(hours)[2]

    def distance_from_other_plane(self, other: Self, date: Calendar):
        loc_self = self.location_at_date(date)
        loc_other = other.location_at_date(date)
        return math.dist(loc_self, loc_other)

    def location_from_hours(self, hours: int) -> tuple[float, float, float]:
        """input in uren"""

        # sample function for perfectly flat orbit
        z = 0.0
        x = self.amplitude * math.cos((math.tau / self.period_in_hours) * (hours - self.phase))  # + d  (d term only necessary if not orbiting center)
        y = self.amplitude * math.sin((math.tau / self.period_in_hours) * (hours - self.phase))

        # alternatively:
            # f(t) = a * cos (ω t + ϕ)
            # met ω > 0 de hoekfrequentie,
            # a > 0 de amplitude,
            # ϕ de fase

        return x, y, z
