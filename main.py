import IsuneCosmology
from IsuneView import IsuneDashApp


##### TODO #####
'''
- add ethereal plane (swarm of cone plots?)
- fix plane size independent of zoom level (maybe replace scatterplot with https://stackoverflow.com/questions/70977042/how-to-plot-spheres-in-3d-with-plotly-or-another-library)
- add month names to calendar
- make calendar date client-side instead of server-side
- fix issue where camera can't be dragged and figure won't be updated during animation (i.e. when interval is enabled)
- graph loading spinner (https://dash.plotly.com/dash-core-components/loading)
- Remove trace info on hover for material and outer planes
- Put outer planes in different trace
- beautify layout (e.g. reposition and css the current date)
- refactor Ven'ron logic
'''

def initialize():

    planes, feyfell = IsuneCosmology.get_isune_cosmology()
    isune_dash = IsuneDashApp(planes, feyfell)
    app = isune_dash.get_app(planes)

    return app


if __name__ == "__main__":
    app = initialize()
    app.run(debug=True)


