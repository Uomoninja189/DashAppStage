import pandas as pd
import dash
import plotly.express as px
from funzioni import *

app = dash.Dash(__name__)

########    CALLBACK SELEZIONE ANNO     ########
#serve a raccogliere i mesi 
@app.callback(
    Output('month-dropdown', 'options'),
    Output('month-dropdown', 'value'),
    Input('anno-dropdown', 'value')
)
def aggiorna_mesi(anno):

    if not anno:
        return [], None
    
    file_path = f'OrdiniAgenti{anno}.xlsx'
    data = pd.ExcelFile(file_path)
    
    #Raccolta nomi dei mesi dai fogli
    mesi = data.sheet_names
    month_options = [{'label': m, 'value': m} for m in mesi]
    month_value = None  


    return month_options, month_value





########    CALLBACK SELEZIONE MESE     ########
#serve a aggiornare i grafici (mese input facoltativo così da vedere i dati sull'anno) 
@app.callback(
    Output('bar-chart', 'figure'),
    Output('pie-chart-settori', 'figure'),
    Output('pie-chart-categorie', 'figure'),
    Output('pie-chart-origine', 'figure'),
    Output('pie-chart-telem', 'figure'),
    Output('totale-imponibile', 'children'),
    Output('agente-dropdown', 'options'),
    Output('agente-dropdown', 'value'),
    Output('origine-dropdown', 'options'),
    Output('origine-dropdown', 'value'),
    Input('anno-dropdown', 'value'),
    [Input('month-dropdown', 'value')],
    [Input('agente-dropdown', 'value')],
    [Input('origine-dropdown', 'value')]
)
def update_grafici(anno, mesi, agente, origine):
    if not anno:
        return {}, {}, {}, {}, {}, "", [], None, [], None

    file_path = f'OrdiniAgenti{anno}.xlsx'

   
    if mesi:
        df_list = []
        for sh in mesi:
            df = pd.read_excel(file_path, sheet_name=sh, header=2)
            df_list.append(df)
        data = pd.concat(df_list, ignore_index=True)

        if len(mesi) == 1:
            titolo = f"{mesi[0]} {anno}"
           
        else:
            mesi_str = ", ".join(mesi)
            titolo = f"{mesi_str} {anno}"
    
    else:
        # TUTTO L'ANNO
        xls = pd.ExcelFile(file_path)
        df_list = []
        for sh in xls.sheet_names:
            df = pd.read_excel(file_path, sheet_name=sh, header=2)
            df_list.append(df)
        data = pd.concat(df_list, ignore_index=True)
        titolo = f"Anno {anno}"

    
    data=pulisci_data(data)


    agenti = data['AGENTE'].unique()  
    agente_options = [{'label': agente, 'value': agente} for agente in agenti]
    if(agente):
        data=filtro_agente(agente, data)
        val_agente=agente
    else:
        val_agente=None
    
  
    origini = data['Origine'].unique()  
    origine_options = [{'label': origine, 'value': origine} for origine in origini]
    if(origine):
        data=filtro_origine(origine, data)
        val_origine=origine
    else:
        val_origine=None


    #colonna tipo, per le vendite effettuate o meno
    data=aggiungi_colonna_tipo(data)
    

    if not agente:
        fig0= crea_barre(data,'AGENTE', 'IMPONIBILE', f'Imponibile per agente {titolo}')  
    else:
        datam=riordina_per_mese(data)
        fig0 = crea_barre(datam,'Mese', 'IMPONIBILE', f'Imponibile per mese {agente} {titolo}')
          


    data = data[(data['Tipo'] == 'Effettuata') | (data['Tipo'] == 'Altro')]#non mi interessa più il saltato

    
    

    fig1=crea_torta(data,'SETTORE ','IMPONIBILE')


    
    fig2 = px.sunburst(
        data,
        path=['CATEGORIA', 'MOD'],
        values='IMPONIBILE',
        title=f'Distribuzione Percentuale per Categoria e Prodotto'
    )
    fig2.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>" +
            "Imponibile: %{value:,.2f} €<br>" +
            "Percentuale: %{percentRoot:.2%}<br>" +
            "<extra></extra>"
            ),

    )
    
    
    
    fig3=crea_torta(data,'Origine','IMPONIBILE')
    
    if 'Nome' in data.columns:
        aux = data.dropna(subset=['Nome'])
        

        # Funzione per creare il grafico (assicurati che 'crea_torta' esista nella tua libreria funzioni)
        fig4 = crea_torta(aux, 'Nome', 'IMPONIBILE')
        fig4.update_layout(title=f'Distribuzione Percentuale per Telemarketing')
    else:
        fig4={}
    
    totale=data['IMPONIBILE'].sum()
    totale_str = f"{totale:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

    contenuto = html.Div([
         html.Div(
            f"Totale Imponibile {titolo}:",
            style={
                'fontSize': '1.5rem',
                'fontWeight': 'bold',
                'marginBottom': '0.3rem',
                'color': '#34495e',
                'fontFamily': 'Roboto, sans-serif'  # Un grigio più scuro per il testo
            }
        ),
        html.Div(
            totale_str,
            style={
                'fontSize': '2rem',
                'fontWeight': 'bold',
                'color': '#27ae60',  # Colore verde per l'importo
                'marginBottom': '0.3rem',
                'fontFamily': 'Roboto, sans-serif'
            }
        )
    ])

    
    return fig0, fig1, fig2, fig3, fig4, contenuto, agente_options, val_agente, origine_options, val_origine
