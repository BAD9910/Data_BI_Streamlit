import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk

# Créez la barre latérale
st.sidebar.title("Coordonnées")

# Ajoutez un lien mailto à la barre latérale
st.sidebar.markdown(
    """
    Pour me contacter par e-mail, [cliquez ici](mailto:adoumboukayode@gmail.com)
    """
)

# Ajoutez un lien vers votre profil LinkedIn
st.sidebar.markdown(
    """
    Pour voir mon profil LinkedIn, [cliquez ici](https://www.linkedin.com/in/your_username)
    """
)

# Charger les données
st.title("Analyse des données Uber - Avril 2014")
st.write("Visualisation interactive des données Uber pour Avril 2014.")
df = pd.read_csv("uber-raw-data-apr14.csv", delimiter = ',')

df['Date/Time'] = pd.to_datetime(df['Date/Time'], format = '%m/%d/%Y %H:%M:%S')

df['day'] = df['Date/Time'].dt.day
df['weekday'] = df['Date/Time'].dt.weekday
df['dayhour'] = df['Date/Time'].dt.hour

# Graphiques
## Histogramme par jour du mois
st.subheader("Histogramme des trajets par jour du mois")
hist_data = px.histogram(df, x="day", nbins=30, title="Histogramme des trajets par jour du mois")
st.plotly_chart(hist_data)

## Diagramme en barres par jour du mois
st.subheader("Diagramme en barres des trajets par jour du mois")
bar_data = df['day'].value_counts().sort_index()
bar_chart = px.bar(bar_data, x=bar_data.index, y='day', labels={'x': 'Jour du mois', 'y': 'Nombre de trajets'})
st.plotly_chart(bar_chart)

## Histogramme par jour de la semaine
st.subheader("Histogramme des trajets par jour de la semaine")
week_hist = px.histogram(df, x="weekday", nbins=7, title="Histogramme des trajets par jour de la semaine")
week_hist.update_xaxes(ticktext=['Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche', 'Lundi'],
                       tickvals=list(range(7)))
st.plotly_chart(week_hist)

## Heatmap par jour de la semaine et heure
st.subheader("Heatmap des trajets par jour de la semaine et heure")
df2 = df.groupby(['weekday', 'dayhour']).size().reset_index(name='count')
heatmap_data = px.density_heatmap(df2, x='dayhour', y='weekday', z='count', nbinsx=24, nbinsy=7,
                                  title="Heatmap des trajets par jour de la semaine et heure")
heatmap_data.update_yaxes(ticktext=['Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche', 'Lundi'],
                          tickvals=list(range(7)))
st.plotly_chart(heatmap_data)

## Scatter plot latitude et longitude
st.subheader("Scatter plot des trajets par latitude et longitude")
scatter_data = px.scatter(df, x='Lat', y='Lon', color='weekday', title="Scatter plot des trajets par latitude et longitude",
                          color_continuous_scale=px.colors.qualitative.Pastel)
st.plotly_chart(scatter_data)

## Carte des trajets
st.subheader("Carte des trajets")
points = pdk.Layer("ScatterplotLayer",
                   df,
                   pickable=True,
                   opacity=0.3,
                   stroked=True,
                   filled=True,
                   radius_scale=10,
                   radius_min_pixels=5,
                   radius_max_pixels=50,
                   line_width_min_pixels=1,
                   get_position=["Lon", "Lat"],
                   get_radius=10,
                   get_fill_color=[255, 0, 0],
                   get_line_color=[0, 0, 0])

view_state = pdk.ViewState(latitude=df["Lat"].mean(), longitude=df["Lon"].mean(), zoom=10, pitch=0, bearing=0)

r = pdk.Deck(layers=[points], initial_view_state=view_state, map_style="mapbox://styles/mapbox/light-v9", tooltip={"text": "Lat: {Lat}\nLon: {Lon}"})

st.pydeck_chart(r)

# Exécutez l'application Streamlit
# Vous pouvez exécuter cette application en enregistrant le code dans un fichier Python (par exemple, app.py)
# et en exécutant la commande suivante dans votre terminal ou invite de commande :
# streamlit run app.py
