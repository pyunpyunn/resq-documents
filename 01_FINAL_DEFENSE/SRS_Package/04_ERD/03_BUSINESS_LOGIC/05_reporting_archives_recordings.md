# Reporting, archives and radio evidence

Source: shared_db, 2026-10-31T13:37:40+08:00. 18 objects; 27 enforced relationships; 94 displayed columns.

Archive table-name/source-ID pairs and JSON file references are application-validated values, not one universal FK. Audio binaries stay outside MySQL.

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
  auditLogs["audit_logs (SHARED DEPENDENCY)"] {
    int audit_log_id PK
    string user_id FK
    string role_key
    datetime created_at
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
  evacuationCenters["evacuation_centers (SHARED DEPENDENCY)"] {
    string evacuation_center_id PK
    string current_event_id FK
    string name
    string status
    datetime created_at
    text notes
  }
  externalReportRequests["external_report_requests (RESQ MAPPING)"] {
    string id PK
    string event_id FK
    string status
    datetime created_at
    string api_version
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
  incidentArchives["incident_archives (RESQ MAPPING)"] {
    int archive_id PK
    string disaster_id FK
    string archived_by_admin_id FK
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
  responderCommunicationLogs["responder_communication_logs (RESQ MAPPING)"] {
    int communication_id PK
    int responder_id FK
    int team_id FK
    string team_name
    string disaster_id FK
    text message
  }
  responders["responders (RESQ MAPPING)"] {
    int responder_id PK
    string user_id FK
    string responder_code UK
    int team_id FK
    string title
    datetime created_at
  }
  severityLevels["severity_levels (SHARED DEPENDENCY)"] {
    int severity_id PK
    string severity_key UK
  }
  situationReportSubmissions["situation_report_submissions (RESQ MAPPING)"] {
    int id PK
    int sit_rep_id FK
    datetime created_at
  }
  situationReports["situation_reports (RESQ MAPPING)"] {
    int sit_rep_id PK
    string report_number UK
    string disaster_id FK
    string household_id FK
    string schema_version
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
  users |o..o{ auditLogs : "user_id"
  severityLevels |o..o{ disasterEvents : "severity_level_id"
  disasterTypes ||..o{ disasterEvents : "type_id"
  disasterEvents |o..o{ evacuationCenters : "current_event_id"
  disasterEvents |o..o{ externalReportRequests : "event_id"
  addresses |o..o{ households : "address_id"
  users |o..o{ households : "created_by"
  users |o..o{ households : "login_user_id"
  users |o..o{ incidentArchives : "archived_by_admin_id"
  disasterEvents |o..o{ incidentArchives : "disaster_id"
  responders |o..o{ rescueTeams : "leader_responder_id"
  evacuationCenters |o..o{ resourceRequests : "evacuation_center_id"
  users |o..o{ resourceRequests : "handled_by"
  users |o..o{ resourceRequests : "requested_by"
  resourceRequestStatus |o..o{ resourceRequests : "status_id"
  users |o..o{ resourceRequests : "validated_by_user_id"
  urgencyLevels |o..o{ resourceRequests : "urgency_id"
  disasterEvents |o..o{ responderCommunicationLogs : "disaster_id"
  responders ||..o{ responderCommunicationLogs : "responder_id"
  rescueTeams |o..o{ responderCommunicationLogs : "team_id"
  rescueTeams |o..o{ responders : "team_id"
  users |o..o{ responders : "user_id"
  situationReports ||..o{ situationReportSubmissions : "sit_rep_id"
  disasterEvents |o..o{ situationReports : "disaster_id"
  households |o..o{ situationReports : "household_id"
  evacuationCenters |o..o{ users : "assigned_center_id"
  households |o..o{ users : "household_id"
```

[Raw Mermaid](05_reporting_archives_recordings.mmd) | [Diagram index](../00_README.md)
