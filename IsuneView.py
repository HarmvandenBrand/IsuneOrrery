import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, State, Input

import plotly.graph_objects as go

from IsuneOrrery import Plane, ExtrusionPlane, AsteroidBeltPlane, Orbit, Orrery
from IsuneCalendar import Calendar, Hour

FIG_WIDTH_PIXELS = 1820
FIG_HEIGHT_PIXELS = 1000
SCENE_SIZE = 35

TEST_ORBIT = Orbit(rotational_axis=[0.0, 0.0, 1.0], amplitude=20)
TEST_PLANES = [Plane("Test", orbit=TEST_ORBIT, period_in_hours=24 * 8, phase=0 / 8, color="#010101", size=20)]

SLICE_ORBIT_OPACITY = 0.5
UNIFORM_SIZE_FACTOR = 1.5


class IsuneDashApp:

    def __init__(self, orrery: Orrery):
        self.orrery = orrery
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

            self.orrery.calendar = Calendar(years=years, months=months, days=days, hours=hours)

    def create_traces_from_orrery(self):
        dfs_dict = self.orrery.get_locations_as_dataframe_dict()
        simple_planes_dict = dfs_dict["simple planes"]
        extrusion_planes_dict = dfs_dict["extrusion planes"]
        asteroid_planes_dict = dfs_dict["asteroid planes"]

        traces = []

        for key in simple_planes_dict.keys():
            df = simple_planes_dict[key]
            traces.append(go.Scatter3d(x=df['x'], y=df['y'], z=df['z'], text=df['name'], mode='markers', marker=dict(color=df['color'], size=df['size']*UNIFORM_SIZE_FACTOR), opacity=0.9, name=key))

        for key in extrusion_planes_dict.keys():
            df = extrusion_planes_dict[key]
            traces.append(go.Scatter3d(x=df['x'], y=df['y'], z=df['z'], text=df['name'], mode='lines', line=dict(width=df['size'][0]*UNIFORM_SIZE_FACTOR, color=df['color'][0]), name=df['name'][0], opacity=SLICE_ORBIT_OPACITY, hovertemplate='%{text}<extra></extra>'))

        for key in asteroid_planes_dict.keys():
            df = asteroid_planes_dict[key]
            colorscale = [[0, '#bff0fc'], [1, '#ffffff']]
            traces.append(go.Cone(x=df['x'], y=df['y'], z=df['z'], u=df['u'], v=df['v'], w=df['w'], text=df['name'][0], name=df['name'][0], sizemode='absolute', sizeref=400000, colorscale=colorscale, showscale=False, hovertemplate=f'{df["name"][0]}<extra></extra>', showlegend=True))

        return traces

    def calculate_fig(self):

        traces = self.create_traces_from_orrery()

        if self.fig is None:
            self.fig = go.Figure(data=traces)

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

            # Remove unnecessary empty margins
            self.fig.layout.margin = dict(l=0, r=0, t=0, b=0)

            # Position the legend (= the list of traces) on top right corner ON TOP OF graph
            self.fig.layout.legend.xref = 'paper'
            self.fig.layout.legend.xanchor = 'right'
            self.fig.layout.legend.x = 1
            self.fig.layout.legend.yref = 'paper'
            self.fig.layout.legend.yanchor = 'bottom'
            self.fig.layout.legend.y = 0

            # Set legend background color to about the same as the plot xy-plane, but with transparancy
            self.fig.layout.legend.bgcolor = f'rgba({str(256-108)},{str(256-80)},{str(256-40)},0.25)'

        else:
            for trace in traces:
                self.fig = self.fig.update_traces(trace, selector=dict(name=trace.name), overwrite=False)

        return self.fig


    def get_app(self):
        # Initialize the app
        app = dash.Dash("Isune Astrolabe")

        self.calculate_fig()

        # App layout
        app.layout = html.Div(children=
        [
            dcc.Graph(id='graph', responsive=True, figure=self.fig, style={'width': '95vw', 'height': '85vh'}),

            html.Div(
                [
                    dcc.Input(id='calendar-field', value='0000/01/01 00:00', type='text', size="12", style={'min-width':'10em%', 'height':'3em'}),
                    html.Button(children='update', id='update-button'),
                    html.Button(children='-1', id='minus-1-hour-button', style={'min-width':'3em'}),
                    html.Button(children='+1', id='plus-1-hour-button', style={'min-width':'3em'}),
                    html.Button(children="►", id='play-button', style={'min-width':'3em'}),
                    dcc.Interval(id='interval-component', interval=0.5 * 1000, n_intervals=0, disabled=True)  # interval is in milliseconds, disabled=True so it begins inactive
                    # ])
                ], style={'display': 'flex', 'justify-content': 'center'}),

        ])

        self.calculate_fig()



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
            """Toggles the icon on the autoplay/pause button."""
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
            Output('calendar-field', 'value'),
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
            """Main callback function to update the graph. Should be called whenever the figure should be updated, which is
            at least whenever the calendar date is channged."""
            if n_clicks_update is None and n_clicks_minus_1 is None and n_clicks_plus_1 is None and n_intervals is None:
                return dash.no_update
            else:

                triggered_id = dash.ctx.triggered_id

                if triggered_id == 'update-button':
                    self.parse_calendar(value)
                elif triggered_id == 'minus-1-hour-button':
                    self.orrery.calendar = self.orrery.calendar - Hour(1)
                elif triggered_id == 'plus-1-hour-button':
                    self.orrery.calendar = self.orrery.calendar + Hour(1)
                elif triggered_id == 'interval-component':
                    self.orrery.calendar = self.orrery.calendar + Hour(1)

                self.calculate_fig()

                return self.fig, str(self.orrery.calendar)

        return app
