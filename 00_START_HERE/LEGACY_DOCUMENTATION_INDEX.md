# RESQPERATION Documentation Index

This index groups the maintained project-level documents in this folder by purpose. The application repository is `../resqperation-system`. Implementation guides that change with the code remain next to the relevant backend or frontend module; they are not copied here.

Private environment backups are intentionally not indexed or shared. Keep credentials in local `.env` files, not in documentation.

## Project Scope and Academic Documentation

- [RESQPERATION_SRS.md](RESQPERATION_SRS.md) - full software requirements specification, including diagrams, use-case narratives, interface screenshots placeholders, traceability, and approval fields.
- [RESQPERATION_REQUIREMENTS_BREAKDOWN.md](RESQPERATION_REQUIREMENTS_BREAKDOWN.md) - system roles, modules, and functional requirements.
- [RESQPERATION_BARANGAY_PROFILE_SCOPE.md](RESQPERATION_BARANGAY_PROFILE_SCOPE.md) - barangay profile and mapping/weather scope.
- [RESQPERATION_FINAL_DEFENSE_STUDY_GUIDE_AND_DIAGRAMS.md](RESQPERATION_FINAL_DEFENSE_STUDY_GUIDE_AND_DIAGRAMS.md) - system concept and defense preparation.
- [diagrams/14_resqperation_scope_erd.md](diagrams/14_resqperation_scope_erd.md) - RESQPERATION data scope and external boundaries.

There is no standalone related-literature or related-studies chapter in this folder. The sources and research references are catalogued below; use verified citations from those sources when preparing the academic chapter.

## Active Development and Implementation

- [RESQPERATION_G10_STEP_BY_STEP_CHECKLIST.md](RESQPERATION_G10_STEP_BY_STEP_CHECKLIST.md) - active implementation checklist and current integration blockers.
- [RESQPERATION_G10_BEGINNER_MODULE_PROMPTS.md](RESQPERATION_G10_BEGINNER_MODULE_PROMPTS.md) - prompts for delegating module work using the project's implementation rules.
- [RESQPERATION_TRACKINGAID_REQUEST_INTEGRATION_GUIDE.md](RESQPERATION_TRACKINGAID_REQUEST_INTEGRATION_GUIDE.md) - request validation, forwarding, handoff, and verification.
- [RESQPERATION_RESCUER_RADIO_COMMUNICATION.md](RESQPERATION_RESCUER_RADIO_COMMUNICATION.md) - implemented rescuer radio/voice-clip workflow.
- [RESQPERATION_RESCUER_RADIO_PTT_PLAN.md](RESQPERATION_RESCUER_RADIO_PTT_PLAN.md) - planned live push-to-talk work; distinguish its future audio-server steps from the implemented workflow.
- [RESQPERATION_SMS_INTEGRATION.md](RESQPERATION_SMS_INTEGRATION.md) - SMS gateway integration and operational constraints.
- [RESQPERATION_UI_TEXT_AND_OPERATION_RULES_NOTE.md](RESQPERATION_UI_TEXT_AND_OPERATION_RULES_NOTE.md) - operational wording and interaction rules.

## System Architecture and Integrations

- [RESQPERATION_SYSTEM_ARCHITECTURE_FILE_STACK.md](RESQPERATION_SYSTEM_ARCHITECTURE_FILE_STACK.md) - system components, boundaries, routes, and file ownership.
- [RESQPERATION_EXTERNAL_SYSTEM_INTEGRATION_DRAFT.md](RESQPERATION_EXTERNAL_SYSTEM_INTEGRATION_DRAFT.md) - current partner integrations and pending external verification. Runtime configuration is the source of truth; this document must not contain credential values.
- [diagrams/18_system_architecture.md](diagrams/18_system_architecture.md) - architecture diagram.
- [diagrams/01_system_context_and_external_integrations.md](diagrams/01_system_context_and_external_integrations.md) - system context and external boundaries.
- [diagrams/07_data_model_and_database_scope.md](diagrams/07_data_model_and_database_scope.md) - data model and database scope.

## Setup, Database, and Operations

- [RESQPERATION_DB_CONNECTION_SWITCH_GUIDE.md](RESQPERATION_DB_CONNECTION_SWITCH_GUIDE.md) - configuring the active database through local environment settings.
- [RESQPERATION_G10_SAFE_SAMPLE_SEED_PLAN.md](RESQPERATION_G10_SAFE_SAMPLE_SEED_PLAN.md) - development-only sample data and safety boundaries.
- [RESQPERATION_MOBILE_INSTALL_DEV_BUILD_ONESIGNAL_GUIDE.md](RESQPERATION_MOBILE_INSTALL_DEV_BUILD_ONESIGNAL_GUIDE.md) - mobile development builds and push verification.
- [RESQPERATION_ONESIGNAL_MOBILE_SETUP.md](RESQPERATION_ONESIGNAL_MOBILE_SETUP.md) - mobile OneSignal setup and registration flow.
- [RESQPERATION_SHARED_DB_AUDIT_AND_PUSH_TOKENS.md](RESQPERATION_SHARED_DB_AUDIT_AND_PUSH_TOKENS.md) - shared database safety and device-token behavior.
- [RESQPERATION_SHARED_DB_DATA_SOURCE_RULES.md](RESQPERATION_SHARED_DB_DATA_SOURCE_RULES.md) - rules for displaying records from the active database.
- [RESQPERATION_HEAVY_DATA_PERFORMANCE_GUIDE.md](RESQPERATION_HEAVY_DATA_PERFORMANCE_GUIDE.md) - query, pagination, and high-volume data guidance.
- [../resqperation-system/docs/HAZARD_MAPPING_SETUP.md](../resqperation-system/docs/HAZARD_MAPPING_SETUP.md) - hazard-map data setup.
- [../resqperation-system/frontend-mobile/FIRST_RUN_SETUP.md](../resqperation-system/frontend-mobile/FIRST_RUN_SETUP.md) - mobile first-run setup.
- [../resqperation-system/frontend-mobile/ANDROID_RELEASE.md](../resqperation-system/frontend-mobile/ANDROID_RELEASE.md) - Android release workflow.
- [../resqperation-system/frontend-mobile/NOTIFICATION_VERIFICATION.md](../resqperation-system/frontend-mobile/NOTIFICATION_VERIFICATION.md) - mobile notification verification.

