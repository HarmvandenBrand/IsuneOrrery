import dash
import plotly.graph_objects
from dash import dcc
from dash import html
from dash.dependencies import Output, State, Input

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from IsuneAstrolabe import Plane
from IsuneCalendar import Calendar, Hour

# def add_bounding_points(fig: Figure):
#     fig.add_scatter3d()





class IsuneDashApp:

    def __init__(self, planes: list[Plane], calendar=Calendar(0,1,1,0)):
        self.calendar = calendar
        self.planes = planes
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
        locations = [[*plane.location_from_hours(self.calendar.total_hours())] for plane in planes]
        location_dict = {'x':[v[0] for v in locations], 'y':[v[1] for v in locations], 'z':[v[2] for v in locations]}
        df = pd.DataFrame(location_dict)
        df['color'] = [plane.color if plane.color is not None else '#dddddd' for plane in planes]
        df['name'] = [plane.name if plane.name is not None else 'None' for plane in planes]
        df['size'] = [plane.size*2 for plane in planes]

        print(df)

        return df


    def calculate_fig(self):
        df = self.planes_to_df(self.planes)
        scatter = go.Scatter3d(x=df['x'], y=df['y'], z=df['z'], text=df['name'], mode='markers', opacity=0.9)

        if self.fig is None:
            self.fig = go.Figure(data=scatter)

            # add colors
            self.fig.update_traces(marker=dict(color=df['color'], size=df['size']))

            # important line, maintains user-adjusted camera view after figure update
            self.fig.layout.uirevision = 1

            # also an important line. First update will trigger camera position reset otherwise
            self.fig.update_layout(width=1200, height=800, autosize=False)

        else:
            self.fig = self.fig.update_traces(scatter, overwrite=False)

        return self.fig


    def run_dash_tutorial(self, planes: list[Plane]):

        # Initialize the app
        app = dash.Dash("Isune Astrolabe")

        self.calculate_fig()

        # App layout
        app.layout = html.Div(
        [
            dcc.Graph(id='graph', figure=self.fig),
            dcc.Input(id='calendar-field', value='0000/01/01 00:00', type='text'),
            html.Button(children='update', id='update-button'),
            html.Button(children='-1', id='minus-1-hour-button'),
            html.Button(children='+1', id='plus-1-hour-button'),
        ])

        @app.callback(
            Output('graph', 'figure'),
            [
                Input('update-button', 'n_clicks'),
                Input('minus-1-hour-button', 'n_clicks'),
                Input('plus-1-hour-button', 'n_clicks')
            ],
            [
                State('calendar-field', 'value')
            ]
        )
        def update_figure(n_clicks_update, n_clicks_minus_1, n_clicks_plus_1, value):

            if n_clicks_update is None and n_clicks_minus_1 is None and n_clicks_plus_1 is None:
                return dash.no_update
            else:

                triggered_id = dash.ctx.triggered_id
                print(triggered_id)
                if triggered_id == 'update-button':
                    self.parse_calendar(value)
                elif triggered_id == 'minus-1-hour-button':
                    self.calendar = self.calendar - Hour(1)
                elif triggered_id == 'plus-1-hour-button':
                    self.calendar = self.calendar + Hour(1)

                self.calculate_fig()

                return self.fig

        app.run(debug=True)
