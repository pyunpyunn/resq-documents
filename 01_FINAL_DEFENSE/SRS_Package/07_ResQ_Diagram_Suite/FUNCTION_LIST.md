# RESQPERATION Function List

50 functional use cases across 12 modules; 211 live Laravel route declarations inventoried.

This is source-backed logical documentation, not deployment or partner acceptance evidence. Role access is subject to backend permission configuration.

## Account Access

| ID | Function | User roles |
| --- | --- | --- |
| UC-01 | Sign In / Out | Household Resident, Rescuer Team Leader, Rescuer Team Member, Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response Personnel, Recovery / Rehabilitation |
| UC-02 | Update Own Profile | Household Resident, Rescuer Team Leader, Rescuer Team Member, Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response Personnel, Recovery / Rehabilitation |
| UC-03 | Recover Account Access | Household Resident, Rescuer Team Leader, Rescuer Team Member, Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response Personnel, Recovery / Rehabilitation |
| UC-37 | Allow App Notifications | Household Resident, Rescuer Team Leader, Rescuer Team Member |
| UC-39 | Review Web Notifications | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response Personnel, Recovery / Rehabilitation |
| UC-13A | Display Household QR for EvaTrack | Household Resident |
| UC-40 | Allow Device Location Access | Household Resident, Rescuer Team Leader, Rescuer Team Member |

Source: `documents\01_FINAL_DEFENSE\SRS_Package\02_Use_Cases_and_Narratives\02_MODULES\01_access_use_cases.mmd`
Related tables: `users`, `roles`, `personal_access_tokens`, `password_reset_requests`, `password_reset_tokens`, `device_tokens`, `remembered_devices`, `notifications`, `web_push_subscriptions`, `web_push_deliveries`.

## Administration

| ID | Function | User roles |
| --- | --- | --- |
| UC-04 | Manage Rescuer Teams | Operations / Admin |
| UC-05 | Manage HQ Access | Operations / Admin |
| UC-06 | Maintain Barangay Profile | Operations / Admin |
| UC-07A | Submit Public Inquiry | Public Visitor |
| UC-07B | Review Public Inquiries | Operations / Admin |

Source: `documents\01_FINAL_DEFENSE\SRS_Package\02_Use_Cases_and_Narratives\02_MODULES\02_administration_use_cases.mmd`
Related tables: `users`, `roles`, `responders`, `rescue_teams`, `landing_inquiries`, `barangays`, `audit_logs`.

## First-Login Household Setup

| ID | Function | User roles |
| --- | --- | --- |
| UC-08 | Complete First-Login Household Setup | Household Resident |

Source: `documents\01_FINAL_DEFENSE\SRS_Package\02_Use_Cases_and_Narratives\02_MODULES\03_household_setup_use_cases.mmd`
Related tables: `households`, `household_members`, `addresses`, `geotagged_locations`, `device_tokens`.

## Household Disaster Response

| ID | Function | User roles |
| --- | --- | --- |
| UC-10 | Report Household / Member Safety | Household Resident |
| UC-11 | Assist a Trusted Household | Household Resident |

Source: `documents\01_FINAL_DEFENSE\SRS_Package\02_Use_Cases_and_Narratives\02_MODULES\04_safety_use_cases.mmd`
Related tables: `household_disasters`, `household_status_logs`, `member_status_logs`, `member_disaster_statuses`, `household_statuses`, `member_statuses`, `trusted_households`, `household_trusted_pins`.

## Disaster Alerts

| ID | Function | User roles |
| --- | --- | --- |
| UC-09 | Read Disaster Alerts and Instructions | Household Resident, Rescuer Team Leader, Rescuer Team Member |
| UC-23A | Publish Disaster Alerts Through OneSignal | Chairperson, Operations / Admin |
| UC-23B | Manage Active Event | Chairperson, Operations / Admin, Response Personnel |

Source: `documents\01_FINAL_DEFENSE\SRS_Package\02_Use_Cases_and_Narratives\02_MODULES\05_alerts_use_cases.mmd`
Related tables: `disaster_events`, `disaster_event_types`, `disaster_broadcasts`, `disaster_types`, `severity_levels`, `status_reminders`, `notifications`, `device_tokens`, `household_mobile_notifications`, `web_push_deliveries`.

