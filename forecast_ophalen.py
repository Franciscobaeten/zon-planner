"""
Forecast.Solar ophalen en wegschrijven voor de zonne-planner.

Haalt de verwachte PV-opbrengst (vandaag + morgen) op bij Forecast.Solar
en schrijft die naar forecast_data.js, dat planner.html inleest.

Gratis tier: geen API-sleutel nodig, max 12 requests/uur. 1x per dag draaien is ruim voldoende.
Doc: https://doc.forecast.solar/api:estimate
"""

import json
import os
from datetime import datetime

try:
    import requests
except ImportError:
    requests = None
import urllib.request

# --- Jouw installatie (uit EPC) -------------------------------------------
LAT = 51.05          # Gent
LON = 3.72
TILT = 10            # helling in graden
AZIMUTH = -12        # 0 = zuid, -90 = oost, +90 = west (EPC gaf ~ -12)
KWP = 3.32           # piekvermogen in kWp
# --------------------------------------------------------------------------

BASE = os.path.dirname(os.path.abspath(__file__))
URL = f"https://api.forecast.solar/estimate/{LAT}/{LON}/{TILT}/{AZIMUTH}/{KWP}"


def haal_forecast():
    """Haal de JSON op bij Forecast.Solar (met requests, val terug op urllib)."""
    if requests is not None:
        r = requests.get(URL, timeout=15)
        r.raise_for_status()
        return r.json()
    with urllib.request.urlopen(URL, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def verwerk(data):
    """Groepeer de 'watts'-reeks per dag tot labels + waarden."""
    result = data["result"]
    watts = result["watts"]                 # { "YYYY-MM-DD HH:MM:SS": vermogen_W }
    wh_day = result.get("watt_hours_day", {})  # { "YYYY-MM-DD": energie_Wh }

    per_dag = {}
    for tijd, vermogen in sorted(watts.items()):
        datum, klok = tijd.split(" ")
        hhmm = klok[:5]
        per_dag.setdefault(datum, {"labels": [], "watts": []})
        per_dag[datum]["labels"].append(hhmm)
        per_dag[datum]["watts"].append(int(round(vermogen)))

    dagen = []
    vandaag = datetime.now().strftime("%Y-%m-%d")
    for datum in sorted(per_dag):
        d = per_dag[datum]
        naam = "Vandaag" if datum == vandaag else ("Morgen" if datum > vandaag else datum)
        dagen.append({
            "naam": f"{naam} ({datum})",
            "datum": datum,
            "wattpiek": max(d["watts"]) if d["watts"] else 0,
            "kwh": round(wh_day.get(datum, 0) / 1000, 1),
            "labels": d["labels"],
            "watts": d["watts"],
        })
    return dagen[:2]  # vandaag + morgen


def schrijf(dagen):
    payload = {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "days": dagen,
    }
    pad = os.path.join(BASE, "forecast_data.js")
    with open(pad, "w", encoding="utf-8") as f:
        f.write("// Automatisch gegenereerd door forecast_ophalen.py — niet handmatig aanpassen\n")
        f.write("const FORECAST = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n")
    print(f"forecast_data.js bijgewerkt: {len(dagen)} dag(en), {datetime.now():%Y-%m-%d %H:%M}")


if __name__ == "__main__":
    try:
        data = haal_forecast()
        dagen = verwerk(data)
        if not dagen:
            raise ValueError("Geen dagen in respons — controleer de API-uitvoer.")
        schrijf(dagen)
    except Exception as e:
        # Fout niet fataal laten zijn voor de rest van je automatisering
        print(f"[forecast_ophalen] FOUT: {e}")
