import streamlit as st
import requests
import pandas as pd
pip install plotly
import plotly.express as px
import plost
from main import run_main
st.set_page_config(
    page_title="Blondin",
    layout="wide"
)

st.title("Tableau de bord")
run_main()
response = requests.get("http://127.0.0.1:8000/jointure")
base=response.json()
base=pd.DataFrame(base)
base=base.replace("-",pd.NA)

base['timestamp'] = pd.to_datetime(base['timestamp'], unit="s")
base['timestamp_x'] = pd.to_datetime(base['timestamp_x'], unit="s")
base['timestamp_y'] = pd.to_datetime(base['timestamp_y'], unit="s")

date_min = base['timestamp_x'].min().date()
date_max = base['timestamp'].max().date()

date_debut, date_fin = st.slider("Sélectionner la période de temps", min_value=date_min, max_value=date_max, value=(date_min, date_max))

# Filtrer le DataFrame en fonction de l'intervalle de dates sélectionné
base_filtre = base[(base["timestamp_x"] >= pd.to_datetime(date_debut)) & (base["timestamp_x"] <= pd.to_datetime(date_fin))]

counts = base_filtre["gender"].value_counts()
women=round((counts['f']/base_filtre['gender'].count())*100,ndigits=2)

cadre1, cadre2, cadre3 = st.columns(3)

cadre1.metric(
    label="Chiffre d'affaires",
    value=f"{base_filtre['price'].sum()} €"
)

cadre2.metric(
    label="Nombre de produits vendus",
    value=base_filtre['timestamp'].count()
)


cadre3.metric(
    label="Femmes",
    value=f"{women} %"
)


total1 = base_filtre['timestamp'].count()
total2 = base_filtre['timestamp_y'].count()
total3 = base_filtre['timestamp_x'].count()



tot = {'Variables': ['Impressions', 'Clics', 'Achats'],
        'Total': [total3, total2, total1]}
df_totals = pd.DataFrame(tot)

# Tracer l'histogramme empilé des totaux

fig1, fig2 = st.columns(2)

with fig1:
    st.markdown("### Age en fonction du produit")
    fig_1 = px.box(y='age', x='product_id', data_frame=base_filtre)
    st.write(fig_1)

with fig2:
    st.markdown("### impressions, clics et achats")
    fig_2 = px.histogram(df_totals, x='Variables', y='Total', text_auto='Total')

    st.write(fig_2)


prods = base_filtre['product_id'].value_counts()
freqs = prods / len(base_filtre['product_id']) * 100

# Création du DataFrame avec les modalités et les pourcentages
freqs = pd.DataFrame({'produits': freqs.index, 'Pourcentage': freqs})
st.markdown("### Produits")
plost.donut_chart(data=freqs, theta='Pourcentage' , color='produits', legend='bottom', use_container_width=True)
