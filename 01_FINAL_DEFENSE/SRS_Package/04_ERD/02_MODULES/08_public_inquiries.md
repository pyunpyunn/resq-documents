# Public inquiries and staff handling

Source: shared_db, 2026-10-31T13:37:40+08:00. 3 objects; 2 enforced relationships; 19 displayed columns.

The implemented table is landing_inquiries. The separate unconfirmed inquiries table is excluded.

Presentation view: keys and selected business fields only. Context tables can have additional relationships outside this module; use the unified ERD for those.

```mermaid
erDiagram
  direction LR
  %% Physical FKs only; views and independent stores receive no invented links.
  auditLogs["audit_logs (SHARED DEPENDENCY)"] {
    int audit_log_id PK
    string user_id FK
    string role_key
    datetime created_at
  }
  landingInquiries["landing_inquiries (RESQ MAPPING)"] {
    int inquiry_id PK
    string name
    text message
    string status
    string handled_by_user_id FK
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
  users |o..o{ auditLogs : "user_id"
  users |o..o{ landingInquiries : "handled_by_user_id"
```

[Raw Mermaid](08_public_inquiries.mmd) | [Diagram index](../00_README.md)
