#Libraries for the dashboard
from pydoc import classname
import dash
import dash_bootstrap_components as dbc
import dash_labs as dl
from dash import Input, Output, dcc, html
import dash_auth
#from dash.dependencies import Input, Ouput, State

# VALID_USERNAME_PASSWORD_PAIRS = {
#    'GACS': 'GACS'
#}

#Images of this page
Uniandes_logo = "https://github.com/Andresbeltran200/logo_despliegue_dash/blob/main/Uniandes.png?raw=true"
data_logo = "https://github.com/Andresbeltran200/logo_despliegue_dash/blob/main/logo2.png?raw=true"
MAIN_LOGO = "https://github.com/jorgeandreszr9/DS4A_Team138/blob/main/logo3.png?raw=true"

request_path_prefix = '/'

app = dash.Dash(
    __name__, plugins=[dl.plugins.pages],
    external_stylesheets=[dbc.themes.MORPH, dbc.icons.FONT_AWESOME],
    requests_pathname_prefix=request_path_prefix
)
#auth = dash_auth.BasicAuth(
#    app,
#    VALID_USERNAME_PASSWORD_PAIRS
#)
 
#Title of Main Page
logo = html.Div(
            html.Img(src=Uniandes_logo, style={"width": "150px","height": "70px"})
)

mytitle = html.H2("¿Cuál es la probabilidad de que haya un accidente fatal en un accidente automovilístico en México?", className="title")


sub_title = html.H6("Gloria Ramos - Cristhian Amaya - Sergio Rojas - Andres Beltrán // Fuente: INEGI", className="subtitle") 

    
parrafo =   html.P("Bienvenido a la página de predicción. Selecciona los valores de las variables para realizar una predicción."),
    

logo1 = html.Div(
            html.Img(src=data_logo, style={"width": "100px","height": "100px"})
)

sidebar = html.Div(
    [
        html.Div(
            [
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                html.I(["  Paginas"],className="fas fa-chart-bar xl-15"),
                html.H6 (" "),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    #[html.I(className="fas fa-globe me-2"), html.Span("La Ascensión"),html.H6("Estado Actual",className="anexos")],
                    [html.I(className="fas fa-globe me-2"), html.Span("Análisis descriptivo"),html.H6("Descripción de la situación actual",className="anexos")],
                    href="/", style={"height": "100px"},
                    active="exact",
                ),
                dbc.NavLink(
                    #[html.I(className="fas fa-home me-2"), html.Span("Vivienda"),html.H6("Plomería",className="anexos"),
                    [html.I(className="fas fa-home me-2"), html.Span("Modelo predictivo"),html.H6("Predicción de probabildiad de",className="anexos"),
                    html.H6("fallecido en un accidente",className="anexos")],
                    href="/Prediccion", style={"height": "100px"},
                    active="exact",
                ),
                #dbc.NavLink(
                #    [html.I(className="fas fa-car me-2"), html.Span("Vehicular"), html.H6("Carros", className="anexos"), 
                #    html.H6("Motocicletas",className="anexos")],
                #    href="/Vehicular", style={"height": "100px"},
                #    active="exact",
                #),
                #dbc.NavLink(
                #    [html.I(className="fas fa-dog me-2"), html.Span("Mascotas"), html.H6("Perros",className="anexos"), 
                #    html.H6("Gatos",className="anexos")],
                #    href="/Mascotas", style={"height": "100px"},
                #    active="exact",
                #),
                
                #dbc.NavLink(
                #    [
                #        html.I(className="fas fa-people-group me-2"),
                #        html.Span("Nosotros"),
                #    ],
                #    href="/Nosotros",
                #    active="exact",
                #),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)

#Layout main for this app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([logo1], md=2, align="center"),
        dbc.Col([mytitle],md=8, align="center"),
        dbc.Col([logo], md=2, align="center")
    ]),
    dbc.Row([
        dcc.Location(id="url"),
        dbc.Col([sidebar], md=2, align="center"),
        dbc.Col([
            dl.plugins.page_container
            ], md=10, align="center")
    ]),
    dbc.Row([
        dbc.Col([sub_title],md=10, align="center"),
    ]), 
])

# Call to external function to register all callbacks
#register_callbacks(app)

# This call will be used with Gunicorn server
application = app.server

# Testing server, don't use in production, host
if __name__ == "__main__":
    ##application.run(host='0.0.0.0', port=8050)
    import uvicorn

    # ejecución del servidor - host para ejecutar en servidor 
    uvicorn.run(app, host="0.0.0.0", port=8050, log_level="debug")