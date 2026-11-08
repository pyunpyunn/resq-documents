# Resqperation use-case, flowchart and swimlane package

50 Mermaid diagrams; 50 current use-case entries; ten human role views. Every diagram has matching .md and .mmd source. All route references were checked against 208 registered API routes.

## Start here

- [Full-system use cases](01_FULL_SYSTEM/01_full_use_cases.md)
- [Full-system process flow](01_FULL_SYSTEM/02_full_process_flow.md)
- [Full-system responsibility swimlane](01_FULL_SYSTEM/03_full_responsibility_swimlane.md)
- [Current use-case narratives and route evidence](06_REFERENCE/01_current_use_case_catalog.md)
- [Role permission matrix](06_REFERENCE/02_role_permission_matrix.md)
- [Syntax and traceability validation](06_REFERENCE/04_validation_report.md)

## How to present the package

Start with the full-system overview, then select a module diagram, the relevant role view, and the business swimlane for the panel question. Module views cover feature boundaries; role views cover who may act; swimlanes cover responsibility and alternatives. A readable module view is preferable to shrinking the entire system onto one slide.

Mermaid has no native UML use-case or BPMN swimlane grammar. Use-case files therefore use labelled actor boxes, oval goals and an explicit system boundary. Their neutral lines are associations, not temporal flow or UML include/extend claims. Swimlanes use flowchart subgraphs and labelled arrows; they are responsibility lanes, not a claim of BPMN execution semantics.

## Diagram index