## Testing, Readiness, and Quality

- [RESQPERATION_TEST_CASES.md](RESQPERATION_TEST_CASES.md) - functional test scenarios.
- [RESQPERATION_SYSTEM_TEST_AND_IMPROVEMENT_NOTES.md](RESQPERATION_SYSTEM_TEST_AND_IMPROVEMENT_NOTES.md) - test results and prioritized improvements.
- [../resqperation-system/docs/MUST_HAVES_IMPLEMENTATION_AUDIT.md](../resqperation-system/docs/MUST_HAVES_IMPLEMENTATION_AUDIT.md) - implementation coverage audit.
- [../resqperation-system/docs/GPS_FOLLOW_AND_OFFLINE_CHECKS.md](../resqperation-system/docs/GPS_FOLLOW_AND_OFFLINE_CHECKS.md) - GPS and offline behavior checks.
- [../resqperation-system/docs/OFFLINE_NAVIGATION_PROGRESS.md](../resqperation-system/docs/OFFLINE_NAVIGATION_PROGRESS.md) - offline navigation implementation status.

## Sources, External References, and Research

- [RESQPERATION_SYSTEM_STACK_RESOURCES_AND_REFERENCES.md](RESQPERATION_SYSTEM_STACK_RESOURCES_AND_REFERENCES.md) - technology, APIs, data sources, legal basis, and research references. Re-verify dated entries before citing or relying on them.
- [RESQPERATION_RESOURCES.txt](RESQPERATION_RESOURCES.txt) - collected links and learning resources.
- [RESQPERATION_PAGASA_TENDAY_API_REQUEST_LETTER.md](RESQPERATION_PAGASA_TENDAY_API_REQUEST_LETTER.md) - draft request for official forecast API access; it is not evidence that access has been granted.
- [../resqperation-system/docs/MAMBALING_HAZARD_SOURCES.md](../resqperation-system/docs/MAMBALING_HAZARD_SOURCES.md) - hazard mapping source inventory.
- [../resqperation-system/docs/OFFICIAL_WEATHER_OUTLOOK.md](../resqperation-system/docs/OFFICIAL_WEATHER_OUTLOOK.md) - official weather outlook references.
- [../resqperation-system/backend-laravel/docs/report-terminology-and-sources.md](../resqperation-system/backend-laravel/docs/report-terminology-and-sources.md) - situation-report terminology and sources.
- [../resqperation-system/backend-laravel/docs/weather-and-external-reports.md](../resqperation-system/backend-laravel/docs/weather-and-external-reports.md) - weather and external report source handling.

## Diagrams

See [diagrams/README.md](diagrams/README.md) for the complete Mermaid diagram catalogue:

- [01 - System context and external integrations](diagrams/01_system_context_and_external_integrations.md)
- [02 - Roles, use cases, and authentication](diagrams/02_roles_use_cases_and_auth.md)
- [03 - HQ web workflows](diagrams/03_hq_web_workflows.md)
- [04 - Disaster status, dispatch, and mapping](diagrams/04_disaster_status_dispatch_mapping.md)
- [05 - Household/rescuer mobile workflows and radio](diagrams/05_mobile_workflows_household_rescuer_radio.md)
- [06 - Requests, SitRep, archive, and notifications](diagrams/06_resource_requests_sitrep_archive_notifications.md)
- [07 - Data model and database scope](diagrams/07_data_model_and_database_scope.md)
- [08 - SSDLC, security, and privacy](diagrams/08_ssdlc_security_privacy.md)
- [10 - Household status reporting simulation](diagrams/10_household_status_reporting_simulation.md)
- [11 - Household status flow](diagrams/11_household_status_flow.md)
- [12 - Household analytics formula](diagrams/12_household_analytics_formula.md)
- [13 - Rescuer dispatching flow](diagrams/13_rescuer_dispatching_flow.md)
- [14 - RESQPERATION scope ERD](diagrams/14_resqperation_scope_erd.md)
- [15 - Household use case](diagrams/15_household_use_case.md)
- [16 - Rescuer use case](diagrams/16_rescuer_use_case.md)
- [17 - HQ/Admin web use case](diagrams/17_hq_admin_web_use_case.md)
- [18 - System architecture](diagrams/18_system_architecture.md)
- [19 - HTTP request methods and process](diagrams/19_http_request_methods_process.md)
- [20 - Data flow diagram](diagrams/20_data_flow_diagram.md)
- [21 - Radio communication flow](diagrams/21_radio_communication_flow.md)

## Module References

- [../resqperation-system/README.md](../resqperation-system/README.md) - repository overview and development entry point.
- [../resqperation-system/backend-laravel/docs/](../resqperation-system/backend-laravel/docs/) - backend API, reports, integrations, notifications, and implementation notes.
- [../resqperation-system/frontend-mobile/](../resqperation-system/frontend-mobile/) - mobile references and setup documentation.
- [../resqperation-system/frontend-web/](../resqperation-system/frontend-web/) - web frontend documentation.

Module READMEs and editor/agent instruction files remain with their modules. Local-only prototype and development-reference folders are not part of the maintained project documentation set. SQL proposals are review-only and are not documentation instructions to run against a shared database.
