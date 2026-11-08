# Shared evacuation verification data

Source: shared_db, 2026-10-31T13:37:40+08:00. 17 objects; 25 enforced relationships; 89 displayed columns.

Used by check-in and situation reporting. Diagram inclusion does not transfer ownership or reconcile ambiguous shared records.

Presentation view: keys and selected business fields only. Context tables can have additional relationships outside this module; use the unified ERD for those.

```mermaid
erDiagram
  direction LR
  %% Physical FKs only; views and independent stores receive no invented links.
  accommodationTypes["accommodation_types (SHARED DEPENDENCY)"] {
    int type_id PK
    string type_key UK
  }
  accommodationUnits["accommodation_units (SHARED DEPENDENCY)"] {
    int unit_id PK
    string center_id FK
    string name
    int type_id FK
    datetime created_at
  }
  addresses["addresses (SHARED DEPENDENCY)"] {
    int address_id PK
    int barangay_id FK
    int sitio_id FK
    int purok_id FK
    int zipcode_id FK
    datetime created_at
  }
  civilStatuses["civil_statuses (SHARED DEPENDENCY)"] {
    int status_id PK
    string status_key UK
    string status_label
  }
  disasterEvents["disaster_events (SHARED DEPENDENCY)"] {
    string event_id PK
    string name
    int type_id FK
    int severity_level_id FK
    datetime created_at
  }
  educationLevels["education_levels (SHARED DEPENDENCY)"] {
    int education_level_id PK
    string education_level_key UK
  }
  evacuationCenters["evacuation_centers (SHARED DEPENDENCY)"] {
    string evacuation_center_id PK
    string current_event_id FK
    string name
    string status
    datetime created_at
    text notes
  }
  evacuationRecords["evacuation_records (SHARED DEPENDENCY)"] {
    int evacuation_id PK
    string event_id FK
    string household_id FK
    string center_id FK
    int household_status_id FK
    string verified_by FK
    datetime created_at
  }
  genders["genders (SHARED DEPENDENCY)"] {
    int gender_id PK
    string gender_key UK
  }
  householdMembers["household_members (SHARED DEPENDENCY)"] {
    string member_id PK
    string household_id FK
    string first_name
    string last_name
    int gender_id FK
    int relationship_id FK
    int civil_status_id FK
    int occupation FK
    int education_level_id FK
    datetime created_at
    string name
  }
  householdStatuses["household_statuses (SHARED DEPENDENCY)"] {
    int status_id PK
    string status_key UK
    string status_label
    boolean is_active
  }
  households["households (SHARED DEPENDENCY)"] {
    string household_id PK
    string household_code UK
    string household_name
    string created_by FK
    int address_id FK
    datetime created_at
    string login_user_id FK
  }
  memberDisasterStatuses["member_disaster_statuses (RESQ MAPPING)"] {
    int member_status_id PK
    string disaster_id FK
    string household_id FK
    string member_id FK
    int status_id FK
    int previous_status_id FK
    string report_source
    string priority_level
    text notes
    boolean is_verified
  }
  memberStatuses["member_statuses (RESQ MAPPING)"] {
    int status_id PK
    string status_key UK
    string status_label
    boolean is_active
    datetime created_at
  }
  occupations["occupations (SHARED DEPENDENCY)"] {
    int occuaption_id PK
  }
  relationships["relationships (SHARED DEPENDENCY)"] {
    int relationship_id PK
    string relationship_key UK
    boolean is_active
    datetime created_at
  }
  users["users (SHARED DEPENDENCY)"] {
    string user_id PK
    string first_name
    string last_name
    string name
    int role_id FK
    string assigned_center_id FK
    string household_id FK
    string member_id FK,UK
    boolean is_active
  }
  evacuationCenters |o..o{ accommodationUnits : "center_id"
  accommodationTypes |o..o{ accommodationUnits : "type_id"
  disasterEvents |o..o{ evacuationCenters : "current_event_id"
  evacuationCenters |o..o{ evacuationRecords : "center_id"
  disasterEvents |o..o{ evacuationRecords : "event_id"
  households |o..o{ evacuationRecords : "household_id"
  householdStatuses |o..o{ evacuationRecords : "household_status_id"
  users |o..o{ evacuationRecords : "verified_by"
  civilStatuses |o..o{ householdMembers : "civil_status_id"
  educationLevels |o..o{ householdMembers : "education_level_id"
  genders |o..o{ householdMembers : "gender_id"
  households |o..o{ householdMembers : "household_id"
  occupations |o..o{ householdMembers : "occupation"
  relationships |o..o{ householdMembers : "relationship_id"
  addresses |o..o{ households : "address_id"
  users |o..o{ households : "created_by"
  users |o..o{ households : "login_user_id"
  disasterEvents ||..o{ memberDisasterStatuses : "disaster_id"
  households ||..o{ memberDisasterStatuses : "household_id"
  householdMembers ||..o{ memberDisasterStatuses : "member_id"
  memberStatuses |o..o{ memberDisasterStatuses : "previous_status_id"
  memberStatuses ||..o{ memberDisasterStatuses : "status_id"
  evacuationCenters |o..o{ users : "assigned_center_id"
  households |o..o{ users : "household_id"
  householdMembers |o..o| users : "member_id"
```

[Raw Mermaid](12_shared_evacuation_data.mmd) | [Diagram index](../00_README.md)
