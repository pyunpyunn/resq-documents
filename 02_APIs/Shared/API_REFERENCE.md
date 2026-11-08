# ResQperation — API Reference
> Free & Open Source APIs for Mapping and Weather
> Last updated: May 2025

---

## Table of Contents
1. [Mapping Stack](#1-mapping-stack)
2. [Routing — Evacuation Routes](#2-routing--evacuation-routes)
3. [Team Live Tracking](#3-team-live-tracking)
4. [Weather — Open-Meteo](#4-weather--open-meteo)
5. [Weather — PAGASA Official](#5-weather--pagasa-official)
6. [Quick Reference Table](#6-quick-reference-table)
7. [Integration Strategy](#7-integration-strategy)

---

## 1. Mapping Stack

### Leaflet + OpenStreetMap + OpenFreeMap

**What it does:** Renders the interactive map, household dots, zoom/pan, layer toggles.

**Cost:** Completely free. No API key. No account. No billing ever.

**Install:**
```bash
npm install leaflet react-leaflet
```

**Tile server (use OpenFreeMap — no key, no rate limits):**
```
https://tiles.openfreemap.org/styles/liberty/{z}/{x}/{y}.png
```

**Or use standard OpenStreetMap tiles:**
```
https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png
```

**Basic React setup:**
```jsx
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

function MapView({ households }) {
  return (
    <MapContainer
      center={[10.3157, 123.8854]}  // your barangay coordinates
      zoom={16}
      style={{ height: '100%', width: '100%' }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />

      {households.map((hh) => (
        <CircleMarker
          key={hh.id}
          center={[hh.lat, hh.lng]}
          radius={4}                     // keep small — 500+ households
          fillColor={getStatusColor(hh.status)}
          color={getStatusColor(hh.status)}
          fillOpacity={0.9}
          weight={1}
        >
          <Popup>
            <strong>{hh.household_code}</strong><br />
            {hh.head_name}<br />
            Status: {hh.status ?? 'Unchecked'}
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
}

// Color logic — matches prototype exactly
function getStatusColor(status) {
  switch (status) {
    case 'safe':      return '#16a34a';  // green
    case 'evacuated': return '#2563eb';  // blue
    case 'unsafe':    return '#dc2626';  // red
    default:          return '#94a3b8';  // gray = unchecked
  }
}
```

**Zoom levels for puroks:** Set zoom to 16–18 for street/purok level detail. OSM has full coverage of Philippine municipalities.

**Docs:** https://leafletjs.com | https://react-leaflet.js.org | https://openfreemap.org

---

## 2. Routing — Evacuation Routes

### OpenRouteService (ORS)

**What it does:** Draws routes from EOC/rescue teams to evacuation centers on the map.
Built specifically for disaster management — routing graphs are recalculated every hour during disaster events.

**Cost:** Free — 2,000 requests/day on the free tier.

**API Key:** Required. Get a free key at https://openrouteservice.org (sign up, go to Dashboard → Request a Token).

**Store your key in `.env` — never hardcode it:**
```env
# web/.env
VITE_ORS_API_KEY=REDACTED
```

**Draw a route between two points:**
```javascript
// src/api/routing.js

const ORS_KEY = import.meta.env.VITE_ORS_API_KEY;

export async function getRoute(fromCoords, toCoords) {
  // fromCoords and toCoords = [longitude, latitude] (ORS uses lng,lat order)
  const response = await fetch(
    'https://api.openrouteservice.org/v2/directions/driving-car/geojson',
    {
      method: 'POST',
      headers: {
        'Authorization': ORS_KEY,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        coordinates: [fromCoords, toCoords],
      }),
    }
  );
  const data = await response.json();
  return data; // GeoJSON — pass directly to react-leaflet GeoJSON component
}
```

**Render the route on the map:**
```jsx
import { GeoJSON } from 'react-leaflet';
import { getRoute } from '../api/routing';

// Inside your MapView component:
const [route, setRoute] = useState(null);

async function showRouteToEvacCenter(evacCenter) {
  const eocCoords    = [123.8854, 10.3157]; // [lng, lat] — your EOC
  const evacCoords   = [evacCenter.lng, evacCenter.lat];
  const routeData    = await getRoute(eocCoords, evacCoords);
  setRoute(routeData);
}

// In your JSX:
{route && (
  <GeoJSON
    data={route}
    style={{ color: '#ea580c', weight: 4, dashArray: '8 4' }}
  />
)}
```

**Rate limit:** 2,000 route requests per day on the free plan.
For a capstone/barangay-level system this is far more than enough.

**Docs:** https://openrouteservice.org/dev/#/api-docs

---

## 3. Team Live Tracking

**No external API needed.** Your own Laravel back end handles this.

Every rescuer mobile device sends its GPS coordinates to your API every 30 seconds.
The dashboard fetches those coordinates and updates the team markers on the Leaflet map.

**Add a `lat` and `lng` column to `resq_dispatches`:**
```sql
ALTER TABLE resq_dispatches
  ADD COLUMN current_lat DECIMAL(10,7) NULL,
  ADD COLUMN current_lng DECIMAL(10,7) NULL,
  ADD COLUMN location_updated_at TIMESTAMP NULL;
```

**Laravel route:**
```php
// routes/api.php
Route::patch('/dispatches/{id}/location', [DispatchController::class, 'updateLocation'])
    ->middleware(['auth:sanctum', 'role:rescuer']);
```

**Laravel controller method:**
```php
// In DispatchController.php
public function updateLocation(Request $request, $id)
{
    $request->validate([
        'lat' => 'required|numeric|between:-90,90',
        'lng' => 'required|numeric|between:-180,180',
    ]);

    $dispatch = Dispatch::findOrFail($id);
    $dispatch->update([
        'current_lat'          => $request->lat,
        'current_lng'          => $request->lng,
        'location_updated_at'  => now(),
    ]);

    return response()->json(['message' => 'Location updated']);
}
```

**Mobile (React Native) — send location every 30 seconds:**
```javascript
// Inside rescuer dispatch screen
import * as Location from 'expo-location';
import api from '../api/axios';

useEffect(() => {
  const interval = setInterval(async () => {
    const location = await Location.getCurrentPositionAsync({});
    await api.patch(`/dispatches/${dispatchId}/location`, {
      lat: location.coords.latitude,
      lng: location.coords.longitude,
    });
  }, 30000); // every 30 seconds

  return () => clearInterval(interval); // cleanup on unmount
}, []);
```

**Web dashboard — poll for team positions every 30 seconds:**
```javascript
// Inside MapView.jsx
useEffect(() => {
  const interval = setInterval(async () => {
    const res = await api.get('/dispatches');
    setTeamPositions(res.data);
  }, 30000);

  return () => clearInterval(interval);
}, []);
```

---

## 4. Weather — Open-Meteo

### Current conditions + forecast

**What it does:** Current temperature, humidity, wind speed, rain probability,
weather condition codes, hourly and 16-day forecast.

**Cost:** Free up to 10,000 requests/day. No API key. No sign-up. No account needed.

**Call it directly from React — no back end needed:**
```javascript
// src/api/weather.js

const BARANGAY_LAT = 10.3157;  // replace with your actual barangay coordinates
const BARANGAY_LNG = 123.8854;

export async function getCurrentWeather() {
  const url = new URL('https://api.open-meteo.com/v1/forecast');
  url.searchParams.set('latitude',  BARANGAY_LAT);
  url.searchParams.set('longitude', BARANGAY_LNG);
  url.searchParams.set('timezone',  'Asia/Manila');
  url.searchParams.set('current', [
    'temperature_2m',
    'relative_humidity_2m',
    'apparent_temperature',
    'precipitation',
    'weathercode',
    'wind_speed_10m',
    'wind_direction_10m',
  ].join(','));
  url.searchParams.set('hourly', [
    'precipitation_probability',
    'temperature_2m',
  ].join(','));
  url.searchParams.set('daily', [
    'weathercode',
    'temperature_2m_max',
    'temperature_2m_min',
    'precipitation_sum',
    'precipitation_probability_max',
  ].join(','));
  url.searchParams.set('forecast_days', '7');

  const res = await fetch(url.toString());
  return res.json();
}
```

**Use it in the Weather page:**
```jsx
// src/pages/Weather.jsx
import { useEffect, useState } from 'react';
import { getCurrentWeather, getWeatherLabel, getWeatherIcon } from '../api/weather';

export default function Weather() {
  const [weather, setWeather] = useState(null);

  useEffect(() => {
    getCurrentWeather().then(setWeather);
  }, []);

  if (!weather) return <div>Loading weather...</div>;

  const c = weather.current;

  return (
    <div>
      <h2>{getWeatherLabel(c.weathercode)}</h2>
      <p>Temperature: {c.temperature_2m}°C (feels like {c.apparent_temperature}°C)</p>
      <p>Humidity: {c.relative_humidity_2m}%</p>
      <p>Wind: {c.wind_speed_10m} km/h</p>
      <p>Rainfall: {c.precipitation} mm</p>
    </div>
  );
}
```

**Weather code to label mapping (WMO standard):**
```javascript
// src/api/weather.js — add this function

export function getWeatherLabel(code) {
  const labels = {
    0:  'Clear sky',
    1:  'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast',
    45: 'Fog',          48: 'Icy fog',
    51: 'Light drizzle', 53: 'Moderate drizzle', 55: 'Dense drizzle',
    61: 'Slight rain',   63: 'Moderate rain',    65: 'Heavy rain',
    71: 'Slight snow',   73: 'Moderate snow',    75: 'Heavy snow',
    80: 'Slight showers', 81: 'Moderate showers', 82: 'Violent showers',
    95: 'Thunderstorm',
    96: 'Thunderstorm with hail', 99: 'Thunderstorm with heavy hail',
  };
  return labels[code] ?? 'Unknown';
}

export function getWeatherIcon(code) {
  if (code === 0)                    return '☀️';
  if (code <= 3)                     return '⛅';
  if (code <= 48)                    return '🌫️';
  if (code <= 67)                    return '🌧️';
  if (code <= 77)                    return '❄️';
  if (code <= 82)                    return '🌦️';
  if (code >= 95)                    return '⛈️';
  return '🌤️';
}
```

**Docs:** https://open-meteo.com/en/docs

---

## 5. Weather — PAGASA Official

### Two options — use both together

---

### Option A: PAGASA RSS Feed (zero setup, works immediately)

**What it does:** Official PAGASA weather bulletins, typhoon advisories, agri-weather forecasts.
Exactly what you see on the PAGASA website — but in machine-readable XML format.

**Cost:** Free. No account. No key. No registration.

**PAGASA RSS feed URLs:**
```
Weather Bulletin:       https://www1.pagasa.dost.gov.ph/rss/weather-forecast
Tropical Cyclone:       https://www1.pagasa.dost.gov.ph/rss/tropical-cyclone
Rainfall Advisory:      https://www1.pagasa.dost.gov.ph/rss/rainfall-advisory
Agri-weather Forecast:  https://www1.pagasa.dost.gov.ph/rss/agri-weather
```

**How to use it — Laravel scheduled command (runs every 30 minutes):**
```php
// app/Console/Commands/FetchPagasaFeed.php

<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Http;

class FetchPagasaFeed extends Command
{
    protected $signature   = 'pagasa:fetch';
    protected $description = 'Fetch latest PAGASA weather advisories from RSS feed';

    public function handle()
    {
        $feedUrl = 'https://www1.pagasa.dost.gov.ph/rss/weather-forecast';

        try {
            $response = Http::timeout(10)->get($feedUrl);

            if ($response->failed()) {
                $this->error('Failed to fetch PAGASA feed');
                return;
            }

            // Parse the XML
            $xml   = simplexml_load_string($response->body());
            $items = [];

            foreach ($xml->channel->item as $item) {
                $items[] = [
                    'title'       => (string) $item->title,
                    'description' => strip_tags((string) $item->description),
                    'pub_date'    => (string) $item->pubDate,
                    'link'        => (string) $item->link,
                ];
            }

            // Cache for 30 minutes
            Cache::put('pagasa_advisories', $items, now()->addMinutes(30));

            $this->info('PAGASA feed updated: ' . count($items) . ' items cached');

        } catch (\Exception $e) {
            $this->error('Error: ' . $e->getMessage());
        }
    }
}
```

**Schedule it in `routes/console.php` (Laravel 12):**
```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('pagasa:fetch')->everyThirtyMinutes();
```

**API endpoint to serve it to the front end:**
```php
// In a WeatherController.php
public function pagasaAdvisories()
{
    $advisories = Cache::get('pagasa_advisories', []);
    return response()->json($advisories);
}
```

---

### Option B: PAGASA TenDay Official API (requires free registration)

**What it does:** Official per-municipality 10-day weather forecast directly from PAGASA servers.
Filterable by municipality, city, or province.

**Cost:** Free. Requires a token from PAGASA.

**API base URL:**
```
https://tenday.pagasa.dost.gov.ph/api/v1
```

**Get your token:REDACTED Register at https://tenday.pagasa.dost.gov.ph — create an account and request a developer token.

**Get current weather for your municipality:**
```
GET https://tenday.pagasa.dost.gov.ph/api/v1/tenday/current
    ?municipality=YOUR_MUNICIPALITY
    &token=REDACTED
```

**Get full 10-day forecast:**
```
GET https://tenday.pagasa.dost.gov.ph/api/v1/tenday/full
    ?municipality=YOUR_MUNICIPALITY
    &token=REDACTED
```

**Store the token in your back end `.env` only — never expose it to the front end:**
```env
# backend/.env
PAGASA_API_TOKEN=REDACTED
```

**Laravel controller method:**
```php
public function pagasaForecast()
{
    $response = Http::get('https://tenday.pagasa.dost.gov.ph/api/v1/tenday/current', [
        'municipality' => 'YOUR_MUNICIPALITY_NAME',
        'token'        =REDACTED env('PAGASA_API_TOKEN'),
    ]);

    return response()->json($response->json());
}
```

> **Note for capstone:** If you cannot get the PAGASA TenDay token in time for your defense,
> Open-Meteo alone (Option 4 above) is fully sufficient to demonstrate the weather feature.
> Use both once the token is available.

---

### Option C: PANaHON (PAGASA real-time station data)

**What it does:** Near real-time rainfall, temperature, humidity, wind from PAGASA
weather stations nationwide. Updated continuously.

**URL:** https://www.panahon.gov.ph

This is a public-facing map system. It does not have a documented public API yet,
but station data can be observed from network requests on the PANaHON website.
Use it as a visual reference and cross-check for your weather display.

---

## 6. Quick Reference Table

| Feature | API / Service | Cost | API Key | Docs |
|---|---|---|---|---|
| Map tiles | OpenStreetMap via OpenFreeMap | Free | ❌ None | openfreemap.org |
| Zoom, dots, layers | Leaflet + react-leaflet | Free | ❌ None | leafletjs.com |
| Evacuation routing | OpenRouteService (ORS) | Free (2k req/day) | ✅ Free signup | openrouteservice.org |
| Team live location | Your Laravel API | Free | ❌ N/A | internal |
| Current weather + forecast | Open-Meteo | Free (10k req/day) | ❌ None | open-meteo.com |
| PAGASA advisories (RSS) | PAGASA RSS Feed | Free | ❌ None | pagasa.dost.gov.ph |
| Per-municipality forecast | PAGASA TenDay API | Free | ✅ Free registration | tenday.pagasa.dost.gov.ph |
| Real-time station data | PANaHON (PAGASA) | Free | ❌ None | panahon.gov.ph |

---

## 7. Integration Strategy

### How all three sources work together in the Weather page

```
Open-Meteo (auto, no key)
  → fetched directly from React every 60 minutes
  → displays: current temperature, humidity, wind, condition icon,
               hourly rain probability, 7-day forecast

PAGASA RSS Feed (fetched by Laravel every 30 minutes)
  → stored in Laravel Cache
  → served via GET /api/weather/pagasa-advisories
  → displays: official PAGASA bulletin text, typhoon advisories,
               rainfall warnings — in the language PAGASA uses

PAGASA TenDay API (fetched by Laravel every 12 hours)
  → stored in database or cache
  → served via GET /api/weather/forecast
  → displays: 10-day per-municipality forecast from official PAGASA data
```

### How all layers work together in the Mapping page

```
Leaflet + OpenStreetMap
  → base map, zoom, pan, purok-level detail

Household dots (your Laravel API)
  → GET /api/households/map-points
  → returns [{ id, lat, lng, status }] only — small payload
  → rendered as CircleMarker, radius 4, color by status
  → polled every 30 seconds for live updates

Evacuation site markers (your Laravel API)
  → stored in resq_evacuation_sites table (add this table)
  → rendered as blue rectangle Marker with popup showing capacity

Rescue team markers (your Laravel API)
  → GET /api/dispatches (includes current_lat, current_lng)
  → rendered as colored Marker per team
  → polled every 30 seconds

Evacuation routes (OpenRouteService)
  → called once when HQ clicks "Show route to Evac Site A"
  → rendered as orange dashed Polyline
  → only called on demand, not on every load (saves daily quota)
```

### Layer toggle implementation

```jsx
// Layer visibility state in MapView.jsx
const [layers, setLayers] = useState({
  households:     true,
  evacSites:      true,
  teams:          true,
  routes:         false,  // off by default — only shown on demand
});

// Toggle a layer
function toggleLayer(name) {
  setLayers(prev => ({ ...prev, [name]: !prev[name] }));
}

// Conditional rendering
{layers.households && households.map(hh => (
  <CircleMarker key={hh.id} center={[hh.lat, hh.lng]} ... />
))}

{layers.evacSites && evacSites.map(site => (
  <Marker key={site.id} position={[site.lat, site.lng]} ... />
))}

{layers.teams && teams.map(team => (
  team.current_lat && <Marker key={team.id} position={[team.current_lat, team.current_lng]} ... />
))}

{layers.routes && activeRoute && (
  <GeoJSON data={activeRoute} style={{ color: '#ea580c', weight: 4 }} />
)}
```

---

## Environment Variables Summary

```env
# web/.env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_ORS_API_KEY=REDACTED

# backend/.env
PAGASA_API_TOKEN=REDACTED
```

> ⚠️  Never commit `.env` files to the repository.
> Add `.env` to `.gitignore` on both `web/` and `backend/`.
> Share keys with teammates through a private group chat only.

---

## Attribution Requirements

When deploying, include these attributions (required by license):

- **OpenStreetMap:** "© OpenStreetMap contributors" — already included in the Leaflet TileLayer attribution prop
- **Open-Meteo:** "Weather data by Open-Meteo.com" — add to footer of Weather page
- **OpenRouteService:** "Routing by openrouteservice.org" — add to map legend or footer
- **PAGASA:** "Weather advisories from PAGASA-DOST" — add to Weather page header

---

*ResQperation — Barangay Disaster Risk Reduction and Management System*
*Associate Degree in Software Development Capstone Project*
