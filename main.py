import IsuneCosmology
from IsuneOrrery import Orrery
from IsuneView import IsuneDashApp


##### TODO #####
'''
- fix plane size independent of zoom level (maybe replace scatterplot with https://stackoverflow.com/questions/70977042/how-to-plot-spheres-in-3d-with-plotly-or-another-library)
- make calendar date client-side instead of server-side
- fix issue where camera can't be dragged and figure won't be updated during animation (i.e. when interval is enabled)
- fix bug so that loading screen is no longer called on any change to graph or any callback
- add different play speeds
- beautify layout (e.g. css the current date and controls, use month name)
'''


def initialize():

    planes = IsuneCosmology.get_isune_cosmology()
    isune_orrery = Orrery(*planes)
    isune_dash = IsuneDashApp(isune_orrery)
    app = isune_dash.get_app()

    return app


if __name__ == "__main__":
    app = initialize()
    app.run(debug=True)


