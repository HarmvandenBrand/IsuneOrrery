# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from IsuneCalendar import Calendar, Year, Month, Day, Hour
from IsuneAstrolabe import Plane

import math

# display shit
import matplotlib.pyplot as plt, mpld3
import numpy as np
from matplotlib.widgets import Slider, Button, TextBox

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # cal1 = Calendar(3, 4, 10, 23)
    # cal2 = Calendar(0, 11, 25, 23)

    cal0 = Calendar(0, 1, 1, 0)
    cal3 = Calendar(12, 12, 29, 0)
    cal4 = Calendar(0, 1, 1, 1)

    # print(cal3)
    # print(cal4)
    # print(cal3 + cal4)
    # print(cal3.weekday())
    #
    # print(cal3 - Day(5))

    print(cal3.total_hours())



    plane = Plane("kek")

    plane_locations = [[*plane.location_from_hours(i), i] for i in range(24*30)]

    ##### single-frame, non-rotational

    # fig = plt.figure()
    # ax = fig.add_subplot(projection='3d')
    # ax.set_xlabel('X Label')
    # ax.set_ylabel('Y Label')
    # ax.set_zlabel('Z Label')
    #
    # for i in range(24):
    #     loc = plane.location_at_date(cal0 + Hour(i))
    #     print(loc)
    #     ax.scatter(loc[0], loc[1], loc[2], marker=i%12)
    #
    # plt.show()


    ##### non-rotational

    # f = plane.location_from_hours
    # t = np.linspace(0, 1, 24)
    #
    # fig = plt.figure()
    # ax = fig.add_subplot(projection='3d')
    # ax.set_xlabel('X Label')
    # ax.set_ylabel('Y Label')
    # ax.set_zlabel('Z Label')
    #
    # point = ax.scatter(*f(0), marker=1)
    #
    # def submit(text):
    #     hours = eval(text)
    #     ax.scatter(*f(hours), marker=1)
    #     plt.draw()
    #
    # axbox = fig.add_axes([0.1, 0.05, 0.8, 0.075])
    # text_box = TextBox(axbox, "Evaluate", textalignment="center")
    # text_box.on_submit(submit)
    # text_box.set_val("4")
    #
    # plt.show()



    ####### plotly

    # import plotly.express as px
    #
    # df = plane_locations
    # fig = px.scatter_3d(df, x=0, y=1, z=2, animation_frame=3, size_max=18, opacity=0.7)
    #
    # # tight layout
    # fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    # fig.show()


    ##### plotly generative

    # import plotly.express as px
    #
    # df = plane_locations
    # f = plane.location_from_hours
    # fx = plane.x_from_hours
    # fy = plane.y_from_hours
    # fz = plane.z_from_hours
    # fig = px.scatter_3d(x=fx, y=fy, z=fz, animation_frame=list(range(24)), size_max=18, opacity=0.7)
    #
    #
    # # tight layout
    # fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    # fig.show()

    ##### plotly dash

    import dash
    from dash import dcc
    from dash import html
    from dash.dependencies import Output, State, Input

    import plotly.express as px

    # df = plane_locations
    data = [[plane.location_from_hours(0)], [2, 2, 2]]
    fig = px.scatter_3d(data, x=0, y=1, z=2, size_max=18, opacity=0.7)

    # tight layout
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    # fig.show()

    app = dash.Dash()

    app.layout = html.Div([
        html.H4("Title"),
        dcc.Graph(id='graph-court', figure=fig),
        dcc.Input(id='username', value='0', type='text'),
        html.Button(id='submit-button', type='submit', children='Submit'),
        html.Div(id='output_div')
    ])


    # @app.callback(Output('output_div', 'children'),
    #               [Input('submit-button', 'n_clicks')],
    #               [State('username', 'value')],
    #               )
    # def update_output(clicks, input_value):
    #     if clicks is not None:
    #         print(clicks, input_value)
    #         hours = int(input_value)
    #         data = [[plane.location_from_hours(hours)], [2,2,2]]
    #         px.scatter_3d(data, x=0, y=1, z=2, size_max=18, opacity=0.7)
    #         fig.update_layout()
    #         return fig

    @app.callback(Output('output_div', 'figure'),
                  [Input('submit-button', 'n_clicks')],
                  [State('username', 'value')],
                  )
    def update_output(clicks, input_value):
        if clicks is not None:
            print(clicks, input_value)
            hours = int(input_value)
            data = [[plane.location_from_hours(hours)], [2,2,2]]
            px.scatter_3d(data, x=0, y=1, z=2, size_max=18, opacity=0.7)
            fig.update_layout()
            return fig


    app.run_server(host='0.0.0.0')
