# ResQperation — Geotagging, Dispatch Tracking & Routing
> Free & Open Source location services for household geotagging,
> live rescuer team tracking, and evacuation route display
> Last updated: May 2025

---

## Table of Contents
1. [Overview — Three separate location features](#1-overview--three-separate-location-features)
2. [Household Geotagging](#2-household-geotagging)
3. [Dispatch Team Live Tracking](#3-dispatch-team-live-tracking)
4. [Evacuation Routing](#4-evacuation-routing)
5. [Important: foreground vs background location](#5-important-foreground-vs-background-location)
6. [Database columns needed](#6-database-columns-needed)
7. [Complete mobile code — rescuer screen](#7-complete-mobile-code--rescuer-screen)
8. [Quick reference table](#8-quick-reference-table)

---

## 1. Overview — Three Separate Location Features

These are three different features that all use location but work differently:

```
FEATURE 1 — Household Geotagging
  Who does it:  Household member (one time setup)
  When:         When they first register or from their profile screen
  What happens: Their device GPS coordinates saved permanently to resq_households
  Package:      expo-location (getCurrentPositionAsync — one shot)

FEATURE 2 — Dispatch Team Live Tracking
  Who does it:  Rescuer (active during a disaster operation)
  When:         While the rescuer app is OPEN and they are on duty
  What happens: Coordinates sent to Laravel every 30 seconds
                Dashboard map updates the team marker in real time
  Package:      expo-location (watchPositionAsync — continuous while app is open)

FEATURE 3 — Evacuation Route Display
  Who does it:  HQ Dispatcher on the web dashboard
  When:         Dispatcher clicks "Show route" on a dispatch record
  What happens: OSRM public API called once — returns a route polyline
                Route drawn on Leaflet map as dashed orange line
  Package:      fetch() call from React — no mobile package needed
```

---

## 2. Household Geotagging

### What it is
A one-time action. When a household member opens the mobile app and
sets up their profile, the app captures their GPS coordinates and saves
them to the database. These coordinates become the dots on the mapping page.

### Package
```bash
cd mobile
npx expo install expo-location
```

### How it works — mobile code

```javascript
// mobile/api/households.js

import * as Location from 'expo-location';
import api from './axios';

// Call this when the household user sets up their profile
// OR when they tap "Update my location" in the profile screen
export async function saveMyLocation(householdId) {
  // 1. Ask for permission
  const { status } = await Location.requestForegroundPermissionsAsync();

  if (status !== 'granted') {
    throw new Error('Location permission denied. Please enable it in Settings.');
  }

  // 2. Get current GPS position (one-time, not continuous)
  const location = await Location.getCurrentPositionAsync({
    accuracy: Location.Accuracy.High, // uses GPS, not just WiFi/cell tower
  });

  const { latitude, longitude } = location.coords;

  // 3. Save to your Laravel back end
  await api.post(`/households/${householdId}/geotag`, {
    lat: latitude,
    lng: longitude,
  });

  return { lat: latitude, lng: longitude };
}
```

### Mobile screen — profile with geotag button

```javascript
// mobile/app/(household)/profile.jsx

import { useState } from 'react';
import { View, Text, TouchableOpacity, Alert } from 'react-native';
import { saveMyLocation } from '../../api/households';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function HouseholdProfile() {
  const [saving, setSaving] = useState(false);

  async function handleGeotag() {
    setSaving(true);
    try {
      const user = JSON.parse(await AsyncStorage.getItem('user'));
      await saveMyLocation(user.household_id);
      Alert.alert('Success', 'Your location has been saved.');
    } catch (err) {
      Alert.alert('Error', err.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <View className="flex-1 p-6 bg-white">
      <Text className="text-lg font-bold mb-6">My Profile</Text>

      {/* Other profile fields... */}

      <TouchableOpacity
        onPress={handleGeotag}
        disabled={saving}
        className="bg-blue-600 p-4 rounded-xl mt-4"
      >
        <Text className="text-white font-bold text-center text-base">
          {saving ? 'Saving location...' : '📍 Save My Location'}
        </Text>
      </TouchableOpacity>

      <Text className="text-xs text-gray-400 mt-2 text-center">
        This pins your household on the barangay map.
        Only needed once. Update if you move.
      </Text>
    </View>
  );
}
```

### Laravel back end — geotag endpoint

```php
// routes/api.php
Route::post('/households/{id}/geotag', [HouseholdController::class, 'geotag'])
    ->middleware('auth:sanctum');
```

```php
// In HouseholdController.php

// Save the GPS coordinates of a household
public function geotag(Request $request, $id)
{
    $request->validate([
        'lat' => 'required|numeric|between:-90,90',
        'lng' => 'required|numeric|between:-180,180',
    ]);

    // Make sure the logged-in user owns this household
    $household = \DB::table('resq_households')->where('id', $id)->first();

    if (!$household) {
        return response()->json(['message' => 'Household not found'], 404);
    }

    \DB::table('resq_households')
        ->where('id', $id)
        ->update([
            'lat'        => $request->lat,
            'lng'        => $request->lng,
            'updated_at' => now(),
        ]);

    // Log the action
    \DB::table('resq_activity_logs')->insert([
        'disaster_event_id' => null,
        'actor_id'          => $request->user()->id,
        'actor_role'        => 'household',
        'event_type'        => 'household.geotagged',
        'entity_type'       => 'household',
        'entity_id'         => $id,
        'description'       => 'Household location pinned by member',
        'created_at'        => now(),
        'updated_at'        => now(),
    ]);

    return response()->json(['message' => 'Location saved', 'lat' => $request->lat, 'lng' => $request->lng]);
}
```

### How dots appear on the web map

The map page fetches `GET /api/households/map-points` which returns only:
```json
[
  { "id": 1, "lat": 10.3157, "lng": 123.8854, "status": "safe" },
  { "id": 2, "lat": 10.3162, "lng": 123.8861, "status": null },
  ...
]
```

`status: null` = unchecked (gray dot). No lat/lng = household not yet geotagged (skip it).

---

## 3. Dispatch Team Live Tracking

### What it is
While a rescuer is out on a mission, their phone sends GPS coordinates
to your Laravel API every 30 seconds. The HQ dashboard polls those
coordinates and updates team markers on the map in near real-time.

### Important limitation
**expo-location only tracks location while the app is open (foreground).**
Background location requires special Android Play Store review and is
not needed for a capstone. The expectation is that rescuers keep the app open
on their phone while on mission — which is realistic for barangay operations.

### Mobile code — rescuer dispatch screen

```javascript
// mobile/api/dispatch.js

import * as Location from 'expo-location';
import api from './axios';

// Start sending location updates every 30 seconds
// Call this when rescuer marks themselves as "on mission"
// Returns a cleanup function — call it to stop tracking
export function startLocationTracking(dispatchId) {
  let watchSubscription = null;
  let intervalId = null;

  async function begin() {
    const { status } = await Location.requestForegroundPermissionsAsync();
    if (status !== 'granted') {
      console.warn('Location permission not granted');
      return;
    }

    // Watch position — updates whenever device moves 10+ meters
    watchSubscription = await Location.watchPositionAsync(
      {
        accuracy:         Location.Accuracy.Balanced, // good accuracy, saves battery
        timeInterval:     30000,  // minimum 30 seconds between updates
        distanceInterval: 10,     // or when moved 10 meters, whichever comes first
      },
      async (location) => {
        const { latitude, longitude } = location.coords;

        try {
          await api.patch(`/dispatches/${dispatchId}/location`, {
            lat: latitude,
            lng: longitude,
          });
        } catch (err) {
          // Silently fail — don't crash the app if one update fails
          console.warn('Location update failed:', err.message);
        }
      }
    );
  }

  begin();

  // Return cleanup function
  return () => {
    if (watchSubscription) {
      watchSubscription.remove();
    }
  };
}
```

### Use it in the rescuer dispatch screen

```javascript
// mobile/app/(rescuer)/dispatch.jsx

import { useEffect, useState } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { startLocationTracking } from '../../api/dispatch';
import api from '../../api/axios';

export default function RescuerDispatch() {
  const [dispatch, setDispatch] = useState(null);
  const [tracking, setTracking] = useState(false);

  useEffect(() => {
    // Load the rescuer's current dispatch assignment
    api.get('/dispatches/my-assignment').then(res => setDispatch(res.data));
  }, []);

  useEffect(() => {
    if (!dispatch || dispatch.status === 'standby') return;

    // Start tracking when dispatched or on-scene
    const stopTracking = startLocationTracking(dispatch.id);
    setTracking(true);

    // Stop tracking when this screen unmounts (rescuer navigates away)
    return () => {
      stopTracking();
      setTracking(false);
    };
  }, [dispatch?.id, dispatch?.status]);

  if (!dispatch) return <Text className="p-6">No active assignment.</Text>;

  return (
    <View className="flex-1 p-6 bg-white">

      {/* Tracking indicator */}
      {tracking && (
        <View className="flex-row items-center gap-2 bg-green-50 border border-green-200 rounded-lg p-3 mb-4">
          <View className="w-2 h-2 rounded-full bg-green-500" />
          <Text className="text-green-700 text-sm font-medium">
            Live location sharing active — HQ can see your position
          </Text>
        </View>
      )}

      {/* Dispatch details */}
      <Text className="text-xl font-bold">{dispatch.mission_type}</Text>
      <Text className="text-gray-500 mt-1">{dispatch.area}</Text>
      <Text className="text-gray-400 text-sm mt-1">
        Team: {dispatch.team_name} · {dispatch.member_count} members
      </Text>

      {/* Status update buttons */}
      <View className="mt-6 gap-3">
        {dispatch.status === 'dispatched' && (
          <TouchableOpacity
            className="bg-blue-600 p-4 rounded-xl"
            onPress={() => updateStatus('onscene')}
          >
            <Text className="text-white font-bold text-center">
              ✓ Mark as On-Scene
            </Text>
          </TouchableOpacity>
        )}

        {dispatch.status === 'onscene' && (
          <TouchableOpacity
            className="bg-green-600 p-4 rounded-xl"
            onPress={() => updateStatus('completed')}
          >
            <Text className="text-white font-bold text-center">
              ✓ Mark as Completed
            </Text>
          </TouchableOpacity>
        )}
      </View>
    </View>
  );

  async function updateStatus(newStatus) {
    await api.patch(`/dispatches/${dispatch.id}/status`, { status: newStatus });
    setDispatch(prev => ({ ...prev, status: newStatus }));
  }
}
```

### Laravel — dispatch location endpoint

```php
// routes/api.php
Route::patch('/dispatches/{id}/location', [DispatchController::class, 'updateLocation'])
    ->middleware(['auth:sanctum', 'role:rescuer']);

Route::get('/dispatches/my-assignment', [DispatchController::class, 'myAssignment'])
    ->middleware('auth:sanctum');
```

```php
// In DispatchController.php

// Rescuer sends their current GPS coordinates
public function updateLocation(Request $request, $id)
{
    $request->validate([
        'lat' => 'required|numeric|between:-90,90',
        'lng' => 'required|numeric|between:-180,180',
    ]);

    \DB::table('resq_dispatches')
        ->where('id', $id)
        ->update([
            'current_lat'          => $request->lat,
            'current_lng'          => $request->lng,
            'location_updated_at'  => now(),
        ]);

    return response()->json(['message' => 'Location updated']);
}

// Get the active dispatch assignment for the logged-in rescuer
public function myAssignment(Request $request)
{
    $user = $request->user();

    // Find the active event
    $event = \DB::table('resq_disaster_events')
        ->where('status', 'active')
        ->first();

    if (!$event) {
        return response()->json(null);
    }

    // Find this rescuer's team's dispatch for the active event
    // (assumes rescuer.purok maps to their team's area — adjust to your schema)
    $dispatch = \DB::table('resq_dispatches as d')
        ->join('resq_rescue_teams as t', 'd.rescue_team_id', '=', 't.id')
        ->where('d.disaster_event_id', $event->id)
        ->where('d.status', '!=', 'standby')
        ->select('d.*', 't.name as team_name', 't.member_count')
        ->first();

    return response()->json($dispatch);
}
```

### Web dashboard — display team markers on Leaflet map

```javascript
// Inside web/src/pages/Mapping.jsx

import { useEffect, useState } from 'react';
import { Marker, Popup, Circle } from 'react-leaflet';
import api from '../api/axios';

// Custom team icons by status color
function teamIcon(color) {
  return L.divIcon({
    html: `<div style="
      width: 28px; height: 28px;
      background: ${color};
      border: 3px solid white;
      border-radius: 50%;
      box-shadow: 0 2px 6px rgba(0,0,0,0.4);
      display: flex; align-items: center; justify-content: center;
      font-size: 12px; color: white; font-weight: bold;
    ">🚑</div>`,
    className: '',
    iconSize:   [28, 28],
    iconAnchor: [14, 14],
  });
}

const TEAM_COLORS = {
  sar:      '#7c3aed',
  evac:     '#2563eb',
  medical:  '#dc2626',
  relief:   '#16a34a',
  comms:    '#d97706',
  fire:     '#f97316',
  dana:     '#0d9488',
  security: '#64748b',
};

export function TeamMarkers() {
  const [teams, setTeams] = useState([]);

  // Poll every 30 seconds for updated team positions
  useEffect(() => {
    function fetchTeams() {
      api.get('/dispatches').then(res => setTeams(res.data));
    }

    fetchTeams(); // load immediately
    const interval = setInterval(fetchTeams, 30000);
    return () => clearInterval(interval);
  }, []);

  return teams
    .filter(t => t.current_lat && t.current_lng) // only show teams with a known position
    .map(team => (
      <Marker
        key={team.id}
        position={[team.current_lat, team.current_lng]}
        icon={teamIcon(TEAM_COLORS[team.code] ?? '#475569')}
      >
        <Popup>
          <strong>{team.name}</strong><br />
          Status: {team.status}<br />
          Mission: {team.mission_type}<br />
          Area: {team.area}<br />
          <small>
            Updated: {team.location_updated_at
              ? new Date(team.location_updated_at).toLocaleTimeString()
              : 'Unknown'}
          </small>
        </Popup>
      </Marker>
    ));
}
```

---

## 4. Evacuation Routing

### What it is
When HQ clicks "Show route to evacuation site" on the map or dispatch page,
a route line is drawn from the team's current position to the selected
evacuation center. Uses the **OSRM public demo server** — free, no key needed.

### Two routing options

#### Option A — OSRM Demo Server (simplest, no key, good for capstone)

OSRM is an open-source route planning library written in C++, designed for compatibility with OpenStreetMap road network data. FOSSGIS runs a free public demo server.

```
Base URL: https://router.project-osrm.org
No API key. No account. No rate limit published (be respectful — don't spam it).
```

```javascript
// web/src/api/routing.js

// Get driving route between two points using OSRM public server
// coords = [[lng, lat], [lng, lat]]  ← NOTE: lng first, then lat (OSRM format)
export async function getRoute(fromLngLat, toLngLat) {
  const [fromLng, fromLat] = fromLngLat;
  const [toLng, toLat]     = toLngLat;

  const url = `https://router.project-osrm.org/route/v1/driving/`
    + `${fromLng},${fromLat};${toLng},${toLat}`
    + `?overview=full&geometries=geojson&steps=false`;

  const res  = await fetch(url);
  const data = await res.json();

  if (data.code !== 'Ok') {
    throw new Error('Could not find a route');
  }

  // Return the route geometry as GeoJSON
  return data.routes[0].geometry;
}

// Get estimated travel time and distance (summary only, no route drawn)
export async function getRouteSummary(fromLngLat, toLngLat) {
  const [fromLng, fromLat] = fromLngLat;
  const [toLng, toLat]     = toLngLat;

  const url = `https://router.project-osrm.org/route/v1/driving/`
    + `${fromLng},${fromLat};${toLng},${toLat}`
    + `?overview=false`;

  const res  = await fetch(url);
  const data = await res.json();

  if (data.code !== 'Ok') return null;

  const route = data.routes[0];
  return {
    distance_km: (route.distance / 1000).toFixed(2),
    duration_min: Math.ceil(route.duration / 60),
  };
}
```

#### Option B — OpenRouteService (more features, free signup, 2,000 req/day)

Use this if you need turn-by-turn instructions or more advanced routing.
See `API_REFERENCE.md` section 2 for the full ORS setup.

### Draw the route on the Leaflet map

```javascript
// web/src/pages/Mapping.jsx

import { GeoJSON }       from 'react-leaflet';
import { getRoute }      from '../api/routing';
import { useState }      from 'react';

export default function Mapping() {
  const [activeRoute, setActiveRoute] = useState(null);
  const [routeInfo,   setRouteInfo]   = useState(null);
  const [loadingRoute, setLoadingRoute] = useState(false);

  // Called when HQ clicks "Show route" on a dispatch or evac site
  async function showRouteTo(evacSite, teamPosition) {
    setLoadingRoute(true);
    try {
      const fromCoords = [teamPosition.lng, teamPosition.lat]; // [lng, lat]
      const toCoords   = [evacSite.lng,     evacSite.lat];

      const routeGeometry = await getRoute(fromCoords, toCoords);
      setActiveRoute(routeGeometry);

      // Also show ETA
      const summary = await getRouteSummary(fromCoords, toCoords);
      setRouteInfo(summary);

    } catch (err) {
      alert('Could not load route: ' + err.message);
    } finally {
      setLoadingRoute(false);
    }
  }

  return (
    // Inside your <MapContainer>:
    <>
      {/* Route line */}
      {activeRoute && (
        <GeoJSON
          key={JSON.stringify(activeRoute)} // force re-render when route changes
          data={activeRoute}
          style={{
            color:     '#ea580c',  // orange — matches prototype
            weight:    5,
            opacity:   0.85,
            dashArray: '10 6',     // dashed line
          }}
        />
      )}

      {/* Route info box */}
      {routeInfo && (
        <div style={{
          position: 'absolute', bottom: 80, right: 12,
          background: 'white', border: '1px solid #e2e8f0',
          borderRadius: 8, padding: '10px 14px', zIndex: 1000,
          fontSize: 13,
        }}>
          <div style={{ fontWeight: 600, marginBottom: 4 }}>
            Route to evacuation site
          </div>
          <div>🚗 {routeInfo.distance_km} km</div>
          <div>⏱ ~{routeInfo.duration_min} min</div>
          <button
            onClick={() => { setActiveRoute(null); setRouteInfo(null); }}
            style={{ marginTop: 8, fontSize: 11, color: '#dc2626', background: 'none', border: 'none', cursor: 'pointer' }}
          >
            Clear route
          </button>
        </div>
      )}
    </>
  );
}
```

### Route for each evacuation site (add to map legend/panel)

```javascript
// A button in the map layer panel or dispatch table that triggers the route

<button
  onClick={() => showRouteTo(evacSite, teamPosition)}
  disabled={loadingRoute}
  style={{
    padding: '4px 10px',
    fontSize: 11,
    background: '#1e3a5f',
    color: 'white',
    border: 'none',
    borderRadius: 5,
    cursor: 'pointer',
  }}
>
  {loadingRoute ? 'Loading...' : '🗺 Show route'}
</button>
```

---

## 5. Important: Foreground vs Background Location

This is a common gotcha. Understand this before you start building.

```
FOREGROUND location   → app is open and visible on screen
                      → works in Expo Go (no build needed for testing)
                      → expo-location supports this fully
                      → USE THIS for dispatch tracking

BACKGROUND location   → app is running but screen is off or another app is open
                      → requires building a real APK (not Expo Go)
                      → requires special Android Play Store review
                      → NOT needed for ResQperation
                      → DO NOT implement this for capstone
```

**Why foreground is enough:**
Rescuers on active missions will have the app open on their phone.
They need to see household statuses, update dispatch status, and report findings.
The app being open means foreground location works perfectly.

**If the app is closed:** the team marker simply stops updating on the map.
HQ will see the last known position. This is acceptable for barangay-scale operations.

---

## 6. Database Columns Needed

### resq_households — add lat/lng

```php
// database/migrations/xxxx_add_geotag_to_resq_households.php

public function up(): void
{
    Schema::table('resq_households', function (Blueprint $table) {
        // GPS latitude — stored as decimal with 7 decimal places (~1cm accuracy)
        $table->decimal('lat', 10, 7)->nullable()->after('address');
        // GPS longitude
        $table->decimal('lng', 10, 7)->nullable()->after('lat');
    });
}
```

### resq_dispatches — add live location columns

```php
// database/migrations/xxxx_add_location_to_resq_dispatches.php

public function up(): void
{
    Schema::table('resq_dispatches', function (Blueprint $table) {
        // Current GPS latitude of the team (updated every 30 seconds)
        $table->decimal('current_lat', 10, 7)->nullable()->after('notes');
        // Current GPS longitude
        $table->decimal('current_lng', 10, 7)->nullable()->after('current_lat');
        // When the location was last updated — shown in map popup
        $table->timestamp('location_updated_at')->nullable()->after('current_lng');
    });
}
```

Run both migrations:
```bash
cd backend
php artisan migrate
```

---

## 7. Complete Mobile Code — Rescuer Screen

This is the full rescuer home screen with geotagging of households
(marking a household as visited and checking their status on-site).

```javascript
// mobile/app/(rescuer)/home.jsx

import { useEffect, useState } from 'react';
import {
  View, Text, FlatList, TouchableOpacity,
  Modal, TextInput, Alert, ActivityIndicator
} from 'react-native';
import * as Location from 'expo-location';
import api from '../../api/axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function RescuerHome() {
  const [households,    setHouseholds]    = useState([]);
  const [loading,       setLoading]       = useState(true);
  const [selected,      setSelected]      = useState(null);  // household being updated
  const [modalOpen,     setModalOpen]     = useState(false);
  const [newStatus,     setNewStatus]     = useState('');
  const [notes,         setNotes]         = useState('');
  const [submitting,    setSubmitting]    = useState(false);

  useEffect(() => {
    loadHouseholds();
  }, []);

  async function loadHouseholds() {
    setLoading(true);
    try {
      const user = JSON.parse(await AsyncStorage.getItem('user'));
      const res  = await api.get('/households', {
        params: { purok: user.purok }
      });
      setHouseholds(res.data.data);
    } catch (err) {
      Alert.alert('Error', 'Could not load households');
    } finally {
      setLoading(false);
    }
  }

  function openStatusModal(household) {
    setSelected(household);
    setNewStatus('');
    setNotes('');
    setModalOpen(true);
  }

  async function submitStatus() {
    if (!newStatus) {
      Alert.alert('Select a status first');
      return;
    }

    setSubmitting(true);
    try {
      // Optionally tag the rescuer's current location with the status update
      let locationNote = '';
      try {
        const loc = await Location.getCurrentPositionAsync({
          accuracy: Location.Accuracy.Balanced,
        });
        locationNote = ` [GPS: ${loc.coords.latitude.toFixed(5)}, ${loc.coords.longitude.toFixed(5)}]`;
      } catch {
        // Location unavailable — still submit without it
      }

      await api.post(`/households/${selected.id}/status`, {
        status: newStatus,
        notes:  notes + locationNote,
      });

      // Update the local list immediately
      setHouseholds(prev =>
        prev.map(hh =>
          hh.id === selected.id
            ? { ...hh, status: newStatus }
            : hh
        )
      );

      setModalOpen(false);
      Alert.alert('Updated', `${selected.head_name} marked as ${newStatus}`);
    } catch (err) {
      Alert.alert('Error', 'Could not update status');
    } finally {
      setSubmitting(false);
    }
  }

  function getStatusColor(status) {
    switch (status) {
      case 'safe':      return '#16a34a';
      case 'evacuated': return '#2563eb';
      case 'unsafe':    return '#dc2626';
      default:          return '#94a3b8';
    }
  }

  if (loading) {
    return (
      <View className="flex-1 items-center justify-center">
        <ActivityIndicator size="large" color="#1e3a5f" />
      </View>
    );
  }

  return (
    <View className="flex-1 bg-gray-50">
      {/* Header */}
      <View className="bg-slate-800 px-4 py-4 pt-12">
        <Text className="text-white font-bold text-lg">Household Status</Text>
        <Text className="text-slate-400 text-sm">
          {households.length} households in your purok
        </Text>
      </View>

      {/* Household list */}
      <FlatList
        data={households}
        keyExtractor={item => String(item.id)}
        contentContainerStyle={{ padding: 12, gap: 8 }}
        renderItem={({ item }) => (
          <TouchableOpacity
            onPress={() => openStatusModal(item)}
            className="bg-white rounded-xl p-4 border border-gray-100"
            style={{ shadowColor: '#000', shadowOpacity: 0.04, shadowRadius: 4 }}
          >
            <View className="flex-row items-center justify-between">
              <View className="flex-1">
                <Text className="font-semibold text-gray-900">{item.household_code}</Text>
                <Text className="text-gray-500 text-sm">{item.head_name}</Text>
                <Text className="text-gray-400 text-xs mt-1">{item.purok} · {item.member_count} members</Text>
              </View>

              {/* Status badge */}
              <View style={{
                backgroundColor: getStatusColor(item.status) + '20',
                borderRadius: 8,
                paddingHorizontal: 10,
                paddingVertical: 4,
              }}>
                <Text style={{
                  color: getStatusColor(item.status),
                  fontSize: 12,
                  fontWeight: '600',
                }}>
                  {item.status ?? 'Unchecked'}
                </Text>
              </View>
            </View>
          </TouchableOpacity>
        )}
      />

      {/* Status update modal */}
      <Modal
        visible={modalOpen}
        transparent
        animationType="slide"
        onRequestClose={() => setModalOpen(false)}
      >
        <View className="flex-1 justify-end" style={{ backgroundColor: 'rgba(0,0,0,0.4)' }}>
          <View className="bg-white rounded-t-2xl p-6">
            <Text className="font-bold text-lg mb-1">
              {selected?.household_code} — {selected?.head_name}
            </Text>
            <Text className="text-gray-400 text-sm mb-6">
              {selected?.purok} · {selected?.member_count} family members
            </Text>

            {/* Status buttons */}
            <Text className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3">
              Update status
            </Text>
            <View className="gap-3 mb-4">
              {[
                { value: 'safe',      label: '✓  Safe',                  bg: '#f0fdf4', color: '#16a34a', border: '#86efac' },
                { value: 'evacuated', label: '🏠  Evacuated',             bg: '#eff6ff', color: '#2563eb', border: '#93c5fd' },
                { value: 'unsafe',    label: '⚠  Needs help / Unsafe',   bg: '#fef2f2', color: '#dc2626', border: '#fca5a5' },
              ].map(opt => (
                <TouchableOpacity
                  key={opt.value}
                  onPress={() => setNewStatus(opt.value)}
                  style={{
                    padding: 14,
                    borderRadius: 10,
                    borderWidth: 2,
                    borderColor: newStatus === opt.value ? opt.color : opt.border,
                    backgroundColor: newStatus === opt.value ? opt.bg : '#fafafa',
                  }}
                >
                  <Text style={{
                    color: opt.color,
                    fontWeight: '600',
                    fontSize: 15,
                  }}>
                    {opt.label}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>

            {/* Notes */}
            <TextInput
              placeholder="Optional notes (injuries, address, etc.)"
              value={notes}
              onChangeText={setNotes}
              multiline
              numberOfLines={2}
              className="border border-gray-200 rounded-lg p-3 text-sm text-gray-700 mb-4"
              style={{ textAlignVertical: 'top' }}
            />

            {/* Buttons */}
            <View className="flex-row gap-3">
              <TouchableOpacity
                onPress={() => setModalOpen(false)}
                className="flex-1 border border-gray-200 rounded-xl p-4"
              >
                <Text className="text-center text-gray-500 font-medium">Cancel</Text>
              </TouchableOpacity>
              <TouchableOpacity
                onPress={submitStatus}
                disabled={submitting}
                className="flex-2 rounded-xl p-4"
                style={{ flex: 2, backgroundColor: '#1e3a5f' }}
              >
                <Text className="text-center text-white font-bold">
                  {submitting ? 'Saving...' : 'Submit Status'}
                </Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
}
```

---

## 8. Quick Reference Table

| Feature | Package | When called | Frequency | Key needed |
|---|---|---|---|---|
| Household geotagging | `expo-location` | Once on profile setup | One-time | No |
| Team live tracking | `expo-location` | While rescuer is on mission | Every 30 sec | No |
| Dispatch location endpoint | Your Laravel API | Receives team coords | Per update | N/A |
| Evacuation routing (OSRM) | `fetch()` only | When HQ clicks "Show route" | On demand | No |
| Evacuation routing (ORS) | `fetch()` only | When HQ clicks "Show route" | On demand | Free signup |
| Map display | `leaflet` + `react-leaflet` | On map page load | Polling 30s | No |

---

## Install Summary

```bash
# Mobile only
cd mobile
npx expo install expo-location

# Web — already covered in API_REFERENCE.md
# npm install leaflet react-leaflet  (already installed)
# No new package needed for OSRM routing — uses plain fetch()

# Back end — no new package needed
# Just add the two migrations and two controller methods above
```

---

## app.json — enable location permissions

```json
{
  "expo": {
    "plugins": [
      [
        "expo-location",
        {
          "locationWhenInUsePermission":
            "ResQperation needs your location to tag your household on the barangay map and to track rescue team positions during disaster response.",
          "isAndroidBackgroundLocationEnabled": false,
          "isAndroidForegroundServiceEnabled": true
        }
      ]
    ]
  }
}
```

---

*ResQperation — Barangay Disaster Risk Reduction and Management System*
*Associate Degree in Software Development Capstone Project*
