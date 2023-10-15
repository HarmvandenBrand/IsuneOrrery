import random
from typing import Optional

import pandas as pd

from IsuneCalendar import Calendar, Year, Month, Day, Hour
import math
import numpy as np


class Orrery:

    def __init__(self, sun: 'Plane', material_planes: list['Plane'], extrusion_planes: list['ExtrusionPlane'], asteroid_planes: list['AsteroidBeltPlane'], outer_planes: list['Plane']):
        self.sun_plane = sun
        self.material_planes = material_planes
        self.extrusion_planes = extrusion_planes
        self.asteroid_planes = asteroid_planes
        self.outer_planes = outer_planes

        self.calendar = Calendar(0, 1, 1, 0)
        self._vilron = Plane("Vil'ron", orbit=None, period_in_hours=10, phase=0.0, color="#bbbbee", size=45)


    def get_locations_as_dataframe_dict(self) -> dict:

        if self.calendar < Calendar(0, 1, 1, 0):
            # Before the zero date display only Vil'ron
            return {"simple planes": {self._vilron.name: self._simple_planes_to_df([self._vilron])}}
        else:
            sun_plane_df = self._simple_planes_to_df([self.sun_plane])
            material_planes_df = self._simple_planes_to_df(self.material_planes)
            feywild_df, shadowfell_df = self._extrusion_planes_to_dfs(self.extrusion_planes)
            ethereal_plane_df = self._asteroid_belt_planes_to_dfs(self.asteroid_planes)[0]
            outer_planes_df = self._simple_planes_to_df(self.outer_planes)

            dfs_dict = {"simple planes": {self.sun_plane.name: sun_plane_df, "Material Planes": material_planes_df, "Outer Planes": outer_planes_df},
                        "extrusion planes": {"Feywild": feywild_df, "Shadowfell": shadowfell_df},
                        "asteroid planes": {"Ethereal Plane": ethereal_plane_df}}

            return dfs_dict

    def _simple_planes_to_df(self, planes: list['Plane']) -> pd.DataFrame:
        """Orders calculation of the current state of the orrery and creates a dataframe from that data.
        This function assumes the calendar date has already been correctly set."""

        locations = [[*plane.location_from_hours(self.calendar.total_hours())] for plane in planes]
        location_dict = {'x': [v[0] for v in locations], 'y': [v[1] for v in locations], 'z': [v[2] for v in locations]}
        df = pd.DataFrame(location_dict)
        df['color'] = [plane.color if plane.color is not None else '#dddddd' for plane in planes]
        df['name'] = [plane.name if plane.name is not None else 'None' for plane in planes]
        df['size'] = [int(plane.size) for plane in planes]

        return df

    def _extrusion_planes_to_dfs(self, planes: list['ExtrusionPlane']) -> list[pd.DataFrame]:
        dfs = []

        for plane in planes:
            locations = [*plane.locations_extrusion_from_hours(self.calendar.total_hours(), n_slice=50)]
            location_dict = {'x': [v[0] for v in locations], 'y': [v[1] for v in locations], 'z': [v[2] for v in locations]}

            df = pd.DataFrame(location_dict)
            df['color'] = plane.color if plane.color is not None else '#dddddd'
            df['name'] = plane.name if plane.name is not None else 'None'
            df['size'] = int(plane.size)
            dfs.append(df)

        return dfs

    def _asteroid_belt_planes_to_dfs(self, planes: list['AsteroidBeltPlane']) -> list[pd.DataFrame]:
        dfs = []

        for plane in planes:
            locations, deltas = plane.locations_belt_from_hours(self.calendar.total_hours())

            # hack for fixing the size of cone plots in plotly
            epsilon = 0.000001
            v_last = [v + epsilon for v in locations[-1]]
            locations.append(v_last)
            deltas.append(deltas[-1])

            asteroid_dict = {'x': [v[0] for v in locations], 'y': [v[1] for v in locations], 'z': [v[2] for v in locations],
                             'u': [d[0] for d in deltas], 'v': [d[1] for d in deltas], 'w': [d[0] for d in deltas]}

            df = pd.DataFrame(asteroid_dict)
            df['color'] = plane.color if plane.color is not None else '#dddddd'
            df['name'] = plane.name if plane.name is not None else 'None'
            dfs.append(df)

        return dfs


class Plane:
    """Represents a simple planet-like plane. Also functions as base class for all other planes."""

    # __slots__ = "name"

    def __init__(self, name, orbit: Optional['Orbit'], period_in_hours: int, phase: float, color: str, size: int):
        self.name = name
        self.orbit = orbit if orbit is not None else Orbit.NULL_ORBIT
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

    def _theta(self, hours: int | float) -> float:
        return (math.tau / self.period_in_hours) * (hours - self.phase)

    def location_from_hours(self, hours: int) -> tuple[float, float, float]:
        """Return the location of the plane for the given time"""
        return self.orbit.location_from_hours(self._theta(hours))

    def __str__(self):
        return self.name


class ExtrusionPlane(Plane):
    """Planes that cover an extended stretch of space along their orbit. Typical examples are the feywild and shadowfell planes."""

    def __init__(self, name, orbit: Optional['Orbit'], period_in_hours: int, phase: float, color: str, size: int, extrusion: float):
        super().__init__(name, orbit, period_in_hours, phase, color, size)
        self.extrusion_percentage = extrusion

    def locations_extrusion_from_hours(self, hours: int, n_slice: int) -> tuple[tuple[float, float, float]]:
        """Return a list of n_slice locations for this plane.
        The locations are within [-extrusion_percentage/2, extrusion_percentage/2], marked from the given time."""
        hours_start = hours - self.period_in_hours * (self.extrusion_percentage/2)
        hours_end = hours + self.period_in_hours * (self.extrusion_percentage/2)
        slice_hours = np.linspace(hours_start, hours_end, n_slice)

        locations_slice = tuple(self.location_from_hours(hour) for hour in slice_hours)
        return locations_slice


