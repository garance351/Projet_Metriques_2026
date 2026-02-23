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

@app.route('/atelier')
def atelier():
    # Coordonnées de Marseille
    latitude = 43.2965
    longitude = 5.3698

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "wind_speed_10m,wind_direction_10m,relativehumidity_2m,precipitation_sum,temperature_2m",
        "timezone": "Europe/Paris"
    }
    response = requests.get(url, params=params)
    data = response.json()
    hourly = data.get('hourly', {})

    if not hourly:
        return "Erreur: données météo indisponibles", 500

    # Récupération des premières valeurs pour indicateurs actuels
    wind = hourly.get("wind_speed_10m", [0])[0]
    wind_dir = hourly.get("wind_direction_10m", [0])[0]
    humidity = hourly.get("relativehumidity_2m", [0])[0]
    precip = hourly.get("precipitation_sum", [0])[0]
    temp = hourly.get("temperature_2m", [0])[0]

    # Sparkline : normaliser 24 dernières températures pour barre miniature
    temps_24h = hourly.get("temperature_2m", [])[:24]
    max_temp = max(temps_24h) if temps_24h else 1
    sparkline = [int((t / max_temp) * 50) for t in temps_24h]  # hauteur max 50px

    indicators = {
        "wind": wind,
        "wind_dir": wind_dir,
        "humidity": humidity,
        "precip": precip,
        "temp": temp,
        "sparkline": sparkline
    }

    return render_template('atelier.html', indicators=indicators)


# Ne rien mettre après ce commentaire
    
if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