| View | Kind | Markdown | Raw Mermaid |
|---|---|---|---|
| Full-system use-case map | usecase | [Open](01_FULL_SYSTEM/01_full_use_cases.md) | [Source](01_FULL_SYSTEM/01_full_use_cases.mmd) |
| Full-system operational flow | flowchart | [Open](01_FULL_SYSTEM/02_full_process_flow.md) | [Source](01_FULL_SYSTEM/02_full_process_flow.mmd) |
| Full-system operational flow | swimlane | [Open](01_FULL_SYSTEM/03_full_responsibility_swimlane.md) | [Source](01_FULL_SYSTEM/03_full_responsibility_swimlane.mmd) |
| Access, recovery and notification registration — use cases | usecase | [Open](02_MODULES/01_access_use_cases.md) | [Source](02_MODULES/01_access_use_cases.mmd) |
| Authenticate and enter the correct workspace | swimlane | [Open](02_MODULES/01_access_swimlane.md) | [Source](02_MODULES/01_access_swimlane.mmd) |
| Personnel administration and public inquiries — use cases | usecase | [Open](02_MODULES/02_administration_use_cases.md) | [Source](02_MODULES/02_administration_use_cases.mmd) |
| Restricted administration and public inquiry intake | swimlane | [Open](02_MODULES/02_administration_swimlane.md) | [Source](02_MODULES/02_administration_swimlane.mmd) |
| Household owner selection, setup and location — use cases | usecase | [Open](02_MODULES/03_household_setup_use_cases.md) | [Source](02_MODULES/03_household_setup_use_cases.mmd) |
| Household owner, setup and geotag | swimlane | [Open](02_MODULES/03_household_setup_swimlane.md) | [Source](02_MODULES/03_household_setup_swimlane.mmd) |
| Household safety, trusted reporting and SMS — use cases | usecase | [Open](02_MODULES/04_safety_use_cases.md) | [Source](02_MODULES/04_safety_use_cases.mmd) |
| Record an authorized household or member safety report | swimlane | [Open](02_MODULES/04_safety_swimlane.md) | [Source](02_MODULES/04_safety_swimlane.mmd) |
| Disaster lifecycle and broadcast delivery — use cases | usecase | [Open](02_MODULES/05_alerts_use_cases.md) | [Source](02_MODULES/05_alerts_use_cases.mmd) |
| Save an alert and record actual OneSignal delivery | swimlane | [Open](02_MODULES/05_alerts_swimlane.md) | [Source](02_MODULES/05_alerts_swimlane.mmd) |
| Dashboard, maps, weather and priorities — use cases | usecase | [Open](02_MODULES/06_monitoring_use_cases.md) | [Source](02_MODULES/06_monitoring_use_cases.mmd) |
| Read database-backed operational monitoring | swimlane | [Open](02_MODULES/06_monitoring_swimlane.md) | [Source](02_MODULES/06_monitoring_swimlane.mmd) |
| Rescue dispatch and mission progress — use cases | usecase | [Open](02_MODULES/07_dispatch_use_cases.md) | [Source](02_MODULES/07_dispatch_use_cases.mmd) |
| Dispatch a scoped rescue assignment | swimlane | [Open](02_MODULES/07_dispatch_swimlane.md) | [Source](02_MODULES/07_dispatch_swimlane.mmd) |
| Field assessment and evacuation evidence — use cases | usecase | [Open](02_MODULES/08_assessment_use_cases.md) | [Source](02_MODULES/08_assessment_use_cases.mmd) |
| Validate and persist field assessment evidence | swimlane | [Open](02_MODULES/08_assessment_swimlane.md) | [Source](02_MODULES/08_assessment_swimlane.mmd) |
| Navigation and supported offline synchronization — use cases | usecase | [Open](02_MODULES/09_navigation_use_cases.md) | [Source](02_MODULES/09_navigation_use_cases.mmd) |
| Navigate with online or supported saved data | swimlane | [Open](02_MODULES/09_navigation_swimlane.md) | [Source](02_MODULES/09_navigation_swimlane.mmd) |
| Internet radio and audio evidence — use cases | usecase | [Open](02_MODULES/10_radio_use_cases.md) | [Source](02_MODULES/10_radio_use_cases.mmd) |
| Record and review internet PTT audio evidence | swimlane | [Open](02_MODULES/10_radio_swimlane.md) | [Source](02_MODULES/10_radio_swimlane.mmd) |
| Resource request validation and handoff — use cases | usecase | [Open](02_MODULES/11_requests_use_cases.md) | [Source](02_MODULES/11_requests_use_cases.mmd) |
| Validate a request before partner handoff | swimlane | [Open](02_MODULES/11_requests_swimlane.md) | [Source](02_MODULES/11_requests_swimlane.mmd) |
| Situation reports, archives and partner exchange — use cases | usecase | [Open](02_MODULES/12_reports_use_cases.md) | [Source](02_MODULES/12_reports_use_cases.mmd) |
| Prepare or release a scoped report | swimlane | [Open](02_MODULES/12_reports_swimlane.md) | [Source](02_MODULES/12_reports_swimlane.mmd) |
| Public visitor — permitted use cases | usecase | [Open](03_USER_ROLES/01_public.md) | [Source](03_USER_ROLES/01_public.mmd) |
| Household resident — permitted use cases | usecase | [Open](03_USER_ROLES/02_household_resident.md) | [Source](03_USER_ROLES/02_household_resident.mmd) |
| Rescuer team leader — permitted use cases | usecase | [Open](03_USER_ROLES/03_tl.md) | [Source](03_USER_ROLES/03_tl.mmd) |
| Rescuer team member — permitted use cases | usecase | [Open](03_USER_ROLES/04_tm.md) | [Source](03_USER_ROLES/04_tm.mmd) |
| Chairperson — permitted use cases | usecase | [Open](03_USER_ROLES/05_chair.md) | [Source](03_USER_ROLES/05_chair.mmd) |
| Operations / Admin — permitted use cases | usecase | [Open](03_USER_ROLES/06_operations_admin.md) | [Source](03_USER_ROLES/06_operations_admin.mmd) |
| Mitigation / Prevention — permitted use cases | usecase | [Open](03_USER_ROLES/07_mitigation_prevention.md) | [Source](03_USER_ROLES/07_mitigation_prevention.mmd) |
| Preparedness — permitted use cases | usecase | [Open](03_USER_ROLES/08_preparedness.md) | [Source](03_USER_ROLES/08_preparedness.mmd) |
| Response personnel — permitted use cases | usecase | [Open](03_USER_ROLES/09_response.md) | [Source](03_USER_ROLES/09_response.mmd) |
| Recovery / Rehabilitation — permitted use cases | usecase | [Open](03_USER_ROLES/10_recovery_rehabilitation.md) | [Source](03_USER_ROLES/10_recovery_rehabilitation.mmd) |
| Household mobile subsystem | swimlane | [Open](04_SUBSYSTEMS/01_household_mobile.md) | [Source](04_SUBSYSTEMS/01_household_mobile.mmd) |
| Rescuer mobile subsystem | swimlane | [Open](04_SUBSYSTEMS/02_rescuer_mobile.md) | [Source](04_SUBSYSTEMS/02_rescuer_mobile.mmd) |
| HQ web subsystem | swimlane | [Open](04_SUBSYSTEMS/03_hq_web.md) | [Source](04_SUBSYSTEMS/03_hq_web.mmd) |
| Partner report exchange subsystem | swimlane | [Open](04_SUBSYSTEMS/04_partner_report_exchange.md) | [Source](04_SUBSYSTEMS/04_partner_report_exchange.mmd) |
| Household safety evidence to rescue response | swimlane | [Open](05_BUSINESS_LOGIC/01_report_to_dispatch.md) | [Source](05_BUSINESS_LOGIC/01_report_to_dispatch.mmd) |
| Household owner, setup and geotag | swimlane | [Open](05_BUSINESS_LOGIC/02_household_owner_setup.md) | [Source](05_BUSINESS_LOGIC/02_household_owner_setup.mmd) |
| Save an alert and record actual OneSignal delivery | swimlane | [Open](05_BUSINESS_LOGIC/03_alert_delivery_provider_id.md) | [Source](05_BUSINESS_LOGIC/03_alert_delivery_provider_id.mmd) |
| Validate and persist field assessment evidence | swimlane | [Open](05_BUSINESS_LOGIC/04_field_assessment_evidence.md) | [Source](05_BUSINESS_LOGIC/04_field_assessment_evidence.mmd) |
| Validate a request before partner handoff | swimlane | [Open](05_BUSINESS_LOGIC/05_resource_validation_handoff.md) | [Source](05_BUSINESS_LOGIC/05_resource_validation_handoff.mmd) |
| Prepare or release a scoped report | swimlane | [Open](05_BUSINESS_LOGIC/06_report_release_and_exports.md) | [Source](05_BUSINESS_LOGIC/06_report_release_and_exports.mmd) |
| Navigate with online or supported saved data | swimlane | [Open](05_BUSINESS_LOGIC/07_offline_trip_sync.md) | [Source](05_BUSINESS_LOGIC/07_offline_trip_sync.mmd) |
| Record and review internet PTT audio evidence | swimlane | [Open](05_BUSINESS_LOGIC/08_radio_audio_evidence.md) | [Source](05_BUSINESS_LOGIC/08_radio_audio_evidence.mmd) |
| Identify, review, export or delete archive evidence | swimlane | [Open](05_BUSINESS_LOGIC/09_archive_identification_and_actions.md) | [Source](05_BUSINESS_LOGIC/09_archive_identification_and_actions.mmd) |

## Important interpretation rules

- Current role keys and server permissions govern access. Operations/Admin, Chairperson, Response and committee roles are not interchangeable. Resource-request approval and HQ dispatch completion differ from general visibility and mobile assignment progress.
- The selected operational database supplies records and labels. These workflow diagrams do not silently switch the backend to shared_db or treat local records as shared records.
- Push is conditional on consent, a real registered subscription, provider configuration and actual acceptance. A OneSignal ID is returned by the provider, not generated for every saved or failed broadcast.
- Radio requires internet; actual audio files are outside MySQL. Browser VAPID push is separate from mobile OneSignal.
- Saved household reading and navigation-event replay are distinct. No universal offline write queue, complete scanner UI or automatic district-report transmission is asserted.
- Provider APIs, shared master records, queue workers, signed links and exported files have explicit availability/configuration limits. An edge does not establish successful production delivery.

## Existing documents

The original USE_CASES.md, SRS narrative source and earlier role diagrams remain untouched. They contain older scope/verification statements; use this current package and route references for the generated diagrams, then reconcile the approved SRS baseline before submission. Supplementary diagram sources do not embed images into the DOCX.
