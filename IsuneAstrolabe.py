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
    __slots__ = "name"

    def __init__(self, name):
        self.name = name

    def location_at_date(self, date: Calendar) -> tuple[float, float, float]:
        return self.location_from_hours(date.total_hours())

    def x_from_hours(self, hours: int) -> float:
        amplitude = 10
        period = 24
        c = 0
        d = 0
        x = amplitude * math.cos((math.tau / period) * (hours - c)) + d
        return x

    def y_from_hours(self, hours: int) -> float:
        amplitude = 10
        period = 24
        c = 0
        d = 0
        y = amplitude * math.sin((math.tau / period) * (hours - c)) + d
        return y

    def z_from_hours(self, hours: int) -> float:
        return 0.0

    def distance_from(self, other: Self, date: Calendar):
        loc_self = self.location_at_date(date)
        loc_other = other.location_at_date(date)
        return math.dist(loc_self, loc_other)



    def location_from_hours(self, hours: int) -> tuple[float, float, float]:
        """input in uren"""

        amplitude = 10
        period = 24
        c = 0
        d = 0

        # sample function for perfectly flat orbit
        z = 0
        x = amplitude * math.cos((math.tau / period) * (hours - c)) + d
        y = amplitude * math.sin((math.tau / period) * (hours - c)) + d

        # f(x) = a * sin( b * (x - c)) + d
        # a = amplitude
        # b = 2pi/periode
        # c = offset
        # d = equilibrium
        # (c,d) = starting point

        # alternatively:
            # De algemene vorm van een sinusoïdale functie van tijd is:   f(t) = a * cos (ω t + ϕ)
            # met ω > 0 de hoekfrequentie,
            # a > 0 de amplitude,
            # ϕ de fase

        return x, y, z
