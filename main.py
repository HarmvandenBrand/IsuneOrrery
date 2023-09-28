from IsuneOrrery import Plane, Orbit
from IsuneView import IsuneDashApp


##### TODO #####
'''
- add other planes
- fix plane size independent of zoom level (maybe replace scatterplot with https://stackoverflow.com/questions/70977042/how-to-plot-spheres-in-3d-with-plotly-or-another-library)
- add month names to calendar
- make calendar date client-side instead of server-side
- fix issue where camera can't be dragged and figure won't be updated during animation (i.e. when interval is enabled)
- Op data vóór 0/0/0, alle planeten deleten en replacen met Ven'ron?
- graph loading spinner (https://dash.plotly.com/dash-core-components/loading)
- set useful hover-tooltips for planes 
- beautify layout (e.g. reposition and css the current date)
'''


def get_isune_cosmology():

    # material plane axis: 8 days
    # fey-shadowfell and ethereal planes: 16 days
    # outer planes: 32 days

    INNER_PLANES_AMPLITUDE = 10
    OUTER_PLANES_AMPLITUDE = 30
    OUTER_PLANES_INCLINATION = 0.4
    PERIOD_IN_HOURS_MATERIAL_PLANES = 24*8
    PERIOD_IN_HOURS_OTHER_INNER_PLANES = 24*16
    PERIOD_IN_HOURS_OUTER_PLANES = 24*32

    OUTER_PLANES_COLOR = "#aaaaaa"
    OUTER_PLANES_SIZE = 15


    material_planes_orbit = Orbit(rotational_axis=[0.0, 0.0, 1.0], amplitude=INNER_PLANES_AMPLITUDE)  # ecliptical plane
    outer_planes_orbit = Orbit(rotational_axis=[1.0, 1.0, 1.0], amplitude=OUTER_PLANES_AMPLITUDE)

    # The arcane core
    arcane_core = Plane("Arcane Core", orbit=None, period_in_hours=1, phase=0.0, color="#ffff99", size=30)

    # Material planes
    veka   = Plane("Veka",   orbit=material_planes_orbit, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=0/8, color="#54d3ab", size=20)
    aspen  = Plane("Aspen",  orbit=material_planes_orbit, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=1/8, color="#41acc1", size=8)
    oshya  = Plane("Oshya",  orbit=material_planes_orbit, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=2/8, color="#4175c1", size=11)
    kipra  = Plane("Kipra",  orbit=material_planes_orbit, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=3/8, color="#79c141", size=18)
    uthos  = Plane("Uthos",  orbit=material_planes_orbit, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=4/8, color="#e8ac22", size=9)
    xidor  = Plane("Xidor",  orbit=material_planes_orbit, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=5/8, color="#888888", size=9)
    iraz   = Plane("Iraz",   orbit=material_planes_orbit, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=6/8, color="#ee0022", size=17)
    baruta = Plane("Baruta", orbit=material_planes_orbit, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=7/8, color="#8c06ad", size=7)
    material_planes = [veka, aspen, oshya, kipra, uthos, xidor, iraz, baruta]

    # Inner planes
        # Ethereal plane
        # Feywild/Shadowfell plane

    # Outer planes
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

    planes = [arcane_core, *material_planes, *outer_planes]

    return planes

def initialize():

    planes = get_isune_cosmology()
    isune_dash = IsuneDashApp(planes)
    app = isune_dash.get_app(planes)

    return app

if __name__ == "__main__":
    app = initialize()
    app.run(debug=True)


