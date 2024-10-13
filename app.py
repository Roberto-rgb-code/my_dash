import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Cargar los datos
url = "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
df = pd.read_csv(url)

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Diseño del dashboard
app.layout = html.Div([
    html.H1("Dashboard de Datos Mundiales"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in df['year'].unique()],
        value=df['year'].min(),
        style={'width': '50%'}
    ),
    dcc.Graph(id='life-exp-vs-gdp')
])

# Callback para actualizar el gráfico
@app.callback(
    Output('life-exp-vs-gdp', 'figure'),
    Input('year-dropdown', 'value')
)
def update_graph(selected_year):
    filtered_df = df[df.year == selected_year]
    
    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp", 
                     size="pop", color="continent", hover_name="country", 
                     log_x=True, size_max=60,
                     title=f'Esperanza de vida vs. PIB per cápita ({selected_year})')
    
    return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)