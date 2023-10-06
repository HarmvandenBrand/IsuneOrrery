import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, State, Input

import plotly.graph_objects as go
import pandas as pd

from IsuneOrrery import Plane, ExtrusionPlane, AsteroidBeltPlane, Orbit
from IsuneCalendar import Calendar, Hour


SCENE_SIZE = 35

TEST_ORBIT = Orbit(rotational_axis=[0.0, 0.0, 1.0], amplitude=20)
TEST_PLANES = [Plane("Test", orbit=TEST_ORBIT, period_in_hours=24 * 8, phase=0 / 8, color="#010101", size=20)]

SLICE_ORBIT_OPACITY = 0.5


class IsuneDashApp:

    def __init__(self, planes: list[Plane], calendar=Calendar(0,1,1,0)):
        self.calendar = calendar
        self.simple_planes = [plane for plane in planes if type(plane) is Plane]
        self.extrusion_planes = [plane for plane in planes if type(plane) is ExtrusionPlane]
        self.asteroid_planes = [plane for plane in planes if type(plane) is AsteroidBeltPlane]
        self.fig = None

    def parse_calendar(self, calendar_string: str) -> Calendar:
        if calendar_string is None:
            raise ValueError("Invalid calendar value")
        else:
            values = calendar_string.split('/')

            # accept number of hours from zero as valid input for debugging purposes
            if len(values) == 1:
                return Calendar(0, 1, 1, int(values[0]))

            years = int(values[0])
            months = int(values[1])
            days = int(values[2].split(' ')[0])
            hours = int(values[2].split(' ')[1].split(':')[0])

            self.calendar = Calendar(years=years, months=months, days=days, hours=hours)

    def planes_to_df(self, planes: list[Plane]):
        """Orders calculation of the current state of the orrery and creates a dataframe from that data.
        This function assumes the calendar date has already been correctly set."""

        # Delete all planes before the zero date and display only Venron
        # TODO: refactor this model logic away from the view
        if self.calendar < Calendar(0, 1, 1, 0):
            planes = [Plane("Ven'ron", orbit=None, period_in_hours=10, phase=0.0, color="#bbbbee", size=45)]

        locations = [[*plane.location_from_hours(self.calendar.total_hours())] for plane in planes]
        location_dict = {'x': [v[0] for v in locations], 'y': [v[1] for v in locations], 'z': [v[2] for v in locations]}
        df = pd.DataFrame(location_dict)
        df['color'] = [plane.color if plane.color is not None else '#dddddd' for plane in planes]
        df['name'] = [plane.name if plane.name is not None else 'None' for plane in planes]
        df['size'] = [int(plane.size*1.5) for plane in planes]

        return df


    def plane_extrusion_to_df(self, plane: ExtrusionPlane, phase_offset_minus, phase_offset_plus):
        locations = [*plane.locations_extrusion_from_hours(self.calendar.total_hours(), 50)]
        location_dict = {'x': [v[0] for v in locations], 'y': [v[1] for v in locations], 'z': [v[2] for v in locations]}
        df = pd.DataFrame(location_dict)
        df['color'] = plane.color if plane.color is not None else '#dddddd'
        df['name'] = plane.name if plane.name is not None else 'None'
        df['size'] = int(plane.size*1.5)

        return df

    def plane_asteroid_to_df(self, plane: AsteroidBeltPlane):

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
        df['size'] = int(plane.size * 1.5)

        return df

    def calculate_fig(self):
        simple_df = self.planes_to_df(self.simple_planes)
        simple_planes_trace = go.Scatter3d(x=simple_df['x'], y=simple_df['y'], z=simple_df['z'], text=simple_df['name'], mode='markers', opacity=0.9, name="Material Planes")

        feywild_df = self.plane_extrusion_to_df(self.extrusion_planes[0], 0.24, 0.24)
        feywild_trace = go.Scatter3d(x=feywild_df['x'], y=feywild_df['y'], z=feywild_df['z'], text=feywild_df['name'], mode='lines', line=dict(width=feywild_df['size'][0], color=feywild_df['color'][0]), name=feywild_df['name'][0], opacity=SLICE_ORBIT_OPACITY, hovertemplate='%{text}<extra></extra>')

        shadowfell_df = self.plane_extrusion_to_df(self.extrusion_planes[1], 0.24, 0.24)
        shadowfell_trace = go.Scatter3d(x=shadowfell_df['x'], y=shadowfell_df['y'], z=shadowfell_df['z'], text=shadowfell_df['name'], mode='lines', line=dict(width=shadowfell_df['size'][0], color=shadowfell_df['color'][0]), name=shadowfell_df['name'][0], opacity=SLICE_ORBIT_OPACITY, hovertemplate='%{text}<extra></extra>')

        ethereal_df = self.plane_asteroid_to_df(self.asteroid_planes[0])
        ethereal_colorscale = [[0, '#bff0fc'], [1, '#ffffff']]
        ethereal_trace = go.Cone(x=ethereal_df['x'], y=ethereal_df['y'], z=ethereal_df['z'], u=ethereal_df['u'], v=ethereal_df['v'], w=ethereal_df['w'], text=ethereal_df['name'][0], name=ethereal_df['name'][0], sizemode='absolute', sizeref=400000, colorscale=ethereal_colorscale, showscale=False, hovertemplate=f'{ethereal_df["name"][0]}<extra></extra>', showlegend=True)

        # test_df = self.planes_to_df(TEST_PLANES)
        # test_scatter = go.Scatter3d(x=test_df['x'], y=test_df['y'], z=test_df['z'], text=test_df['name'], mode='markers', opacity=0.9, name="FeyFell", hoverinfo='skip')  # Note the "hoverinfo='skip'"

        if self.fig is None:
            self.fig = go.Figure(data=simple_planes_trace)
            self.fig.add_trace(feywild_trace)
            self.fig.add_trace(shadowfell_trace)
            self.fig.add_trace(ethereal_trace)

            # add individual colors for material plane
            self.fig.update_traces(marker=dict(color=simple_df['color'], size=simple_df['size']), selector=dict(name="Material Planes"))

            # Test stuff
            # self.fig.add_trace(test_scatter)
            # self.fig.update_traces(marker=dict(color=test_df['color'], size=test_df['size']), selector=dict(name="FeyFell"))

            # important line, maintains user-adjusted camera view after figure update
            self.fig.layout.uirevision = 1
            self.fig.layout.scene.aspectmode = 'cube'

            # fix scene size
            self.fig.layout.scene.xaxis.range = [-SCENE_SIZE, SCENE_SIZE]
            self.fig.layout.scene.yaxis.range = [-SCENE_SIZE, SCENE_SIZE]
            self.fig.layout.scene.zaxis.range = [-SCENE_SIZE, SCENE_SIZE]

            # disable all axis information, except for a background in the xy-plane, which is kept as referencing point
            self.fig.layout.scene.xaxis.visible = False
            self.fig.layout.scene.yaxis.visible = False
            self.fig.layout.scene.zaxis.visible = True
            self.fig.layout.scene.zaxis.showticklabels = False
            self.fig.layout.scene.zaxis.showaxeslabels = False
            self.fig.layout.scene.zaxis.title = ""
            self.fig.layout.scene.zaxis.showbackground = True

            # also an important line. First update will trigger camera position reset otherwise
            self.fig.update_layout(width=1200, height=800, autosize=False)

        else:
            self.fig = self.fig.update_traces(simple_planes_trace, selector=dict(name="Material Planes"), overwrite=False)
            # self.fig = self.fig.update_traces(test_scatter, selector=dict(name="FeyFell"), overwrite=False)
            self.fig = self.fig.update_traces(feywild_trace, selector=dict(name="Feywild"), overwrite=False)
            self.fig = self.fig.update_traces(shadowfell_trace, selector=dict(name="Shadowfell"), overwrite=False)
            self.fig = self.fig.update_traces(ethereal_trace, selector=dict(name="Ethereal Plane"), overwrite=False)

        return self.fig


    def get_app(self, planes: list[Plane]):

        # Initialize the app
        app = dash.Dash("Isune Astrolabe")

        self.calculate_fig()

        # App layout
        app.layout = html.Div(
        [
            html.Div(id='current-date-div', children=str(self.calendar)),
            # dcc.Loading(id="loading-screen-graph", type="cube", fullscreen=True, children=dcc.Graph(id='graph', figure=self.fig)),
            dcc.Graph(id='graph', figure=self.fig),
            dcc.Input(id='calendar-field', value='0000/01/01 00:00', type='text'),
            html.Button(children='update', id='update-button'),
            html.Button(children='-1', id='minus-1-hour-button'),
            html.Button(children='+1', id='plus-1-hour-button'),
            html.Button(children="►", id='play-button'),
            dcc.Interval(id='interval-component', interval=0.5 * 1000, n_intervals=0, disabled=True)  # interval is in milliseconds, disabled=True so it begins inactive
        ])


        @app.callback(
            Output('interval-component', 'disabled'),
            Output('play-button', 'children'),
            [
                Input('play-button', 'n_clicks')
            ],
            [
                State('interval-component', 'disabled')
            ]
        )
        def toggle_interval(button_clicks, disabled_state):
            if button_clicks is not None and button_clicks > 0:
                if disabled_state:
                    return not disabled_state, "||"
                else:
                    return not disabled_state, "►"
            else:
                return disabled_state, "►"

        # Callback for the manipulation of buttons
        @app.callback(
            Output('graph', 'figure'),
            Output('current-date-div', 'children'),
            [
                Input('update-button', 'n_clicks'),
                Input('minus-1-hour-button', 'n_clicks'),
                Input('plus-1-hour-button', 'n_clicks'),
                Input('interval-component', 'n_intervals')
            ],
            [
                State('calendar-field', 'value')
            ]
        )
        def update_figure(n_clicks_update, n_clicks_minus_1, n_clicks_plus_1, n_intervals, value):

            if n_clicks_update is None and n_clicks_minus_1 is None and n_clicks_plus_1 is None and n_intervals is None:
                return dash.no_update
            else:

                triggered_id = dash.ctx.triggered_id

                if triggered_id == 'update-button':
                    self.parse_calendar(value)
                elif triggered_id == 'minus-1-hour-button':
                    self.calendar = self.calendar - Hour(1)
                elif triggered_id == 'plus-1-hour-button':
                    self.calendar = self.calendar + Hour(1)
                elif triggered_id == 'interval-component':
                    self.calendar = self.calendar + Hour(1)


                self.calculate_fig()

                return self.fig, str(self.calendar)

        return app
