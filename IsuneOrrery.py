from IsuneCalendar import Calendar, Year, Month, Day, Hour
import math
from typing_extensions import Self


DEFAULT_PLANE_SIZE = 10


class Orrery:
    pass

    # arcane core is at (0,0,0)
    # reference plane is the (x,y) plane and is defined as the ecliptic plane for all material planes

    # Each plane has a unique biome and terrain, which results in a different climate dedicated to it.
    # There is also a central divide of hemispheres within the axis of material planes.
    # On the northern hemisphere are Veka (air), Aspen (ice), Oshya (water) and Kipra (earth) where Winter starts its cycle in the month Srabuph.
    # In the southern hemisphere are Uthos (rock), Xidor (shadow), Iraz (fire), and Baruta (lighting) where Winter starts in the month Newird.


class Plane:
    # __slots__ = "name"

    def __init__(self, name, amplitude: float, inclination: float, period_in_hours: int, phase: float, color: str, size=DEFAULT_PLANE_SIZE, z_phase=0.0):
        self.name = name
        self.amplitude = amplitude
        self.inclination = inclination  # INCOMPLETE inclination is in the range [0,1]
        self.period_in_hours = period_in_hours
        self.phase = period_in_hours * phase  # phase is given as portion of single orbit and should be in [0, 1]
        self.color = color
        self.size = size
        self.z_phase = period_in_hours * z_phase

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

        xy_theta = (math.tau / self.period_in_hours) * (hours - self.phase)
        # z_theta = (math.tau / self.period_in_hours) * (hours - self.z_phase)


        # sample function for perfectly flat orbit
        x = self.amplitude * math.cos(xy_theta)  # + d  (d term only necessary if not orbiting center)
        y = self.amplitude * math.sin(xy_theta)
        # z = self.amplitude * math.sin(z_theta) * math.cos(self.inclination)
        z = 0.0

        # alternatively:
            # f(t) = a * cos (ω t + ϕ)
            # met ω > 0 de hoekfrequentie,
            # a > 0 de amplitude,
            # ϕ de fase

        return x, y, z
