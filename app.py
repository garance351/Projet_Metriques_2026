import requests
from flask import Flask, jsonify, render_template
import plotly.graph_objects as go


app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Déposez votre code à partir d'ici :
@app.route("/contact")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"  

@app.get("/paris")
def api_paris():
    
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&hourly=temperature_2m"
    response = requests.get(url)
    data = response.json()

    times = data.get("hourly", {}).get("time", [])
    temps = data.get("hourly", {}).get("temperature_2m", [])

    n = min(len(times), len(temps))
    result = [
        {"datetime": times[i], "temperature_c": temps[i]}
        for i in range(n)
    ]

    return jsonify(result)

@app.route("/rapport")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme")
def histogramme():

    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&daily=temperature_2m_max&forecast_days=7&timezone=Europe/Paris"

    response = requests.get(url)
    data = response.json()

    dates = data["daily"]["time"]
    temps = data["daily"]["temperature_2m_max"]

    result = list(zip(dates, temps))

    return render_template("histogramme1.html", data=result)


@app.route("/graphique")
def atelier_dashboard():
    # --- Récupérer les données météo ItaliaMeteo ARPAE ICON-2I pour Rome ---
    latitude = 41.89
    longitude = 12.51
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,relativehumidity_2m,wind_speed_10m,precipitation_sum",
        "models": "italia_meteo_arpae_icon_2i"
    }
    data = requests.get(url, params=params).json()
    
    # Préparer les données
    hours = list(range(len(data['hourly']['temperature_2m'])))
    temp = data['hourly']['temperature_2m']
    humidity = data['hourly']['relativehumidity_2m']
    wind = data['hourly']['wind_speed_10m']
    precip = data['hourly']['precipitation_sum']
    
    # --- Radar Chart ---
    radar_fig = go.Figure()
    radar_fig.add_trace(go.Scatterpolar(
        r=[temp[0], humidity[0], wind[0], precip[0]],
        theta=['Temp (°C)','Humidité (%)','Vent (km/h)','Précipitations (mm)'],
        fill='toself',
        name='Indicateurs actuels'
    ))
    radar_fig.update_layout(polar=dict(radialaxis=dict(visible=True)))
    radar_div = radar_fig.to_html(full_html=False)
    
    # --- Gauge ---
    gauge_fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = wind[0],
        title = {'text': "Vitesse du vent (km/h)"},
        delta = {'reference': 10, 'increasing': {'color': "red"}},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "blue"},
            'steps' : [
                {'range': [0, 25], 'color': "lightgreen"},
                {'range': [25, 50], 'color': "yellow"},
                {'range': [50, 75], 'color': "orange"},
                {'range': [75, 100], 'color': "red"}],
            'threshold' : {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': wind[0]}
        }
    ))
    gauge_div = gauge_fig.to_html(full_html=False)
    
    # --- Heatmap ---
    heatmap_fig = go.Figure(data=go.Heatmap(
        z=[temp],
        x=hours,
        y=["Température (°C)"],
        colorscale='Viridis'
    ))
    heatmap_div = heatmap_fig.to_html(full_html=False)
    
    return render_template("graphique3.html",
                           radar_div=radar_div,
                           gauge_div=gauge_div,
                           heatmap_div=heatmap_div)


# Ne rien mettre après ce commentaire
    
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
