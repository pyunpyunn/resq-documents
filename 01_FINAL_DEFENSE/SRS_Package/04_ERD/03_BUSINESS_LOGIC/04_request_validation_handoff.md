# Resource request validation and partner handoff data

Source: shared_db, 2026-10-31T13:37:40+08:00. 12 objects; 18 enforced relationships; 68 displayed columns.

Tracking/release fields are business values on real requests. Partner systems are not fabricated SQL entities.

Presentation view: keys and selected business fields only. Context tables can have additional relationships outside this module; use the unified ERD for those.

```mermaid
erDiagram
  direction LR
  %% Physical FKs only; views and independent stores receive no invented links.
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
  evacuationCenters["evacuation_centers (SHARED DEPENDENCY)"] {
    string evacuation_center_id PK
    string current_event_id FK
    string name
    string status
    datetime created_at
    text notes
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
  requestValidations["request_validations (RESQ MAPPING)"] {
    int validation_id PK
    string request_id FK
    string validation_status
    string validator_user_id FK
    datetime created_at
  }
  resourceRequestStatus["resource_request_status (SHARED DEPENDENCY)"] {
    int status_id PK
    string status_key UK
    string status_label
  }
  resourceRequests["resource_requests (SHARED DEPENDENCY)"] {
    string request_id PK
    string request_category
    string evacuation_center_id FK
    string requested_by FK
    string handled_by FK
    int status_id FK
    string validation_status
    string validated_by_user_id FK
    string tracking_reference
    datetime created_at
    int urgency_id FK
  }
  roles["roles (SHARED DEPENDENCY)"] {
    int role_id PK
    string role_key UK
    string name
  }
  severityLevels["severity_levels (SHARED DEPENDENCY)"] {
    int severity_id PK
    string severity_key UK
  }
  urgencyLevels["urgency_levels (RESQ MAPPING)"] {
    int urgency_id PK
    string urgency_key UK
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
  severityLevels |o..o{ disasterEvents : "severity_level_id"
  disasterTypes ||..o{ disasterEvents : "type_id"
  disasterEvents |o..o{ evacuationCenters : "current_event_id"
  households |o..o{ householdMembers : "household_id"
  users |o..o{ households : "created_by"
  users |o..o{ households : "login_user_id"
  resourceRequests ||..o{ requestValidations : "request_id"
  users |o..o{ requestValidations : "validator_user_id"
  evacuationCenters |o..o{ resourceRequests : "evacuation_center_id"
  users |o..o{ resourceRequests : "handled_by"
  users |o..o{ resourceRequests : "requested_by"
  resourceRequestStatus |o..o{ resourceRequests : "status_id"
  users |o..o{ resourceRequests : "validated_by_user_id"
  urgencyLevels |o..o{ resourceRequests : "urgency_id"
  evacuationCenters |o..o{ users : "assigned_center_id"
  households |o..o{ users : "household_id"
  householdMembers |o..o| users : "member_id"
  roles |o..o{ users : "role_id"
```

[Raw Mermaid](04_request_validation_handoff.mmd) | [Diagram index](../00_README.md)
