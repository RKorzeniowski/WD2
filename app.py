import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

surv_df = pd.read_csv('ceidg_data_surv.csv')
surv_df.loc[:, 'YearOfStartingOfTheBusiness'] = pd.to_datetime(surv_df['YearOfStartingOfTheBusiness'], format='%Y')
surv_df.loc[:, 'DateOfStartingOfTheBusiness'] = pd.to_datetime(surv_df['DateOfStartingOfTheBusiness'], format='%Y-%m-%d')
surv_df.loc[:, 'DateOfTermination'] = pd.to_datetime(surv_df['DateOfTermination'], format='%Y-%m-%d')

surv_removed_df = surv_df[surv_df['Terminated'] == 1]
surv_removed_df.loc[:, 'YearOfTermination'] = surv_removed_df['DateOfTermination'].dt.year

terminated_year_PDK_df = pd.DataFrame({'count': surv_removed_df.groupby(["YearOfTermination", "PKDMainSection"]).size()}).reset_index()



min_year = min(terminated_year_PDK_df['YearOfTermination'])
max_year = max(terminated_year_PDK_df['YearOfTermination'])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(
        id='graph-with-slider',
        ),
    dcc.Slider(
        id='year-slider',
        min=min_year,
        max=max_year,
        value=min_year,
        marks={str(year): str(year) for year in range(min_year, max_year)},
        step=None
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = terminated_year_PDK_df[terminated_year_PDK_df['YearOfTermination'] == selected_year] \
                    .sort_values('count', ascending=False)[:10]
    traces = [
        dict(
            x=filtered_df['PKDMainSection'],
            y=filtered_df['count'],
            type='bar'
        )
    ]
    return {
        'data': traces,
        'layout': dict(
            title='Number of terminated firms in year by PKDMain'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)