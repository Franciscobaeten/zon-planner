# Zonne-planner in de gratis cloud

Deze map bevat alles om je zonne-planner automatisch en gratis in de cloud te laten draaien,
zonder dat je eigen pc aan moet staan, en met een vaste weblink die je met je vriendin kunt delen.

**Hoe het werkt:** GitHub draait elke ochtend je `forecast_ophalen.py` (via GitHub Actions),
zet de verse `forecast_data.js` bij, en toont `index.html` op een vaste weblink (GitHub Pages).

## Wat zit erin
- `index.html` — de planner (opent in elke browser, ook op gsm)
- `forecast_ophalen.py` — haalt de voorspelling op bij Forecast.Solar
- `forecast_data.js` — de opgehaalde data (wordt automatisch ververst)
- `.github/workflows/forecast.yml` — de dagelijkse automatische taak

## Eenmalige installatie (± 15 minuten)

1. **Maak een gratis GitHub-account** op https://github.com (als je er nog geen hebt).

2. **Maak een nieuwe repository.**
   - Klik rechtsboven op **+** → **New repository**.
   - Naam bijvoorbeeld `zonne-planner`. Kies **Public** (of Private, allebei werkt gratis).
   - Klik **Create repository**.

3. **Upload deze bestanden.**
   - Klik op **Add file** → **Upload files**.
   - Sleep de inhoud van deze `cloud-planner`-map erin: `index.html`, `forecast_ophalen.py`,
     `forecast_data.js` én de map `.github` (met daarin `workflows/forecast.yml`).
   - Klik **Commit changes**.
   - Let op: de map `.github` moet mee. Lukt slepen niet, maak dan via **Add file → Create new file**
     een bestand met exact de naam `.github/workflows/forecast.yml` en plak de inhoud erin.

4. **Zet schrijfrechten voor de automatische taak aan.**
   - Ga naar **Settings** → **Actions** → **General** → onderaan **Workflow permissions**.
   - Kies **Read and write permissions** → **Save**.

5. **Zet de weblink (GitHub Pages) aan.**
   - Ga naar **Settings** → **Pages**.
   - Bij **Source** kies **Deploy from a branch**, branch **main**, map **/ (root)** → **Save**.
   - Na een minuutje verschijnt bovenaan je link, in de vorm:
     `https://<jouw-gebruikersnaam>.github.io/zonne-planner/`

6. **Test de automatische taak één keer.**
   - Ga naar de tab **Actions** → kies **Update zonne-forecast** → **Run workflow**.
   - Na ± 1 minuut is `forecast_data.js` ververst. Open daarna je Pages-link.

7. **Delen.** Stuur de Pages-link naar je vriendin; jullie kunnen hem allebei op je gsm bookmarken.

## Onderhoud
- De taak draait daarna elke ochtend vanzelf. Niets meer te doen.
- Klopt de oriëntatie niet, pas dan `AZIMUTH` bovenaan in `forecast_ophalen.py` aan
  (0 = zuid, negatief = oost, positief = west) en commit de wijziging.

## Kanttekeningen
- De gratis Forecast.Solar-laag geeft doorgaans uurresolutie; een blok van 45 min wordt naar het uur afgerond.
- De cron-tijd staat in UTC (05:00 UTC = 07:00 zomertijd, 06:00 wintertijd). Aanpasbaar in `forecast.yml`.
- Dit betreft alleen de zonne-planner. Je P1-verbruiksmeting blijft op je pc draaien,
  want de P1-meter is enkel op je thuisnetwerk bereikbaar.