class AsteroidBeltPlane(ExtrusionPlane):

    def __init__(self, name, orbit: Optional['Orbit'], period_in_hours: int, phase: float, color: str, size: int, extrusion: float, n: int, sigma=2):
        super().__init__(name, orbit, period_in_hours, phase, color, size, extrusion)

        self.N = n
        self.sigma = sigma

        # Disable inappropriate parent methods
        self.location_from_hours = None
        self.location_extrusion_from_hours = None

    def locations_belt_from_hours(self, hours: int):
        """Generates a number of random points and corresponding tangent vectors along the extrusion curve.
        The locations are within [-extrusion_percentage/2, extrusion_percentage/2], marked from the given time.
        The randomness and number of generated point,tangent pairs are determined by instance fields."""

        hours_start = hours - self.period_in_hours * (self.extrusion_percentage/2)
        hours_end = hours + self.period_in_hours * (self.extrusion_percentage/2)

        vertices = []
        deltas = []

        for _ in range(self.N):
            # Generate random location within extrusion space
            hour = random.random() * (hours_end - hours_start) + hours_start
            loc1 = self.orbit.location_from_hours(self._theta(hour))

            # Generate delta's, a.k.a. direction vectors
            loc2 = self.orbit.location_from_hours((self._theta(hour+0.01)))
            delta = [loc2[0]-loc1[0], loc2[1]-loc1[1], loc2[2]-loc1[2]]
            delta = delta / np.linalg.norm(delta)  # normalization is important for fixing sizing of cones in plotly

            # add randomnness
            loc1 = [loc + random.gauss(0.0, self.sigma) for loc in loc1]

            vertices.append(loc1)
            deltas.append(delta)

        return vertices, deltas


class Orbit:

    def __init__(self, rotational_axis: list[float, float, float], amplitude: float, eccentricity=1.0, center=(0, 0, 0)):

        self.rotational_axis = rotational_axis / np.linalg.norm(rotational_axis)
        self.amplitude = amplitude
        self.eccentricity = eccentricity
        self.center = np.asarray(center)

        self._orthogonal_axis_a, self._orthogonal_axis_b = self._create_orbit_vectors(self.rotational_axis)

    def _create_orbit_vectors(self, rotational_axis_vector: np.ndarray):
        """Create orbit vectors a and b that are perpendicular to the rotational_axis using the Rodrigues rotation formula.
        The orbit vectors are used to calculate the location of a plane in 3D-space in other methods."""

        # Construct the xyz unit vectors in R3
        V = np.asarray([(1, 0, 0), (0, 1, 0), (0, 0, 1)], dtype=float)

        # Interpret the rotational axis as a rotated z-axis of the unit vectors. Calculate cross-product k between the two.
        r = rotational_axis_vector / np.linalg.norm(rotational_axis_vector)

        # if r == (0,0,1), k will be (0,0,0). Normalizing k then results in NaNs. Return unchanged unit vectors instead.
        if np.array_equal(r, np.asarray((0, 0, 1), dtype=float)):
            return V[0], V[1]

        k = np.cross(V[2], r)
        k /= np.linalg.norm(k)

        # Calculate angle theta between the z-unit vector and the rotational axis.
        theta = np.arccos(np.dot(V[2], r) / (np.linalg.norm(V[2]) * np.linalg.norm(r)))

        # Use Rodrigues' rotation formula to calculate the rotated vector for every one of the unit vectors
        for i, v in enumerate(V):
            V[i] = v * np.cos(theta) + np.cross(k, v) * np.sin(theta) + k * np.dot(k, v) * (1 - np.cos(theta))
            V[i] /= np.linalg.norm(V[i])

        return V[0], V[1]

    def _create_orbit_vectors_gramschmidt(self, rotational_axis_vector: np.ndarray):
        """Deprecated, use _create_orbit_vectors instead. Gram-Schmidt procedure to generate orthogonal vectors
        (see https://stackoverflow.com/questions/33658620/generating-two-orthogonal-vectors-that-are-orthogonal-to-a-particular-direction)"""
        a = np.random.randn(3)
        a -= a.dot(rotational_axis_vector) * rotational_axis_vector
        a = a / np.linalg.norm(a)

        b = np.cross(rotational_axis_vector, a)
        b = b / np.linalg.norm(b)

        return a, b

    def location_from_hours(self, theta: float):
        # https://math.stackexchange.com/questions/73237/parametric-equation-of-a-circle-in-3d-space
        a = self._orthogonal_axis_a
        b = self._orthogonal_axis_b

        c = self.eccentricity
        d = 1 / c

        x = self.amplitude/c * math.cos(theta) * a[0] + self.amplitude/d * math.sin(theta) * b[0]
        y = self.amplitude/c * math.cos(theta) * a[1] + self.amplitude/d * math.sin(theta) * b[1]
        z = self.amplitude/c * math.cos(theta) * a[2] + self.amplitude/d * math.sin(theta) * b[2]

        return x, y, z


Orbit.NULL_ORBIT = Orbit(rotational_axis=[0.0, 0.0, 1.0], amplitude=0.0)
