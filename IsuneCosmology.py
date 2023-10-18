from IsuneOrrery import Plane, ExtrusionPlane, AsteroidBeltPlane, Orbit, Orrery

INNER_PLANES_AMPLITUDE = 10
OUTER_PLANES_AMPLITUDE = 30
OUTER_PLANES_INCLINATION = 0.4
PERIOD_IN_HOURS_MATERIAL_PLANES = 24 * 8  # material plane axis: 8 days
PERIOD_IN_HOURS_OTHER_INNER_PLANES = 24 * 16  # fey-shadowfell and ethereal planes: 16 days
PERIOD_IN_HOURS_OUTER_PLANES = 24 * 32  # outer planes: 32 days

OUTER_PLANES_COLOR = "#aaaaaa"
OUTER_PLANES_SIZE = 15

MATERIAL_PLANES_ORBIT = Orbit(rotational_axis=[0.0, 0.0, 1.0], amplitude=INNER_PLANES_AMPLITUDE)  # ecliptical plane
FEYFELL_ORBIT = Orbit(rotational_axis=[1.0, 0.0, 0.90], amplitude=INNER_PLANES_AMPLITUDE)
ETHEREAL_PLANE_ORBIT = Orbit(rotational_axis=[-1.0, 0.0, 1.10], amplitude=INNER_PLANES_AMPLITUDE)
OUTER_PLANES_ORBIT = Orbit(rotational_axis=[1.0, 1.0, 1.10], amplitude=OUTER_PLANES_AMPLITUDE)

# Offset in phase used to define the position of planes at the starting date of the calendar
GLOBAL_HOURS_OFFSET = -60

# arcane core is at (0,0,0)
# reference plane is the (x,y) plane and is defined as the ecliptic plane for all material planes

# Each plane has a unique biome and terrain, which results in a different climate dedicated to it.
# There is also a central divide of hemispheres within the axis of material planes.
# On the northern hemisphere are Veka (air), Aspen (ice), Oshya (water) and Kipra (earth) where Winter starts its cycle in the month Srabuph.
# In the southern hemisphere are Uthos (rock), Xidor (shadow), Iraz (fire), and Baruta (lighting) where Winter starts in the month Newird.


def get_material_planes() -> list[Plane]:

    veka   = Plane("Veka",   orbit=MATERIAL_PLANES_ORBIT, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=0 / 8, color="#54d3ab", size=20)
    aspen  = Plane("Aspen",  orbit=MATERIAL_PLANES_ORBIT, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=1 / 8, color="#41acc1", size=8)
    oshya  = Plane("Oshya",  orbit=MATERIAL_PLANES_ORBIT, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=2 / 8, color="#4175c1", size=11)
    kipra  = Plane("Kipra",  orbit=MATERIAL_PLANES_ORBIT, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=3 / 8, color="#79c141", size=18)
    uthos  = Plane("Uthos",  orbit=MATERIAL_PLANES_ORBIT, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=4 / 8, color="#e8ac22", size=9)
    xidor  = Plane("Xidor",  orbit=MATERIAL_PLANES_ORBIT, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=5 / 8, color="#888888", size=9)
    iraz   = Plane("Iraz",   orbit=MATERIAL_PLANES_ORBIT, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=6 / 8, color="#ee0022", size=17)
    baruta = Plane("Baruta", orbit=MATERIAL_PLANES_ORBIT, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=7 / 8, color="#8c06ad", size=7)
    material_planes = [veka, aspen, oshya, kipra, uthos, xidor, iraz, baruta]

    return material_planes


def get_outer_planes() -> list[Plane]:

    mount_delestia = Plane("Mount Delestia", orbit=OUTER_PLANES_ORBIT, period_in_hours=PERIOD_IN_HOURS_OUTER_PLANES, phase=2/8, color=OUTER_PLANES_COLOR, size=OUTER_PLANES_SIZE)
    elysium        = Plane("Elysium",        orbit=OUTER_PLANES_ORBIT, period_in_hours=PERIOD_IN_HOURS_OUTER_PLANES, phase=3/8, color=OUTER_PLANES_COLOR, size=OUTER_PLANES_SIZE)
    the_beastlands = Plane("The Beastlands", orbit=OUTER_PLANES_ORBIT, period_in_hours=PERIOD_IN_HOURS_OUTER_PLANES, phase=4/8, color=OUTER_PLANES_COLOR, size=OUTER_PLANES_SIZE)
    limbo          = Plane("Limbo",          orbit=OUTER_PLANES_ORBIT, period_in_hours=PERIOD_IN_HOURS_OUTER_PLANES, phase=5/8, color=OUTER_PLANES_COLOR, size=OUTER_PLANES_SIZE)
    the_abyss      = Plane("The Abyss",      orbit=OUTER_PLANES_ORBIT, period_in_hours=PERIOD_IN_HOURS_OUTER_PLANES, phase=6/8, color=OUTER_PLANES_COLOR, size=OUTER_PLANES_SIZE)
    the_nine_hells = Plane("The Nine Hells", orbit=OUTER_PLANES_ORBIT, period_in_hours=PERIOD_IN_HOURS_OUTER_PLANES, phase=7/8, color=OUTER_PLANES_COLOR, size=OUTER_PLANES_SIZE)
    outer_planes = [mount_delestia, elysium, the_beastlands, limbo, the_abyss, the_nine_hells]

    return outer_planes


def get_feyfell_planes() -> list[Plane]:

    feywild    = ExtrusionPlane("Feywild",    orbit=FEYFELL_ORBIT, period_in_hours=PERIOD_IN_HOURS_OTHER_INNER_PLANES, phase=0.0, color="#dba1e0", size=20, extrusion=0.48)
    shadowfell = ExtrusionPlane("Shadowfell", orbit=FEYFELL_ORBIT, period_in_hours=PERIOD_IN_HOURS_OTHER_INNER_PLANES, phase=0.5, color="#7f7f7f", size=20, extrusion=0.48)
    feyfell = [feywild, shadowfell]

    return feyfell


def get_ethereal_plane() -> AsteroidBeltPlane:
    ethereal_plane = AsteroidBeltPlane("Ethereal Plane", ETHEREAL_PLANE_ORBIT, PERIOD_IN_HOURS_OTHER_INNER_PLANES, 0.0, "#ffffff", 5, 1.0, 250, 0.7)
    return ethereal_plane


def apply_initial_phase_offset(planes: list, offset_hours: int):
    planes_flattened = []

    for p in planes:
        if type(p) is list:
            planes_flattened.extend(p)
        else:
            planes_flattened.append(p)

    for p in planes_flattened:
        p.phase -= offset_hours / p.period_in_hours

def get_isune_cosmology():

    arcane_core = Plane("Arcane Core", orbit=None, period_in_hours=1, phase=0.0, color="#ffff99", size=25)
    material_planes = get_material_planes()
    feyfell_planes = get_feyfell_planes()
    ethereal_plane = get_ethereal_plane()
    outer_planes = get_outer_planes()

    planes = [arcane_core, material_planes, feyfell_planes, [ethereal_plane], outer_planes]

    apply_initial_phase_offset(planes, GLOBAL_HOURS_OFFSET)

    return Orrery(*planes)
