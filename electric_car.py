import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots


df = pd.read_csv("./Data preprocessing/charging station_car.csv", encoding = "cp949")
df_model = pd.read_csv("./Data preprocessing/car model.csv", encoding = "cp949")

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    html.H1("Electric vehicle charging station location selection data analysis", style = {"font-size" : "20px", "color" : "white", "text-align" : "center"})
                )
            ]),
            html.Br(),
            
            dbc.Row([
                dbc.Col(html.Div([dcc.Graph(id = "map_gp")]), width = 6),
                dbc.Col(html.Div([dcc.Graph(id = "line_gp")]), width = 6)
            ]),
            html.Br(),
            
            dbc.Row([
                dbc.Col(
                    html.Div([
                        dcc.Dropdown(
                            id = "map_Dropdown_1",
                            options = [
                                {"label" : i, "value" : i}for i in df['행정구역'].unique()],
                                multi = False,
                                value = "강남구",
                                searchable = True,
                                placeholder = "구역을 입력 해 주세요"
                        )])),

                dbc.Col(
                    html.Div([
                        dcc.Dropdown(
                            id = "map_Dropdown_2",
                            options = [
                                {"label" : i, "value" : i}for i in df_model['동'].unique()],
                                multi = False,
                                value = "논현동",
                                searchable = True,
                                placeholder = "동을 입력 해 주세요"
                        )
                    ])
                ) 
            ]),

            html.Br(),

            dbc.Row([
                dbc.Col(html.Div([dcc.Graph(id = "pie_gp_1")]), width = 3),
                dbc.Col(html.Div([dcc.Graph(id = "pie_gp_2")]), width = 3),
                dbc.Col(html.Div([dcc.Graph(id = "pie_gp_3")]), width = 3),
                dbc.Col(html.Div([dcc.Graph(id = "pie_gp_4")]), width = 3)
            ]),

            html.Br()
        ])
    )
])
@app.callback(
    Output(component_id = "map_gp", component_property = "figure"),
    Output(component_id = "line_gp", component_property = "figure"),
    Output(component_id = "pie_gp_1", component_property = "figure"),
    Output(component_id = "pie_gp_2", component_property = "figure"),
    Output(component_id = "pie_gp_3", component_property = "figure"),
    Output(component_id = "pie_gp_4", component_property = "figure"),
    Input(component_id = "map_Dropdown_1", component_property = "value"),
    Input(component_id = "map_Dropdown_2", component_property = "value")
)

def update_fig(map_Dropdown_1, map_Dropdown_2):


    car = go.Scatter(
        x = df[df['행정구역'] == map_Dropdown_1]['동'],
        y = df[df['행정구역'] == map_Dropdown_1]["동별 전기차 수"],
        fill='tozeroy',
        line=dict(
            color='rgb(000, 153, 255)',
        ),
        name = '전기차 수'
    )
    charging = go.Scatter(
        x = df[df['행정구역'] == map_Dropdown_1]['동'],
        y = df[df['행정구역'] == map_Dropdown_1]["동별 충전소 수"],
        fill='tozeroy',
        line=dict(
            color='rgb(102, 255, 051)',
        ),
        name = '충전소 수'
    )

    data = [car, charging]
    fig_1 = go.Figure(data=data)
    fig_1.update_layout(template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)')


    trace1 = go.Bar(x=df["동"],y=df["동별 전기차 수"],name="동별 전기차 수", marker=dict(color='rgb(000, 153, 255)'))

    trace2 = go.Bar(x=df["동"],y=df['동별 충전소 수'],name='동별 충전소 수', marker=dict(color='rgb(102, 255, 051)'))

    fig_2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig_2.add_trace(trace1)
    fig_2.add_trace(trace2,secondary_y=True)
    fig_2.update_layout(template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)')

    fig_3 = px.pie(df[df['행정구역'] == map_Dropdown_1], values = '동별 전기차 수', names = '동', hole = 0.4)
    fig_3.update_layout(template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        title = dict(text = "전기차 수", x = 0.48, y = 0.93))
    fig_4 = px.pie(df[df['행정구역'] == map_Dropdown_1], values = '동별 충전소 수', names = '동', hole = 0.4)
    fig_4.update_layout(template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        title = dict(text = "충전소 수", x = 0.48, y = 0.93))
    fig_5 = px.pie(df_model[df_model['동'] == map_Dropdown_2], names = '차명', hole = 0.4)
    fig_5.update_layout(template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        title = dict(text = "차량 모델 비율", x = 0.5, y = 0.93))
    fig_6 = px.pie(df_model[df_model['동'] == map_Dropdown_2], names = '충전단자', hole = 0.4)
    fig_6.update_layout(template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        title = dict(text = "충전타입 비율", x = 0.5, y = 0.93))

    return fig_1, fig_2, fig_3, fig_4, fig_5, fig_6


if __name__ == "__main__":
    app.run_server(debug=True)