## Operational Monitoring

| ID | Function | User roles |
| --- | --- | --- |
| UC-22A | Monitor Operations Dashboard | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response Personnel, Recovery / Rehabilitation |
| UC-22B | Review Operational Maps | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response Personnel, Recovery / Rehabilitation |
| UC-24 | Review Hazard Overlays | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response Personnel, Recovery / Rehabilitation |
| UC-25A | Review Safety Reports | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response Personnel, Recovery / Rehabilitation |
| UC-26A | Inspect Rescue Priorities | Chairperson, Operations / Admin, Response Personnel |

Source: `documents\01_FINAL_DEFENSE\SRS_Package\02_Use_Cases_and_Narratives\02_MODULES\06_monitoring_use_cases.mmd`
Related tables: `disaster_events`, `household_disasters`, `household_status_logs`, `households`, `geotagged_locations`, `mapping_hazard_layers`, `weather_logs`, `rescue_criteria_snapshots`, `rescue_criteria_line_snapshots`, `rescue_priority_settings`.

## Rescue Dispatch

| ID | Function | User roles |
| --- | --- | --- |
| UC-15 | Review Assigned Rescue Mission | Rescuer Team Leader, Rescuer Team Member |
| UC-25B | Confirm Household Status | Chairperson, Operations / Admin, Response Personnel |
| UC-26B | Dispatch Rescue Team | Chairperson, Operations / Admin, Response Personnel |
| UC-26C | Approve Dispatch Completion | Chairperson, Operations / Admin |
| UC-41 | Update Assigned Rescue Progress | Rescuer Team Leader, Rescuer Team Member |
| UC-16 | Follow Assigned Rescue Route | Rescuer Team Leader, Rescuer Team Member |
| UC-19 | Submit Assigned Field Report If Needed | Rescuer Team Leader, Rescuer Team Member |

Source: `documents\01_FINAL_DEFENSE\SRS_Package\02_Use_Cases_and_Narratives\02_MODULES\07_dispatch_use_cases.mmd`
Related tables: `responder_assignments`, `rescue_teams`, `responders`, `dispatch_statuses`, `household_disasters`, `rescue_priority_settings`, `rescue_criteria_snapshots`, `rescue_criteria_contact_baselines`, `rescue_criteria_line_snapshots`.

## Field Assessment

| ID | Function | User roles |
| --- | --- | --- |
| UC-18 | Record Rescue Member Assessment | Rescuer Team Leader, Rescuer Team Member |
| UC-19 | Submit Assigned Field Report If Needed | Rescuer Team Leader, Rescuer Team Member |
| UC-27 | Monitor Field Progress | Chairperson, Operations / Admin, Response Personnel |

Source: `documents\01_FINAL_DEFENSE\SRS_Package\02_Use_Cases_and_Narratives\02_MODULES\08_assessment_use_cases.mmd`
Related tables: `responder_check_ins`, `responder_field_reports`, `responder_field_report_details`, `responder_field_report_members`, `hq_field_reports`, `field_report_categories`, `property_damage_levels`, `member_disaster_statuses`.

## Evacuation and Mission Maps

| ID | Function | User roles |
| --- | --- | --- |
| UC-16 | Follow Assigned Rescue Route | Rescuer Team Leader, Rescuer Team Member |
| UC-17 | Synchronize Saved Trips | Rescuer Team Leader, Rescuer Team Member |
| UC-12 | View Evacuation Centers and Routes | Household Resident |
| UC-14 | View Previously Saved Household Data | Household Resident |

Source: `documents\01_FINAL_DEFENSE\SRS_Package\02_Use_Cases_and_Narratives\02_MODULES\09_navigation_use_cases.mmd`
Related tables: `cached_routes`, `offline_packs`, `dispatch_trips`, `trip_points`, `route_coordinates`, `device_tracking_logs`, `responder_location_logs`, `responder_routes`, `sync_events`, `map_tile_metadata`, `evacuation_centers`.

## Field Communication

| ID | Function | User roles |
| --- | --- | --- |
| UC-20A | Transmit PTT Clips | Rescuer Team Leader, Rescuer Team Member |
| UC-20B | Monitor Rescue Communications | Chairperson, Operations / Admin, Response Personnel |

