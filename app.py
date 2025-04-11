import pandas as pd
import plotly.express as px
from funzioni import *
from callback import *




server = app.server



#layout app
app.layout = html.Div(
    style={'backgroundColor': '#dce2f0', 'width':'100%'},  # Colore di sfondo
    children=[
        # Prima riga con i filtri
        html.Div(
            style={
                'width': '100%',
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'flex-start',
                'padding': '2rem',
            },
            children=[
                html.H1(children='Seleziona i filtri', style={'fontFamily': 'Roboto, sans-serif', 'marginBottom': '1rem'}),
                
                html.Div(
                    style={
                        'width': '90%',
                        'display': 'flex',
                        'flexDirection': 'row',
                        'justifyContent': 'space-between',
                    },
                    children=[
                        html.Div(style={'width': '25%', 'padding': '0 1rem'}, children=[
                            dcc.Dropdown(
                                id='anno-dropdown',
                                options=[{'label': anno, 'value': anno} for anno in carica_anni()],
                                placeholder="Seleziona un anno",
                                style={'width': '100%', 'marginBottom': '1em', 'fontFamily': 'Roboto, sans-serif'}
                            ),
                        ]),
                        html.Div(style={'width': '25%', 'padding': '0 1rem'}, children=[
                            dcc.Dropdown(
                                id='month-dropdown',
                                placeholder="Seleziona un mese",
                                style={'width': '100%', 'marginBottom': '1em', 'fontFamily': 'Roboto, sans-serif'},
                                value=None,
                                multi=True,
                                searchable=False
                            ),
                        ]),
                        html.Div(style={'width': '25%', 'padding': '0 1rem'}, children=[
                            dcc.Dropdown(
                                id='agente-dropdown',
                                placeholder="Seleziona un Agente",
                                style={'width': '100%', 'marginBottom': '1em', 'fontFamily': 'Roboto, sans-serif'},
                                value=None
                            ),
                        ]),
                        html.Div(style={'width': '25%', 'padding': '0 1rem'}, children=[
                            dcc.Dropdown(
                                id='origine-dropdown',
                                placeholder="Seleziona un Origine",
                                style={'width': '100%', 'marginBottom': '1em', 'fontFamily': 'Roboto, sans-serif'},
                                value=None
                            ),
                        ]),
                    ]
                ),
            ]
        ),

        # Seconda riga con il grafico a barre e il totale imponibile
        html.Div(
            style={
                'width': '100%',
                'display': 'flex',
                'flexDirection': 'row',
                'justifyContent': 'flex-start',
                'alignItems': 'flex-start',
                'padding': '1rem',
            },
            children=[
                html.Div(
                    style={'min-width': '60%', 'padding': '0.5rem'},
                    children=[
                        dcc.Graph(id='bar-chart', style={'width': '100%'}),
                    ]
                ),
                html.Div(
                    style={'width': '25%', 'padding': '0.5rem'},
                    children=[
                        html.Div(id='totale-imponibile', style={'fontSize': '2rem', 'fontWeight': 'bold'})
                    ]
                ),
            ]
        ),

        # Terza riga con i grafici a torta
        html.Div(
            style={
                'width': '100%',
                'display': 'flex',
                'flexDirection': 'row',
                'justifyContent': 'space-between',
                'padding': '1rem',  # Maggiore distanza tra le righe in altezza
            },
            children=[
                html.Div(style={'width': '50%', 'padding': '0.5rem'}, children=[
                    dcc.Graph(id='pie-chart-settori', style={'width': '100%'}),
                ]),
                html.Div(style={'width': '50%', 'padding': '0.5rem'}, children=[
                    dcc.Graph(id='pie-chart-categorie', style={'width': '100%'}),
                ]),
            ]
        ),
        
        # Quarta riga con i grafici a torta
        html.Div(
            style={
                'width': '100%',
                'display': 'flex',
                'flexDirection': 'row',
                'justifyContent': 'space-between',
                'padding': '1rem',  
            },
            children=[
                html.Div(style={'width': '50%', 'padding': '0.5rem'}, children=[
                    dcc.Graph(id='pie-chart-origine', style={'width': '100%'}),
                ]),
                html.Div(style={'width': '50%', 'padding': '0.5rem'}, children=[
                    dcc.Graph(id='pie-chart-telem', style={'width': '100%'}),
                ]),
            ]
        ),
    ]
)





server = app.server

# Avvia l'app
if __name__ == '__main__':
    app.run(debug=False)
