# Field reports and damage assessment

Source: shared_db, 2026-10-31T13:37:40+08:00. 17 objects; 34 enforced relationships; 108 displayed columns.

Categories attach to category detail counts; property damage uses the persisted damage catalog.

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
  disasterEvents["disaster_events (SHARED DEPENDENCY)"] {
    string event_id PK
    string name
    int type_id FK
    int severity_level_id FK
    datetime created_at
  }
  fieldReportCategories["field_report_categories (RESQ MAPPING)"] {
    int category_id PK
    string category_key UK
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
  householdStatusLogs["household_status_logs (RESQ MAPPING)"] {
    int status_log_id PK
    string disaster_id FK
    string household_id FK
    int status_id FK
    string source
    text notes
    datetime created_at
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
  hqFieldReports["hq_field_reports (RESQ MAPPING)"] {
    int hq_report_id PK
    string disaster_id FK
    string household_id FK
    string source
    int linked_report_id FK
    datetime created_at
  }
  memberStatuses["member_statuses (RESQ MAPPING)"] {
    int status_id PK
    string status_key UK
    string status_label
    boolean is_active
    datetime created_at
  }
  propertyDamageLevels["property_damage_levels (RESQ MAPPING)"] {
    string damage_key PK
    string label
    boolean is_active
  }
  rescueTeams["rescue_teams (RESQ MAPPING)"] {
    int team_id PK
    string team_code UK
    string team_name
    int assigned_purok_id FK
    int leader_responder_id FK
    datetime created_at
  }
  responderAssignments["responder_assignments (RESQ MAPPING)"] {
    int assignment_id PK
    string assignment_code UK
    int responder_id FK
    int team_id FK
    string disaster_id FK
    int affected_area_id FK
    string household_id FK
    string priority_level
    string status FK
    datetime assigned_at
  }
  responderCheckIns["responder_check_ins (RESQ MAPPING)"] {
    int check_in_id PK
    int responder_id FK
    string disaster_id FK
    int team_id FK
    int affected_area_id FK
    string household_id FK
    string member_id FK
    text notes
  }
  responderFieldReportDetails["responder_field_report_details (RESQ MAPPING)"] {
    int detail_id PK
    int report_id FK
    int category_id FK
    text notes
  }
  responderFieldReportMembers["responder_field_report_members (RESQ MAPPING)"] {
    int detail_id PK
    int report_id FK
    string household_id FK
    string disaster_id FK
    string member_id FK
    int status_id FK
    string status_key
    datetime created_at
  }
  responderFieldReports["responder_field_reports (RESQ MAPPING)"] {
    int report_id PK
    int responder_id FK
    string disaster_id FK
    string household_id FK
    text notes
    datetime created_at
    int assignment_id FK
    int status_log_id FK
    string property_damage FK
    string idempotency_key UK
  }
  responders["responders (RESQ MAPPING)"] {
    int responder_id PK
    string user_id FK
    string responder_code UK
    int team_id FK
    string title
    datetime created_at
  }
  disasterEvents |o..o{ affectedAreas : "disaster_id"
  households |o..o{ householdMembers : "household_id"
  disasterEvents |o..o{ householdStatusLogs : "disaster_id"
  households ||..o{ householdStatusLogs : "household_id"
  householdStatuses ||..o{ householdStatusLogs : "status_id"
  disasterEvents |o..o{ hqFieldReports : "disaster_id"
  households |o..o{ hqFieldReports : "household_id"
  responderFieldReports ||..o{ hqFieldReports : "linked_report_id"
  responders |o..o{ rescueTeams : "leader_responder_id"
  disasterEvents |o..o{ responderAssignments : "disaster_id"
  households |o..o{ responderAssignments : "household_id"
  responders ||..o{ responderAssignments : "responder_id"
  rescueTeams |o..o{ responderAssignments : "team_id"
  affectedAreas |o..o{ responderAssignments : "affected_area_id"
  disasterEvents |o..o{ responderCheckIns : "disaster_id"
  households |o..o{ responderCheckIns : "household_id"
  responders ||..o{ responderCheckIns : "responder_id"
  rescueTeams |o..o{ responderCheckIns : "team_id"
  householdMembers |o..o{ responderCheckIns : "member_id"
  affectedAreas |o..o{ responderCheckIns : "affected_area_id"
  fieldReportCategories ||..o{ responderFieldReportDetails : "category_id"
  responderFieldReports ||..o{ responderFieldReportDetails : "report_id"
  disasterEvents ||..o{ responderFieldReportMembers : "disaster_id"
  households ||..o{ responderFieldReportMembers : "household_id"
  householdMembers ||..o{ responderFieldReportMembers : "member_id"
  responderFieldReports ||..o{ responderFieldReportMembers : "report_id"
  memberStatuses |o..o{ responderFieldReportMembers : "status_id"
  responderAssignments |o..o{ responderFieldReports : "assignment_id"
  disasterEvents |o..o{ responderFieldReports : "disaster_id"
  households |o..o{ responderFieldReports : "household_id"
  responders ||..o{ responderFieldReports : "responder_id"
  propertyDamageLevels |o..o{ responderFieldReports : "property_damage"
  householdStatusLogs |o..o{ responderFieldReports : "status_log_id"
  rescueTeams |o..o{ responders : "team_id"
```

[Raw Mermaid](04_field_assessment.mmd) | [Diagram index](../00_README.md)
