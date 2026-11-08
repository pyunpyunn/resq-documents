# Resqperation Mermaid ERD package

Database: shared_db. Verified snapshot: 2026-10-31T13:37:40+08:00.

23 editable diagrams: two unified ERDs, 12 module/data-domain ERDs, seven business-logic ERDs, a view/recovery ERD and a view-dependency flowchart. Scope: 106 objects (104 base tables, 2 views), 174 actual FK relationships, 1147 columns. All 60 canonical mappings are covered.

## Start here

- [Full physical ERD: every column](01_UNIFIED/01_full_physical_erd.md)
- [Unified key overview](01_UNIFIED/02_unified_key_relationships.md)
- [Table scope and FK catalog](04_REFERENCE/03_table_scope_and_relationships.md)
- [Exact SQL dictionary](04_REFERENCE/04_exact_data_dictionary.md)

## Diagram index

| Diagram | Objects | Links | Markdown | Raw Mermaid |
|---|---:|---:|---|---|
| Full Resqperation physical ERD | 106 | 174 | [Open](01_UNIFIED/01_full_physical_erd.md) | [Source](01_UNIFIED/01_full_physical_erd.mmd) |
| Unified key relationship overview | 106 | 174 | [Open](01_UNIFIED/02_unified_key_relationships.md) | [Source](01_UNIFIED/02_unified_key_relationships.mmd) |
| Identity and account access | 19 | 25 | [Open](02_MODULES/01_identity_and_access.md) | [Source](02_MODULES/01_identity_and_access.mmd) |
| Household and member safety | 32 | 63 | [Open](02_MODULES/02_household_safety.md) | [Source](02_MODULES/02_household_safety.mmd) |
| Teams and rescue dispatch | 19 | 35 | [Open](02_MODULES/03_rescue_dispatch.md) | [Source](02_MODULES/03_rescue_dispatch.mmd) |
| Field reports and damage assessment | 17 | 34 | [Open](02_MODULES/04_field_assessment.md) | [Source](02_MODULES/04_field_assessment.mmd) |
| Navigation and tracking | 23 | 36 | [Open](02_MODULES/05_navigation_and_tracking.md) | [Source](02_MODULES/05_navigation_and_tracking.mmd) |
| Radio and notifications | 18 | 33 | [Open](02_MODULES/06_communications.md) | [Source](02_MODULES/06_communications.mmd) |
| Requests, reporting and archives | 12 | 19 | [Open](02_MODULES/07_requests_reports_archives.md) | [Source](02_MODULES/07_requests_reports_archives.mmd) |
| Public inquiries and staff handling | 3 | 2 | [Open](02_MODULES/08_public_inquiries.md) | [Source](02_MODULES/08_public_inquiries.mmd) |
| Operational and framework support | 19 | 13 | [Open](02_MODULES/09_platform_support.md) | [Source](02_MODULES/09_platform_support.mmd) |
| Geography and household master data | 21 | 28 | [Open](02_MODULES/10_geography_and_master_data.md) | [Source](02_MODULES/10_geography_and_master_data.mmd) |
| Disaster events, hazards and weather | 12 | 18 | [Open](02_MODULES/11_disasters_and_weather.md) | [Source](02_MODULES/11_disasters_and_weather.mmd) |
| Shared evacuation verification data | 17 | 25 | [Open](02_MODULES/12_shared_evacuation_data.md) | [Source](02_MODULES/12_shared_evacuation_data.mmd) |
| Household report to rescue assignment | 26 | 48 | [Open](03_BUSINESS_LOGIC/01_household_report_to_rescue.md) | [Source](03_BUSINESS_LOGIC/01_household_report_to_rescue.mmd) |
| Assessment and safety evidence | 21 | 53 | [Open](03_BUSINESS_LOGIC/02_assessment_and_safety_evidence.md) | [Source](03_BUSINESS_LOGIC/02_assessment_and_safety_evidence.mmd) |
| Priority, dashboard and historical charts | 26 | 37 | [Open](03_BUSINESS_LOGIC/03_priority_dashboard_charts.md) | [Source](03_BUSINESS_LOGIC/03_priority_dashboard_charts.mmd) |
| Resource request validation and partner handoff data | 12 | 18 | [Open](03_BUSINESS_LOGIC/04_request_validation_handoff.md) | [Source](03_BUSINESS_LOGIC/04_request_validation_handoff.mmd) |
| Reporting, archives and radio evidence | 18 | 27 | [Open](03_BUSINESS_LOGIC/05_reporting_archives_recordings.md) | [Source](03_BUSINESS_LOGIC/05_reporting_archives_recordings.mmd) |
| Alert delivery and device identity | 20 | 33 | [Open](03_BUSINESS_LOGIC/06_alert_delivery_devices.md) | [Source](03_BUSINESS_LOGIC/06_alert_delivery_devices.mmd) |
| Household login, device owner and recovery | 17 | 25 | [Open](03_BUSINESS_LOGIC/07_household_login_recovery.md) | [Source](03_BUSINESS_LOGIC/07_household_login_recovery.mmd) |
| Views and retained legacy recovery objects | 4 | 0 | [Open](04_REFERENCE/01_views_and_legacy_objects.md) | [Source](04_REFERENCE/01_views_and_legacy_objects.mmd) |
| SQL view query dependencies | 12 | 14 | [Open](04_REFERENCE/02_view_query_dependencies.md) | [Source](04_REFERENCE/02_view_query_dependencies.mmd) |

## Reading and scope

- Labels retain real table names and distinguish Resq mappings, shared dependencies, shared framework, SQL views and legacy recovery. Mapping does not establish exclusive ownership.
- PK = primary key; FK = enforced foreign-key column; UK = individually unique column. Composite unique groups are documented separately.
- Parent || = required; parent |o = optional, derived from FK nullability. Child o{ = zero or more; child o| = at most one, derived from actual unique/primary keys. FKs do not guarantee every parent has children.
- Solid lines are identifying (FK contributes to child PK); dotted lines are non-identifying. Both represent enforced physical FKs. Labels name actual child FK columns.
- Standalone caches, queues, journals and views can legitimately have no FK line. The view dependency flowchart shows SQL joins separately.
- Polymorphic Sanctum owners/archive targets, JSON references, partner systems and external audio paths are not converted into invented physical relationships.
- Unified scope includes code-verified shared data roots, their FK parent closure, framework stores and labelled legacy/view objects. It excludes unused partner internals. Module views limit context to direct parent tables; use the unified ERD for cross-module closure.

## Using Mermaid

Open .md files in a Mermaid-capable viewer or paste matching .mmd sources into your editor. Use Mermaid 11 or newer for entity aliases. The full physical diagram is large; module/business views are better suited to defense slides.
All 23 sources fit Mermaid's default 50,000-character text limit; the largest contains 45,549 characters. The unified diagram is still visually large, so use module views for defense slides. These files are editable sources, not exported SVG/PDF images.

## Existing drafts and verification

The existing 07_data_model_and_database_scope.md and 14_resqperation_scope_erd.md were preserved as earlier SRS drafts; their conceptual links are not the current physical-schema authority. No database, environment or application behavior was changed to generate this package.
The generation manifest records schema hashes and exact coverage. The [validation report](04_REFERENCE/06_validation_report.md) confirms that all 23 diagrams passed Mermaid 11.17.2 parsing and independent schema/key/cardinality checks. The shared database has additional unrelated tables; the package draws the 174 foreign keys within the documented Resqperation scope, not every foreign key in the shared database.
