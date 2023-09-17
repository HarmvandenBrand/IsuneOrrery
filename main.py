# This is a sample Python script.
import sys

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from IsuneCalendar import Calendar, Year, Month, Day, Hour
from IsuneAstrolabe import Plane
from IsuneView import IsuneDashApp


##### TODO #####
'''
- add option to incline plane axis
- add other planes
- add arrow buttons for decreasing/increasing viewed date by one hour 
- host as github page
- add month names to calendar
- remove 3d "box" surrounding the data (but retain axes?)
- graph loading spinner (https://dash.plotly.com/dash-core-components/loading)
- set useful hover-tooltips for planes 
'''

def get_isune_cosmology():

    # The arcane core
    arcane_core = Plane("Arcane Core", amplitude=0, period_in_hours=1, phase=0.0, color="#ffff99", size=30)

    # Material planes
    veka   = Plane("Veka",   amplitude=INNER_PLANES_AMPLITUDE, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=0/8, color="#54d3ab", size=20)
    aspen  = Plane("Aspen",  amplitude=INNER_PLANES_AMPLITUDE, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=1/8, color="#41acc1", size=8)
    oshya  = Plane("Oshya",  amplitude=INNER_PLANES_AMPLITUDE, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=2/8, color="#4175c1", size=11)
    kipra  = Plane("Kipra",  amplitude=INNER_PLANES_AMPLITUDE, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=3/8, color="#79c141", size=18)
    uthos  = Plane("Uthos",  amplitude=INNER_PLANES_AMPLITUDE, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=4/8, color="#e8ac22", size=9)
    xidor  = Plane("Xidor",  amplitude=INNER_PLANES_AMPLITUDE, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=5/8, color="#888888", size=9)
    iraz   = Plane("Iraz",   amplitude=INNER_PLANES_AMPLITUDE, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=6/8, color="#ee0022", size=17)
    baruta = Plane("Baruta", amplitude=INNER_PLANES_AMPLITUDE, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=7/8, color="#8c06ad", size=5)

    # Inner planes
        # Ethereal plane
        # Feywild/Shadowfell plane

    # Outer planes
        # Mount Delestia,
        # Elysium,
        # The Beastlands
        # Limbo
        # The Abyss
        # The Nine Hells

    planes = [arcane_core, veka, aspen, oshya, kipra, uthos, xidor, iraz, baruta]

    return planes


if __name__ == '__main__':

    cal0 = Calendar(0, 1, 1, 0)
    cal3 = Calendar(12, 12, 29, 0)
    cal4 = Calendar(0, 1, 1, 1)

    print(cal3.total_hours())

    # material plane axis: 8 days
    # fey-shadowfell and ethereal planes: 16 days
    # outer planes: 32 days

    INNER_PLANES_AMPLITUDE = 10
    PERIOD_IN_HOURS_MATERIAL_PLANES = 24*8
    PERIOD_IN_HOURS_OTHER_INNER_PLANES = 24*16
    PERIOD_IN_HOURS_OUTER_PLANES = 24*32

    planes = get_isune_cosmology()

    isune_dash = IsuneDashApp(planes)
    isune_dash.run_dash_tutorial(planes)

