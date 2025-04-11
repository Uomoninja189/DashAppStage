import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import os
import re



def carica_anni():
    folder = './'  

    excel_files = [f for f in os.listdir(folder) if re.match(r'OrdiniAgenti\d{4}\.xlsx', f)]

    anni = sorted([re.search(r'\d{4}', f).group() for f in excel_files])

    return anni



def raggruppa_altro(data, nomi, disc, soglia_percentuale=3, pie=True):#non funziona, SERVE?
    totale=data[disc].sum()
    percentuali = (data[disc] / totale) * 100
    sottosoglia = data[percentuali < soglia_percentuale]
    if sottosoglia.shape[0] <2:
        return data
    data['Root'] = ['Altro' if p < soglia_percentuale else 'Root' for p in percentuali]
    altro = pd.DataFrame({
        disc: 0, 
        'Root': ['Root'],
        nomi: 'Altro'
    })
    data = pd.concat([data, altro], ignore_index=True)
    return data
    


def filtro_agente(nomeAgente, data):
    data=data[data['AGENTE'] == nomeAgente]
    return data

def filtro_settore(nomeSettore, data):
    data=data[data['SETTORE ']==nomeSettore]
    return data

def filtro_origine(nomeOrigine, data):
    data=data[data['Origine']==nomeOrigine]
    return data


def pulisci_data(data):

    data=data.replace(r'^\s*$', pd.NA, regex=True)
    

    data = data[~data.iloc[:, 1:].isna().all(axis=1)]

    for col in data.select_dtypes(include=['object', 'category']).columns:
        data[col] = data[col].apply(lambda x: str(x).strip().lower().capitalize() if pd.notna(x) else x)


    data = data.rename(columns={'?': 'Origine'})
    data=riempi_vuoti(data)
    data['MOD']=data['MOD'].str.upper()
    data['Origine'] = data['Origine'].str.upper()
    return data

def riempi_vuoti(data):
    data[['SETTORE ', 'MOD', 'AGENTE','Origine']] = data[['SETTORE ', 'MOD', 'AGENTE','Origine']].fillna("Sconosciuto")
    data['CATEGORIA']=data['CATEGORIA'].fillna('Acc')
    data['Q.'] = pd.to_numeric(data['Q.'], errors='coerce')  # DA CONTROLLARE SE IGNORA DATI
    data['Q.'] = data['Q.'].fillna(1)   
    return data

def aggiungi_colonna_tipo(data):
    data['Tipo'] = data.apply(
        lambda row: 
            'Effettuata' if str(row['FT. ']).startswith(('F', 'f')) 
            else 'Saltata' if str(row['FT. ']).strip().lower() == 'saltata' 
            else 'Altro', 
        axis=1
    )

    data['Tipo'] = data.apply(lambda row: 'Saltata' if str(row['NOTE']).startswith('saltata') else row['Tipo'], axis=1)
    order = ['Effettuata', 'Altro', 'Saltata']
    data['Tipo'] = pd.Categorical(data['Tipo'], categories=order, ordered=True)

    return data

def riordina_per_mese(data):
    
    mesi_dict = {
        1: 'Gennaio', 2: 'Febbraio', 3: 'Marzo', 4: 'Aprile',
        5: 'Maggio', 6: 'Giugno', 7: 'Luglio', 8: 'Agosto',
        9: 'Settembre', 10: 'Ottobre', 11: 'Novembre', 12: 'Dicembre'
    }
    mesi_presenti = sorted(data['DATA '].dt.month.unique())
    data['Mese']=data['DATA '].dt.month.map(mesi_dict)
    ordine_mesi_presenti = [mesi_dict[m] for m in mesi_presenti]
    data['Mese'] = pd.Categorical(data['Mese'], categories=ordine_mesi_presenti, ordered=True)

    return data

def crea_torta(data, group, disc):
    
    data= data.groupby([group], as_index=True).agg({
            disc: 'sum',
            'Q.': 'sum'
        }).rename(columns={'Q.': 'N° vendite'})
    
    
    return px.pie(data, 
                names=data.index,
                values=disc, 
                title=f'Distribuzione Percentuale per {group}',
                hole=.3,
                hover_data=["N° vendite"],
                hover_name=data.index
    )

def crea_barre(data, x, y, title):
    data = data.groupby([x, 'Tipo'], as_index=False)['IMPONIBILE'].sum()
    fig=px.bar(data, 
                x=x, 
                y=y, 
                color='Tipo',  # Differenza tra vendite saltate e non saltate
                title=title,
                labels={'IMPONIBILE': 'Imponibile', 'AGENTE': 'Agente'},
                color_discrete_map={'Effettuata': '#2ecc71',  'Saltata': '#e74c3c',   'Altro': '#3498db'  } 
                )

    #per impilare le barre
    fig.update_layout(
        barmode='stack')
    return fig