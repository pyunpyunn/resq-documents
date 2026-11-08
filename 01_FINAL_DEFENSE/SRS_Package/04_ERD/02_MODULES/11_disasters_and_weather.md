# Disaster events, hazards and weather

Source: shared_db, 2026-10-31T13:37:40+08:00. 12 objects; 18 enforced relationships; 56 displayed columns.

Includes the actual event/type junction used by broadcast workflows. External providers are data sources, not SQL tables.

Presentation view: keys and selected business fields only. Context tables can have additional relationships outside this module; use the unified ERD for those.

```mermaid
erDiagram
  direction LR
  %% Physical FKs only; views and independent stores receive no invented links.
  affectedAreas["affected_areas (RESQ MAPPING)"] {
    int affected_area_id PK
    string disaster_id FK
    int severity_id FK
    int purok_id FK
    int sitio_id FK
    int barangay_id FK
  }
  barangays["barangays (SHARED DEPENDENCY)"] {
    int barangay_id PK
    string barangay_code UK
    int city_id FK
  }
  disasterBroadcasts["disaster_broadcasts (RESQ MAPPING)"] {
    int broadcast_id PK
    string disaster_id FK
    int severity_id FK
    text message
    string channel
    string status
    int notification_id FK
    int weather_log_id FK
    datetime sent_at
  }
  disasterEventTypes["disaster_event_types (SHARED DEPENDENCY)"] {
    int event_type_id PK
    string event_id FK
    int type_id FK
  }
  disasterEvents["disaster_events (SHARED DEPENDENCY)"] {
    string event_id PK
    string name
    int type_id FK
    int severity_level_id FK
    datetime created_at
  }
  disasterTypes["disaster_types (SHARED DEPENDENCY)"] {
    int type_id PK
    string type_code UK
    boolean is_active
    datetime created_at
  }
  mappingHazardLayers["mapping_hazard_layers (RESQ MAPPING)"] {
    int id PK
    int barangay_id FK
    string name
    string source
    datetime created_at
  }
  notifications["notifications (SHARED DEPENDENCY)"] {
    int notif_id PK
    text message
    string sent_by FK
    string evacuation_event_id FK
    string evacuation_center_id FK
    int recurrence_type_id FK
    datetime created_at
    string channel
    string status
    string source_key UK
    string advisory_fingerprint UK
  }
  puroks["puroks (SHARED DEPENDENCY)"] {
    int purok_id PK
    int sitio_id FK
  }
  severityLevels["severity_levels (SHARED DEPENDENCY)"] {
    int severity_id PK
    string severity_key UK
  }
  sitios["sitios (SHARED DEPENDENCY)"] {
    int sitio_id PK
    int barangay_id FK
  }
  weatherLogs["weather_logs (RESQ MAPPING)"] {
    int weather_log_id PK
    string disaster_id FK
    datetime observed_at
    datetime created_at
  }
  barangays |o..o{ affectedAreas : "barangay_id"
  disasterEvents |o..o{ affectedAreas : "disaster_id"
  puroks |o..o{ affectedAreas : "purok_id"
  severityLevels |o..o{ affectedAreas : "severity_id"
  sitios |o..o{ affectedAreas : "sitio_id"
  disasterEvents |o..o{ disasterBroadcasts : "disaster_id"
  notifications |o..o{ disasterBroadcasts : "notification_id"
  severityLevels |o..o{ disasterBroadcasts : "severity_id"
  weatherLogs |o..o{ disasterBroadcasts : "weather_log_id"
  disasterEvents |o..o{ disasterEventTypes : "event_id"
  disasterTypes ||..o{ disasterEventTypes : "type_id"
  severityLevels |o..o{ disasterEvents : "severity_level_id"
  disasterTypes ||..o{ disasterEvents : "type_id"
  barangays ||..o{ mappingHazardLayers : "barangay_id"
  disasterEvents |o..o{ notifications : "evacuation_event_id"
  sitios ||..o{ puroks : "sitio_id"
  barangays ||..o{ sitios : "barangay_id"
  disasterEvents |o..o{ weatherLogs : "disaster_id"
```

[Raw Mermaid](11_disasters_and_weather.mmd) | [Diagram index](../00_README.md)
