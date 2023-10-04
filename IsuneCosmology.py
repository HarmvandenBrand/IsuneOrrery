from IsuneOrrery import Plane, Orbit



INNER_PLANES_AMPLITUDE = 10
OUTER_PLANES_AMPLITUDE = 30
OUTER_PLANES_INCLINATION = 0.4
PERIOD_IN_HOURS_MATERIAL_PLANES = 24 * 8  # material plane axis: 8 days
PERIOD_IN_HOURS_OTHER_INNER_PLANES = 24 * 16  # fey-shadowfell and ethereal planes: 16 days
PERIOD_IN_HOURS_OUTER_PLANES = 24 * 32  # outer planes: 32 days

OUTER_PLANES_COLOR = "#aaaaaa"
OUTER_PLANES_SIZE = 15


def get_material_planes() -> list[Plane]:
    material_planes_orbit = Orbit(rotational_axis=[0.0, 0.0, 1.0], amplitude=INNER_PLANES_AMPLITUDE)  # ecliptical plane

    veka   = Plane("Veka",   orbit=material_planes_orbit, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=0/8, color="#54d3ab", size=20)
    aspen  = Plane("Aspen",  orbit=material_planes_orbit, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=1/8, color="#41acc1", size=8)
    oshya  = Plane("Oshya",  orbit=material_planes_orbit, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=2/8, color="#4175c1", size=11)
    kipra  = Plane("Kipra",  orbit=material_planes_orbit, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=3/8, color="#79c141", size=18)
    uthos  = Plane("Uthos",  orbit=material_planes_orbit, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=4/8, color="#e8ac22", size=9)
    xidor  = Plane("Xidor",  orbit=material_planes_orbit, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=5/8, color="#888888", size=9)
    iraz   = Plane("Iraz",   orbit=material_planes_orbit, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=6/8, color="#ee0022", size=17)
    baruta = Plane("Baruta", orbit=material_planes_orbit, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=7/8, color="#8c06ad", size=7)
    material_planes = [veka, aspen, oshya, kipra, uthos, xidor, iraz, baruta]

    return material_planes


def get_outer_planes() -> list[Plane]:
    outer_planes_orbit = Orbit(rotational_axis=[1.0, 1.0, 1.0], amplitude=OUTER_PLANES_AMPLITUDE)

    mount_delestia = Plane("Mount Delestia", orbit=outer_planes_orbit, period_in_hours=PERIOD_IN_HOURS_OUTER_PLANES,
        phase=2/8, color=OUTER_PLANES_COLOR, size=OUTER_PLANES_SIZE)
    elysium = Plane("Elysium",               orbit=outer_planes_orbit, period_in_hours=PERIOD_IN_HOURS_OUTER_PLANES,
        phase=3/8, color=OUTER_PLANES_COLOR, size=OUTER_PLANES_SIZE)
    the_beastlands = Plane("The Beastlands", orbit=outer_planes_orbit, period_in_hours=PERIOD_IN_HOURS_OUTER_PLANES,
        phase=4/8, color=OUTER_PLANES_COLOR, size=OUTER_PLANES_SIZE)
    limbo = Plane("Limbo",                   orbit=outer_planes_orbit, period_in_hours=PERIOD_IN_HOURS_OUTER_PLANES,
        phase=5/8, color=OUTER_PLANES_COLOR, size=OUTER_PLANES_SIZE)
    the_abyss = Plane("The Abyss",           orbit=outer_planes_orbit, period_in_hours=PERIOD_IN_HOURS_OUTER_PLANES,
        phase=6/8, color=OUTER_PLANES_COLOR, size=OUTER_PLANES_SIZE)
    the_nine_hells = Plane("The Nine Hells", orbit=outer_planes_orbit, period_in_hours=PERIOD_IN_HOURS_OUTER_PLANES,
        phase=7/8, color=OUTER_PLANES_COLOR, size=OUTER_PLANES_SIZE)
    outer_planes = [mount_delestia, elysium, the_beastlands, limbo, the_abyss, the_nine_hells]

    return outer_planes


def get_feyfell_planes() -> list[Plane]:
    feyfell_orbit = Orbit(rotational_axis=[1.0, 0.0, 0.6], amplitude=INNER_PLANES_AMPLITUDE)

    feywild = Plane("Feywild", orbit=feyfell_orbit, period_in_hours=PERIOD_IN_HOURS_OTHER_INNER_PLANES, phase=0.0, color="#dba1e0", size=20)
    shadowfell = Plane("Shadowfell", orbit=feyfell_orbit, period_in_hours=PERIOD_IN_HOURS_OTHER_INNER_PLANES, phase=0.5, color="#7f7f7f", size=20)
    feyfell = [feywild, shadowfell]

    return feyfell


def get_isune_cosmology():

    arcane_core = Plane("Arcane Core", orbit=None, period_in_hours=1, phase=0.0, color="#ffff99", size=25)
    material_planes = get_material_planes()
    feyfell_planes = get_feyfell_planes()
    # - Ethereal plane
    outer_planes = get_outer_planes()

    planes = [arcane_core, *material_planes, *outer_planes], feyfell_planes

    return planes