Source: `documents\01_FINAL_DEFENSE\SRS_Package\02_Use_Cases_and_Narratives\02_MODULES\10_radio_use_cases.mmd`
Related tables: `responder_communication_logs`, `responder_assignments`, `responders`, `users`.

## Resource Requests

| ID | Function | User roles |
| --- | --- | --- |
| UC-21A | Submit Logistics Request | Rescuer Team Leader |
| UC-21B | Track Own Requests | Rescuer Team Leader, Rescuer Team Member |
| UC-31 | Submit Partner Request | Partner / configured provider |
| UC-32A | Review Resource Requests | Chairperson, Operations / Admin, Response Personnel, Recovery / Rehabilitation |
| UC-32B | Validate Resource Requests | Chairperson, Operations / Admin |
| UC-33 | Forward Validated Requests | Chairperson, Operations / Admin |

Source: `documents\01_FINAL_DEFENSE\SRS_Package\02_Use_Cases_and_Narratives\02_MODULES\11_requests_use_cases.mmd`
Related tables: `resource_requests`, `request_validations`, `resource_request_status`, `urgency_levels`.

## Reports and Archives

| ID | Function | User roles |
| --- | --- | --- |
| UC-28 | Prepare Situation Reports | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response Personnel, Recovery / Rehabilitation |
| UC-29 | Export Escalation Findings | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response Personnel, Recovery / Rehabilitation |
| UC-30 | Manage Archive Evidence | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response Personnel, Recovery / Rehabilitation |
| UC-34A | Request Operational Report | Partner / configured provider |
| UC-34B | Authorize Report Release | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response Personnel, Recovery / Rehabilitation |
| UC-35 | Review Partner Reports | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response Personnel, Recovery / Rehabilitation |
| UC-36 | Export Selected Findings | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response Personnel, Recovery / Rehabilitation |

Source: `documents\01_FINAL_DEFENSE\SRS_Package\02_Use_Cases_and_Narratives\02_MODULES\12_reports_use_cases.mmd`
Related tables: `situation_reports`, `situation_report_submissions`, `external_report_requests`, `incident_archives`, `hq_field_reports`, `responder_field_reports`, `resource_requests`, `audit_logs`.

## Scope and interpretation

- Legacy use-case sources are reconciled with current mobile UI, WebAccessPolicy and the requested product boundaries. Corrections and evidence are recorded in `assets/scope-corrections.json`. Endpoints/middleware come from the Laravel route inventory.
- The ERD uses the package's physical-schema snapshot. Views and legacy recovery tables are excluded from table diagrams; they remain in the original reference sources. Shared tables are not claimed as RESQPERATION-owned.
- Full and role flow/swimlane diagrams illustrate scoped operating paths; module views contain the detailed decision and error branches.
- Provider delivery, deployed navigation packs, signed-link expiry, partner acceptance, and physical-device behavior remain conditional on their running configuration.
- EvaTrack owns evacuation-arrival verification. RESQPERATION may display a household QR; legacy verification endpoints in the API inventory do not make verification a RESQPERATION user responsibility.
- Disaster and assignment notifications use OneSignal. The SMS recovery integration, where depicted, is limited to configured account recovery and never represents SMS disaster-alert delivery.
- First-login household setup is separate from disaster operations. It covers phone-owner selection when required, household geotag/address confirmation and optional photo capture. Evacuation maps, safety reports and current-disaster instructions are not onboarding tasks.
- Notification and location permissions are real user consent actions. Push-subscription registration is automatic background behavior, not a separate user-facing screen.
- Rescuers may review assigned households, open the assigned route, update permitted mission progress and submit field reports when applicable. Creating dispatches, publishing alerts and approving closure remain separate authorized HQ actions.
- DFD entity copies denote the same logical actor; local copies avoid long connector bundles across process rows.
- A physical FK is drawn only when present in the schema source. Polymorphic / JSON / partner references are not invented as foreign keys.
- Full ERDs retain physical table and column names. Compact views retain primary and foreign keys; the detailed full view retains all fields.
- Dense non-planar graphs can require 90-degree crossings. Routing checks prevent connectors from passing through unrelated cards; compact, module and role views reduce congestion.
