from IsuneCalendar import Calendar, Year, Month, Day, Hour
import math
import numpy as np

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

    def __init__(self, name, orbit: 'Orbit', period_in_hours: int, phase: float, color: str, size=DEFAULT_PLANE_SIZE):
        self.name = name
        self.orbit = orbit
        self.period_in_hours = period_in_hours
        self.phase = period_in_hours * phase  # phase is given as portion of single orbit and should be in [0, 1]
        self.color = color
        self.size = size


    def location_at_date(self, date: Calendar) -> tuple[float, float, float]:
        return self.location_from_hours(date.total_hours())

    def x_from_hours(self, hours: int) -> float:
        return self.location_from_hours(hours)[0]

    def y_from_hours(self, hours: int) -> float:
        return self.location_from_hours(hours)[1]

    def z_from_hours(self, hours: int) -> float:
        return self.location_from_hours(hours)[2]

    def distance_from_other_plane(self, other: 'Plane', date: Calendar):
        loc_self = self.location_at_date(date)
        loc_other = other.location_at_date(date)
        return math.dist(loc_self, loc_other)

    def location_from_hours_old(self, hours: int) -> tuple[float, float, float]:
        """input in uren"""

        phi = (math.tau / self.period_in_hours) * (hours - self.phase)  # phi is in the xy-plane, and theta in the xz-plane. This follows the common notation in physics
        # theta = (math.tau / self.period_in_hours) * (hours - self.z_phase)


        # sample function for perfectly flat orbit
        x = self.amplitude * math.cos(phi)
        y = self.amplitude * math.sin(phi)
        # z = self.amplitude * math.sin(theta) * math.cos(self.inclination)
        z = 0.0

        # alternatively:
            # f(t) = a * cos (ω t + ϕ)
            # met ω > 0 de hoekfrequentie,
            # a > 0 de amplitude,
            # ϕ de fase

        return x, y, z


    def location_from_hours(self, hours: int) -> tuple[float, float, float]:

        theta = (math.tau / self.period_in_hours) * (hours - self.phase)
        return self.orbit.location_from_hours(theta)


class Orbit:

    def __init__(self, rotational_axis: list[float, float, float], amplitude: float, eccentricity=1.0, center=[0, 0, 0]):

        self.rotational_axis = rotational_axis / np.linalg.norm(rotational_axis)
        self.amplitude = amplitude
        self.eccentricity = eccentricity
        self.center = np.asarray(center)

        self._orthogonal_axis_a, self._orthogonal_axis_b = self._create_orbit_vectors(self.rotational_axis)

    def _create_orbit_vectors(self, rotational_axis_vector: np.ndarray):

        # Gram-Schmidt procedure to generate orthogonal vectors (see https://stackoverflow.com/questions/33658620/generating-two-orthogonal-vectors-that-are-orthogonal-to-a-particular-direction)
        a = np.random.randn(3)
        a -= a.dot(rotational_axis_vector) * rotational_axis_vector
        a = a / np.linalg.norm(a)

        b = np.cross(rotational_axis_vector, a)
        b = b / np.linalg.norm(b)

        return a, b

    def location_from_hours(self, theta):
        a = self._orthogonal_axis_a
        b = self._orthogonal_axis_b

        c = self.eccentricity
        d = 1 / c

        x = self.amplitude/c * math.cos(theta) * a[0] + self.amplitude/d * math.sin(theta) * b[0]
        y = self.amplitude/c * math.cos(theta) * a[1] + self.amplitude/d * math.sin(theta) * b[1]
        z = self.amplitude/c * math.cos(theta) * a[2] + self.amplitude/d * math.sin(theta) * b[2]

        return x, y, z
