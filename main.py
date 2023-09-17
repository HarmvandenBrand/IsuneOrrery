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
- affix layout
- host as github page
- add month names to calendar
- remove 3d "box" surrounding the data (but retain axes?)
- graph loading spinner (https://dash.plotly.com/dash-core-components/loading)
- set useful hover-tooltips for planes 
'''

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


    veka   = Plane("Veka",   amplitude=INNER_PLANES_AMPLITUDE, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=0/8, color=None)
    aspen  = Plane("Aspen",  amplitude=INNER_PLANES_AMPLITUDE, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=1/8, color=None)
    oshya  = Plane("Oshya",  amplitude=INNER_PLANES_AMPLITUDE, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=2/8, color=None)
    kipra  = Plane("Kipra",  amplitude=INNER_PLANES_AMPLITUDE, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=3/8, color=None)
    uthos  = Plane("Uthos",  amplitude=INNER_PLANES_AMPLITUDE, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=4/8, color=None)
    xidor  = Plane("Xidor",  amplitude=INNER_PLANES_AMPLITUDE, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=5/8, color=None)
    iraz   = Plane("Iraz",   amplitude=INNER_PLANES_AMPLITUDE, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=6/8, color=None)
    baruta = Plane("Baruta", amplitude=INNER_PLANES_AMPLITUDE, period_in_hours=PERIOD_IN_HOURS_MATERIAL_PLANES, phase=7/8, color=None)


    arcane_core = Plane("Arcane Core", amplitude=0, period_in_hours=1, phase=0.0, color="#ffff22")

    planes = [arcane_core, veka, aspen, oshya, kipra, uthos, xidor, iraz, baruta]

    isune_dash = IsuneDashApp(planes)
    isune_dash.run_dash_tutorial(planes)

