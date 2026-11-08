# Household login, device owner and recovery

Source: shared_db, 2026-10-31T13:37:40+08:00. 17 objects; 25 enforced relationships; 91 displayed columns.

Uses consolidated login_user_id, device owner/selection fields and SMS recovery. Retired duplicate access/OTP/device tables are not reintroduced.

Presentation view: keys and selected business fields only. Context tables can have additional relationships outside this module; use the unified ERD for those.

```mermaid
erDiagram
  direction LR
  %% Physical FKs only; views and independent stores receive no invented links.
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
  deviceTokens["device_tokens (SHARED DEPENDENCY)"] {
    int id PK
    string household_id FK
    string member_id FK
    boolean is_active
    datetime logged_at
    datetime created_at
    string user_id FK
    int team_id FK
    int selection_token_id FK
    int responder_id FK
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
  households["households (SHARED DEPENDENCY)"] {
    string household_id PK
    string household_code UK
    string household_name
    string created_by FK
    int address_id FK
    datetime created_at
    string login_user_id FK
  }
  occupations["occupations (SHARED DEPENDENCY)"] {
    int occuaption_id PK
  }
  passwordResetRequests["password_reset_requests (RESQ MAPPING)"] {
    string request_id PK
    string user_id FK
    string token_hash UK
    datetime created_at
    string otp_subject_key UK
    string household_id FK
    datetime sent_at
  }
  personalAccessTokens["personal_access_tokens (SHARED DEPENDENCY)"] {
    int id PK
    text name
    string token UK
    datetime created_at
  }
  relationships["relationships (SHARED DEPENDENCY)"] {
    int relationship_id PK
    string relationship_key UK
    boolean is_active
    datetime created_at
  }
  rememberedDevices["remembered_devices (RESQ MAPPING)"] {
    string remembered_device_id PK
    string user_id FK
    string token_hash UK
    datetime created_at
  }
  rescueTeams["rescue_teams (RESQ MAPPING)"] {
    int team_id PK
    string team_code UK
    string team_name
    int assigned_purok_id FK
    int leader_responder_id FK
    datetime created_at
  }
  responders["responders (RESQ MAPPING)"] {
    int responder_id PK
    string user_id FK
    string responder_code UK
    int team_id FK
    string title
    datetime created_at
  }
  roles["roles (SHARED DEPENDENCY)"] {
    int role_id PK
    string role_key UK
    string name
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
  households |o..o{ deviceTokens : "REDACTED"
  householdMembers |o..o{ deviceTokens : "REDACTED"
  responders |o..o{ deviceTokens : "REDACTED"
  rescueTeams |o..o{ deviceTokens : "REDACTED"
  users |o..o{ deviceTokens : "REDACTED"
  personalAccessTokens |o..o{ deviceTokens : "REDACTED"
  civilStatuses |o..o{ householdMembers : "civil_status_id"
  educationLevels |o..o{ householdMembers : "education_level_id"
  genders |o..o{ householdMembers : "gender_id"
  households |o..o{ householdMembers : "household_id"
  occupations |o..o{ householdMembers : "occupation"
  relationships |o..o{ householdMembers : "relationship_id"
  addresses |o..o{ households : "address_id"
  users |o..o{ households : "created_by"
  users |o..o{ households : "login_user_id"
  users |o..o{ passwordResetRequests : "user_id"
  households |o..o{ passwordResetRequests : "household_id"
  users ||..o{ rememberedDevices : "user_id"
  responders |o..o{ rescueTeams : "leader_responder_id"
  rescueTeams |o..o{ responders : "team_id"
  users |o..o{ responders : "user_id"
  evacuationCenters |o..o{ users : "assigned_center_id"
  households |o..o{ users : "household_id"
  householdMembers |o..o| users : "member_id"
  roles |o..o{ users : "role_id"
```

[Raw Mermaid](07_household_login_recovery.mmd) | [Diagram index](../00_README.md)
