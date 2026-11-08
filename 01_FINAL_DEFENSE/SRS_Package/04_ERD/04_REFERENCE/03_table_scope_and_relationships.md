# Table scope and physical relationship catalog

Verified snapshot: 2026-10-31T13:37:40+08:00. Schema metadata only.

| Object | Classification | Columns | Primary key | Modules |
|---|---|---:|---|---|
| `_archive_orphan_household_disasters` | LEGACY RECOVERY | 18 | household_disaster_id |  |
| `_archive_orphan_household_status_logs` | LEGACY RECOVERY | 20 | status_log_id |  |
| `accommodation_types` | SHARED DEPENDENCY | 3 | type_id | Shared evacuation verification data |
| `accommodation_units` | SHARED DEPENDENCY | 7 | unit_id | Shared evacuation verification data |
| `addresses` | SHARED DEPENDENCY | 21 | address_id | Identity and account access; Household and member safety; Teams and rescue dispatch; Geography and household master data; Shared evacuation verification data |
| `affected_areas` | RESQ MAPPING | 9 | affected_area_id | Household and member safety; Teams and rescue dispatch; Field reports and damage assessment; Disaster events, hazards and weather |
| `audit_logs` | SHARED DEPENDENCY | 12 | audit_log_id | Public inquiries and staff handling; Operational and framework support |
| `barangay_boundaries` | RESQ MAPPING | 10 | psgc_code | Navigation and tracking; Geography and household master data |
| `barangays` | SHARED DEPENDENCY | 4 | barangay_id | Household and member safety; Navigation and tracking; Geography and household master data; Disaster events, hazards and weather |
| `cache` | SHARED FRAMEWORK | 3 | key | Operational and framework support |
| `cache_locks` | SHARED FRAMEWORK | 3 | key | Operational and framework support |
| `cached_routes` | RESQ MAPPING | 15 | id | Navigation and tracking |
| `cities` | SHARED DEPENDENCY | 4 | city_id | Geography and household master data |
| `civil_statuses` | SHARED DEPENDENCY | 3 | status_id | Identity and account access; Household and member safety; Geography and household master data; Shared evacuation verification data |
| `device_tokens` | SHARED DEPENDENCY | 32 | id | Identity and account access; Household and member safety; Teams and rescue dispatch; Navigation and tracking; Radio and notifications; Operational and framework support |
| `device_tracking_logs` | RESQ MAPPING | 13 | tracking_id | Operational and framework support |
| `disaster_broadcasts` | RESQ MAPPING | 28 | broadcast_id | Radio and notifications; Disaster events, hazards and weather |
| `disaster_event_types` | SHARED DEPENDENCY | 3 | event_type_id | Disaster events, hazards and weather |
| `disaster_events` | SHARED DEPENDENCY | 10 | event_id | Household and member safety; Teams and rescue dispatch; Field reports and damage assessment; Navigation and tracking; Radio and notifications; Requests, reporting and archives; Disaster events, hazards and weather; Shared evacuation verification data |
| `disaster_types` | SHARED DEPENDENCY | 7 | type_id | Teams and rescue dispatch; Disaster events, hazards and weather |
| `dispatch_statuses` | RESQ MAPPING | 10 | status_key | Teams and rescue dispatch |
| `dispatch_trips` | RESQ MAPPING | 15 | id | Teams and rescue dispatch; Navigation and tracking |
| `education_levels` | SHARED DEPENDENCY | 3 | education_level_id | Identity and account access; Household and member safety; Geography and household master data; Shared evacuation verification data |
| `evacuation_centers` | SHARED DEPENDENCY | 16 | evacuation_center_id | Identity and account access; Navigation and tracking; Radio and notifications; Requests, reporting and archives; Shared evacuation verification data |
| `evacuation_records` | SHARED DEPENDENCY | 11 | evacuation_id | Shared evacuation verification data |
| `external_report_requests` | RESQ MAPPING | 17 | id | Requests, reporting and archives |
| `failed_jobs` | SHARED FRAMEWORK | 7 | id | Operational and framework support |
| `field_report_categories` | RESQ MAPPING | 3 | category_id | Field reports and damage assessment |
| `genders` | SHARED DEPENDENCY | 3 | gender_id | Identity and account access; Household and member safety; Geography and household master data; Shared evacuation verification data |
| `geotagged_locations` | SHARED DEPENDENCY | 12 | location_id | Household and member safety |
| `household_disasters` | RESQ MAPPING | 18 | household_disaster_id | Household and member safety |
| `household_geographic_classifications` | RESQ MAPPING | 8 | household_id | Household and member safety; Geography and household master data |
| `household_members` | SHARED DEPENDENCY | 30 | member_id | Identity and account access; Household and member safety; Field reports and damage assessment; Navigation and tracking; Radio and notifications; Operational and framework support; Geography and household master data; Shared evacuation verification data |
| `household_mobile_notifications` | RESQ MAPPING | 9 | notification_id | Household and member safety |
| `household_status_logs` | RESQ MAPPING | 20 | status_log_id | Household and member safety; Field reports and damage assessment |
| `household_statuses` | SHARED DEPENDENCY | 9 | status_id | Household and member safety; Field reports and damage assessment; Shared evacuation verification data |
| `household_trusted_pins` | RESQ MAPPING | 5 | household_id | Household and member safety |
| `households` | SHARED DEPENDENCY | 14 | household_id | Identity and account access; Household and member safety; Teams and rescue dispatch; Field reports and damage assessment; Navigation and tracking; Radio and notifications; Requests, reporting and archives; Operational and framework support; Geography and household master data; Shared evacuation verification data |
| `hq_field_reports` | RESQ MAPPING | 6 | hq_report_id | Field reports and damage assessment |
| `incident_archives` | RESQ MAPPING | 9 | archive_id | Requests, reporting and archives |
| `job_batches` | SHARED FRAMEWORK | 10 | id | Operational and framework support |
| `jobs` | SHARED FRAMEWORK | 7 | id | Operational and framework support |
| `landing_inquiries` | RESQ MAPPING | 13 | inquiry_id | Public inquiries and staff handling |
| `map_tile_metadata` | RESQ MAPPING | 7 | tile_id | Navigation and tracking |
| `mapping_hazard_layers` | RESQ MAPPING | 9 | id | Navigation and tracking; Disaster events, hazards and weather |
| `member_disaster_statuses` | RESQ MAPPING | 28 | member_status_id | Household and member safety; Shared evacuation verification data |
| `member_status_logs` | RESQ MAPPING | 20 | member_status_log_id | Household and member safety |
| `member_statuses` | RESQ MAPPING | 14 | status_id | Household and member safety; Field reports and damage assessment; Shared evacuation verification data |
| `member_vulnerable_groups` | SHARED DEPENDENCY | 3 | id | Household and member safety; Geography and household master data |
| `migrations` | SHARED FRAMEWORK | 3 | id | Operational and framework support |
| `notifications` | SHARED DEPENDENCY | 22 | notif_id | Radio and notifications; Disaster events, hazards and weather |
| `occupations` | SHARED DEPENDENCY | 3 | occuaption_id | Identity and account access; Household and member safety; Geography and household master data; Shared evacuation verification data |
| `offline_packs` | RESQ MAPPING | 9 | version | Navigation and tracking |
| `operational_sequences` | RESQ MAPPING | 3 | sequence_key | Operational and framework support |
| `password_reset_requests` | RESQ MAPPING | 17 | request_id | Identity and account access |
| `password_reset_tokens` | SHARED FRAMEWORK | 3 | email | Identity and account access; Operational and framework support |
| `personal_access_tokens` | SHARED DEPENDENCY | 10 | id | Identity and account access; Navigation and tracking; Radio and notifications |
| `property_damage_levels` | RESQ MAPPING | 4 | damage_key | Field reports and damage assessment |
| `provinces` | SHARED DEPENDENCY | 4 | province_id | Geography and household master data |
| `purok_boundaries` | RESQ MAPPING | 5 | purok_id | Household and member safety; Geography and household master data |
| `puroks` | SHARED DEPENDENCY | 3 | purok_id | Household and member safety; Teams and rescue dispatch; Navigation and tracking; Geography and household master data; Disaster events, hazards and weather |
| `realtime_outbox` | RESQ MAPPING | 8 | id | Operational and framework support |
| `recurrence_types` | SHARED DEPENDENCY | 3 | type_id | Radio and notifications |
| `regions` | SHARED DEPENDENCY | 3 | region_id | Geography and household master data |
| `relationships` | SHARED DEPENDENCY | 10 | relationship_id | Identity and account access; Household and member safety; Geography and household master data; Shared evacuation verification data |
| `remembered_devices` | RESQ MAPPING | 12 | remembered_device_id | Identity and account access |
| `report_idempotency` | RESQ MAPPING | 7 | scope | Operational and framework support |
| `request_validations` | RESQ MAPPING | 10 | validation_id | Requests, reporting and archives |
| `rescue_criteria_contact_baselines` | RESQ MAPPING | 4 | event_id, household_id | Teams and rescue dispatch |
| `rescue_criteria_line_snapshots` | RESQ MAPPING | 15 | id | Teams and rescue dispatch |
| `rescue_criteria_snapshots` | RESQ MAPPING | 10 | id | Teams and rescue dispatch |
| `rescue_priority_settings` | RESQ MAPPING | 12 | version | Teams and rescue dispatch |
| `rescue_teams` | RESQ MAPPING | 12 | team_id | Identity and account access; Teams and rescue dispatch; Field reports and damage assessment; Navigation and tracking; Radio and notifications |
| `resource_request_status` | SHARED DEPENDENCY | 3 | status_id | Requests, reporting and archives |
| `resource_requests` | SHARED DEPENDENCY | 22 | request_id | Requests, reporting and archives |
| `responder_assignments` | RESQ MAPPING | 23 | assignment_id | Teams and rescue dispatch; Field reports and damage assessment; Navigation and tracking |
| `responder_check_ins` | RESQ MAPPING | 15 | check_in_id | Field reports and damage assessment |
| `responder_communication_logs` | RESQ MAPPING | 7 | communication_id | Radio and notifications |
| `responder_field_report_details` | RESQ MAPPING | 5 | detail_id | Field reports and damage assessment |
| `responder_field_report_members` | RESQ MAPPING | 10 | detail_id | Field reports and damage assessment |
| `responder_field_reports` | RESQ MAPPING | 19 | report_id | Field reports and damage assessment |
| `responder_location_logs` | RESQ MAPPING | 7 | log_id | Navigation and tracking |
| `responder_routes` | RESQ MAPPING | 16 | route_id | Navigation and tracking |
| `responders` | RESQ MAPPING | 27 | responder_id | Identity and account access; Household and member safety; Teams and rescue dispatch; Field reports and damage assessment; Navigation and tracking; Radio and notifications |
| `resq_orphan_references` | RESQ MAPPING | 7 | id | Operational and framework support |
| `roles` | SHARED DEPENDENCY | 8 | role_id | Identity and account access |
| `route_coordinates` | RESQ MAPPING | 7 | coordinate_id | Navigation and tracking |
| `sessions` | SHARED FRAMEWORK | 6 | id | Identity and account access; Operational and framework support |
| `severity_levels` | SHARED DEPENDENCY | 3 | severity_id | Household and member safety; Teams and rescue dispatch; Radio and notifications; Disaster events, hazards and weather |
| `sitios` | SHARED DEPENDENCY | 3 | sitio_id | Household and member safety; Geography and household master data; Disaster events, hazards and weather |
| `situation_report_submissions` | RESQ MAPPING | 8 | id | Requests, reporting and archives |
| `situation_reports` | RESQ MAPPING | 18 | sit_rep_id | Requests, reporting and archives |
| `status_reminders` | RESQ MAPPING | 13 | reminder_id | Household and member safety |
| `sync_events` | RESQ MAPPING | 8 | id | Navigation and tracking; Operational and framework support |
| `trip_points` | RESQ MAPPING | 8 | id | Teams and rescue dispatch; Navigation and tracking |
| `trusted_households` | RESQ MAPPING | 11 | connection_id | Household and member safety |
| `urgency_levels` | RESQ MAPPING | 3 | urgency_id | Requests, reporting and archives |
| `user_notifications` | RESQ MAPPING | 9 | id | Radio and notifications |
| `users` | SHARED DEPENDENCY | 26 | user_id | Identity and account access; Household and member safety; Teams and rescue dispatch; Navigation and tracking; Radio and notifications; Requests, reporting and archives; Public inquiries and staff handling; Operational and framework support; Geography and household master data; Shared evacuation verification data |
| `v_household_status_board` | VIEW | 18 | none |  |
| `v_member_status_monitor` | VIEW | 49 | none |  |
| `vulnerable_groups` | SHARED DEPENDENCY | 3 | vulnerable_group_id | Household and member safety; Geography and household master data |
| `weather_logs` | RESQ MAPPING | 16 | weather_log_id | Radio and notifications; Disaster events, hazards and weather |
| `web_push_deliveries` | RESQ MAPPING | 4 | id | Radio and notifications |
| `web_push_subscriptions` | RESQ MAPPING | 9 | id | Radio and notifications |
| `zipcodes` | SHARED DEPENDENCY | 3 | zipcode_id | Geography and household master data |

## Enforced relationships

| Child columns | Parent columns | Symbols | Delete | Update | Constraint |
|---|---|---|---|---|---|
| accommodation_units.center_id | evacuation_centers.evacuation_center_id | `|o..o{` | CASCADE | CASCADE | fk_accomm_units_center |
| accommodation_units.type_id | accommodation_types.type_id | `|o..o{` | SET NULL | CASCADE | fk_accomm_units_type |
| addresses.barangay_id | barangays.barangay_id | `|o..o{` | SET NULL | CASCADE | fk_addresses_barangay |
| addresses.purok_id | puroks.purok_id | `|o..o{` | SET NULL | CASCADE | fk_addresses_purok |
| addresses.sitio_id | sitios.sitio_id | `|o..o{` | SET NULL | CASCADE | fk_addresses_sitio |
| addresses.zipcode_id | zipcodes.zipcode_id | `|o..o{` | SET NULL | CASCADE | fk_addresses_zipcode |
| affected_areas.barangay_id | barangays.barangay_id | `|o..o{` | SET NULL | CASCADE | fk_affected_areas_barangay |
| affected_areas.disaster_id | disaster_events.event_id | `|o..o{` | CASCADE | CASCADE | fk_affected_areas_disaster |
| affected_areas.purok_id | puroks.purok_id | `|o..o{` | SET NULL | CASCADE | fk_affected_areas_purok |
| affected_areas.severity_id | severity_levels.severity_id | `|o..o{` | SET NULL | CASCADE | fk_affected_areas_severity |
| affected_areas.sitio_id | sitios.sitio_id | `|o..o{` | SET NULL | CASCADE | fk_affected_areas_sitio |
| audit_logs.user_id | users.user_id | `|o..o{` | RESTRICT | RESTRICT | resq_7e9e267e7c9af499_fk |
| barangay_boundaries.barangay_id | barangays.barangay_id | `|o..o{` | SET NULL | CASCADE | fk_barangay_boundaries_barangay |
| barangays.city_id | cities.city_id | `||..o{` | RESTRICT | CASCADE | fk_barangays_city |
| cached_routes.evac_center_id | evacuation_centers.evacuation_center_id | `|o..o{` | CASCADE | NO ACTION | cached_routes_evac_center_id_foreign |
| cached_routes.household_id | households.household_id | `|o..o{` | CASCADE | NO ACTION | cached_routes_household_id_foreign |
| cached_routes.team_id | rescue_teams.team_id | `||..o{` | CASCADE | NO ACTION | cached_routes_team_id_foreign |
| cities.province_id | provinces.province_id | `||..o{` | RESTRICT | CASCADE | fk_cities_province |
| device_tokens.household_id | households.household_id | `|o..o{` | SET NULL | CASCADE | fk_device_tokens_household |
| device_tokens.member_id | household_members.member_id | `|o..o{` | SET NULL | CASCADE | fk_device_tokens_member |
| device_tokens.responder_id | responders.responder_id | `|o..o{` | SET NULL | CASCADE | fk_device_tokens_responder |
| device_tokens.team_id | rescue_teams.team_id | `|o..o{` | SET NULL | CASCADE | fk_device_tokens_team |
| device_tokens.user_id | users.user_id | `|o..o{` | SET NULL | CASCADE | fk_device_tokens_user |
| device_tokens.selection_token_id | personal_access_tokens.id | `|o..o{` | SET NULL | RESTRICT | resq_7e18a8a3a40fd914_fk |
| device_tracking_logs.household_id | households.household_id | `|o..o{` | SET NULL | CASCADE | fk_dev_tracking_household |
| device_tracking_logs.member_id | household_members.member_id | `|o..o{` | SET NULL | CASCADE | fk_dev_tracking_member |
| device_tracking_logs.device_token_id | device_tokens.id | `|o..o{` | SET NULL | CASCADE | fk_dev_tracking_token |
| disaster_broadcasts.disaster_id | disaster_events.event_id | `|o..o{` | SET NULL | CASCADE | fk_disaster_broadcasts_event |
| disaster_broadcasts.notification_id | notifications.notif_id | `|o..o{` | SET NULL | CASCADE | fk_disaster_broadcasts_notif |
| disaster_broadcasts.severity_id | severity_levels.severity_id | `|o..o{` | SET NULL | CASCADE | fk_disaster_broadcasts_severity |
| disaster_broadcasts.weather_log_id | weather_logs.weather_log_id | `|o..o{` | SET NULL | CASCADE | fk_disaster_broadcasts_weather |
| disaster_event_types.event_id | disaster_events.event_id | `|o..o{` | CASCADE | CASCADE | fk_det_event |
| disaster_event_types.type_id | disaster_types.type_id | `||..o{` | RESTRICT | CASCADE | fk_det_type |
| disaster_events.severity_level_id | severity_levels.severity_id | `|o..o{` | SET NULL | CASCADE | fk_disaster_events_severity |
| disaster_events.type_id | disaster_types.type_id | `||..o{` | RESTRICT | CASCADE | fk_disaster_events_type |
| dispatch_trips.device_id | device_tokens.id | `||..o{` | NO ACTION | NO ACTION | dispatch_trips_device_id_foreign |
| dispatch_trips.dispatch_id | responder_assignments.assignment_id | `||..o{` | NO ACTION | NO ACTION | dispatch_trips_dispatch_id_foreign |
| dispatch_trips.team_id | rescue_teams.team_id | `||..o{` | NO ACTION | NO ACTION | dispatch_trips_team_id_foreign |
| evacuation_centers.current_event_id | disaster_events.event_id | `|o..o{` | SET NULL | CASCADE | fk_evac_centers_event |
| evacuation_records.center_id | evacuation_centers.evacuation_center_id | `|o..o{` | CASCADE | CASCADE | fk_evac_records_center |
| evacuation_records.event_id | disaster_events.event_id | `|o..o{` | SET NULL | CASCADE | fk_evac_records_event |
| evacuation_records.household_id | households.household_id | `|o..o{` | CASCADE | CASCADE | fk_evac_records_household |
| evacuation_records.household_status_id | household_statuses.status_id | `|o..o{` | SET NULL | CASCADE | fk_evac_records_status |
| evacuation_records.verified_by | users.user_id | `|o..o{` | SET NULL | CASCADE | fk_evac_records_verifier |
| external_report_requests.event_id | disaster_events.event_id | `|o..o{` | RESTRICT | RESTRICT | resq_72e67152b620c50c_fk |
| geotagged_locations.household_id | households.household_id | `|o..o{` | CASCADE | CASCADE | fk_geo_household |
| geotagged_locations.verified_by_user_id | users.user_id | `|o..o{` | SET NULL | CASCADE | fk_geo_verified_by |
| household_disasters.disaster_id | disaster_events.event_id | `|o..o{` | NO ACTION | NO ACTION | fk_hd_event |
| household_disasters.household_id | households.household_id | `|o..o{` | NO ACTION | NO ACTION | fk_hd_household |
| household_disasters.initial_status_id | household_statuses.status_id | `|o..o{` | NO ACTION | NO ACTION | fk_hd_initial_status |
| household_disasters.current_status_id | household_statuses.status_id | `|o..o{` | NO ACTION | NO ACTION | fk_hd_status |
| household_geographic_classifications.household_id | households.household_id | `||--o|` | RESTRICT | RESTRICT | resq_22b65cda8c001677_fk |
| household_geographic_classifications.purok_id | puroks.purok_id | `|o..o{` | RESTRICT | RESTRICT | resq_79ef643b0ca93a73_fk |
| household_geographic_classifications.sitio_id | sitios.sitio_id | `|o..o{` | RESTRICT | RESTRICT | resq_99abdeb64f2c90cb_fk |
| household_members.civil_status_id | civil_statuses.status_id | `|o..o{` | SET NULL | CASCADE | fk_hm_civil_status |
| household_members.education_level_id | education_levels.education_level_id | `|o..o{` | SET NULL | CASCADE | fk_hm_education |
| household_members.gender_id | genders.gender_id | `|o..o{` | SET NULL | CASCADE | fk_hm_gender |
| household_members.household_id | households.household_id | `|o..o{` | CASCADE | CASCADE | fk_hm_household |
| household_members.occupation | occupations.occuaption_id | `|o..o{` | SET NULL | CASCADE | fk_hm_occupation |
| household_members.relationship_id | relationships.relationship_id | `|o..o{` | SET NULL | CASCADE | fk_hm_relationship |
| household_mobile_notifications.household_id | households.household_id | `||..o{` | RESTRICT | RESTRICT | resq_de2d65f74bfa2dd0_fk |
| household_status_logs.disaster_id | disaster_events.event_id | `|o..o{` | SET NULL | CASCADE | fk_hsl_event |
| household_status_logs.household_id | households.household_id | `||..o{` | CASCADE | CASCADE | fk_hsl_household |
| household_status_logs.status_id | household_statuses.status_id | `||..o{` | NO ACTION | NO ACTION | fk_hsl_status |
| household_trusted_pins.household_id | households.household_id | `||--o|` | CASCADE | CASCADE | fk_htp_household |
| households.address_id | addresses.address_id | `|o..o{` | SET NULL | CASCADE | fk_households_address |
| households.created_by | users.user_id | `|o..o{` | SET NULL | CASCADE | fk_households_created_by |
| households.login_user_id | users.user_id | `|o..o{` | SET NULL | CASCADE | fk_households_login_user |
| hq_field_reports.disaster_id | disaster_events.event_id | `|o..o{` | SET NULL | CASCADE | fk_hqfr_event |
| hq_field_reports.household_id | households.household_id | `|o..o{` | SET NULL | CASCADE | fk_hqfr_household |
| hq_field_reports.linked_report_id | responder_field_reports.report_id | `||..o{` | CASCADE | CASCADE | fk_hqfr_linked_report |
| incident_archives.archived_by_admin_id | users.user_id | `|o..o{` | RESTRICT | RESTRICT | resq_d85e1801ac3fda4f_fk |
| incident_archives.disaster_id | disaster_events.event_id | `|o..o{` | RESTRICT | RESTRICT | resq_f7d5b96efe64094f_fk |
| landing_inquiries.handled_by_user_id | users.user_id | `|o..o{` | RESTRICT | RESTRICT | resq_0e1dae93e28724cc_fk |
| mapping_hazard_layers.barangay_id | barangays.barangay_id | `||..o{` | RESTRICT | RESTRICT | resq_77025190d59483ff_fk |
| member_disaster_statuses.disaster_id | disaster_events.event_id | `||..o{` | NO ACTION | NO ACTION | fk_mds_event |
| member_disaster_statuses.household_id | households.household_id | `||..o{` | NO ACTION | NO ACTION | fk_mds_household |
| member_disaster_statuses.member_id | household_members.member_id | `||..o{` | NO ACTION | NO ACTION | fk_mds_member |
| member_disaster_statuses.previous_status_id | member_statuses.status_id | `|o..o{` | NO ACTION | NO ACTION | fk_mds_prev_status |
| member_disaster_statuses.status_id | member_statuses.status_id | `||..o{` | NO ACTION | NO ACTION | fk_mds_status |
| member_status_logs.responder_id | responders.responder_id | `|o..o{` | RESTRICT | RESTRICT | resq_1bb82f76ed97afd9_fk |
| member_status_logs.reported_by_member_id | household_members.member_id | `|o..o{` | RESTRICT | RESTRICT | resq_24280c3ab56db0ea_fk |
| member_status_logs.member_id | household_members.member_id | `||..o{` | RESTRICT | RESTRICT | resq_6978563e9169effa_fk |
| member_status_logs.from_status_id | member_statuses.status_id | `|o..o{` | RESTRICT | RESTRICT | resq_844996646fa2d02b_fk |
| member_status_logs.reported_by_user_id | users.user_id | `|o..o{` | RESTRICT | RESTRICT | resq_8e17c1f43c343e6b_fk |
| member_status_logs.device_token_id | device_tokens.id | `|o..o{` | RESTRICT | RESTRICT | resq_9ecdc0a83c933c65_fk |
| member_status_logs.to_status_id | member_statuses.status_id | `||..o{` | RESTRICT | RESTRICT | resq_c7815a85001a4c39_fk |
| member_status_logs.disaster_id | disaster_events.event_id | `||..o{` | RESTRICT | RESTRICT | resq_d1454f446a6c172a_fk |
| member_status_logs.household_id | households.household_id | `||..o{` | RESTRICT | RESTRICT | resq_e2907eafd56b71fb_fk |
| member_vulnerable_groups.vulnerable_group_id | vulnerable_groups.vulnerable_group_id | `||..o{` | CASCADE | CASCADE | fk_mvg_group |
| member_vulnerable_groups.member_id | household_members.member_id | `|o..o{` | CASCADE | CASCADE | fk_mvg_member |
| notifications.evacuation_center_id | evacuation_centers.evacuation_center_id | `|o..o{` | SET NULL | CASCADE | fk_notifications_center |
| notifications.evacuation_event_id | disaster_events.event_id | `|o..o{` | SET NULL | CASCADE | fk_notifications_event |
| notifications.recurrence_type_id | recurrence_types.type_id | `|o..o{` | SET NULL | CASCADE | fk_notifications_recurrence |
| notifications.sent_by | users.user_id | `|o..o{` | SET NULL | CASCADE | fk_notifications_sender |
| password_reset_requests.user_id | users.user_id | `|o..o{` | RESTRICT | RESTRICT | resq_2792ce2041a6b947_fk |
| password_reset_requests.household_id | households.household_id | `|o..o{` | RESTRICT | RESTRICT | resq_f282227758b5c771_fk |
| provinces.region_id | regions.region_id | `||..o{` | RESTRICT | CASCADE | fk_provinces_region |
| purok_boundaries.purok_id | puroks.purok_id | `||--o|` | RESTRICT | RESTRICT | resq_f1a504a4e34ddae2_fk |
| puroks.sitio_id | sitios.sitio_id | `||..o{` | RESTRICT | CASCADE | fk_puroks_sitio |
| remembered_devices.user_id | users.user_id | `||..o{` | RESTRICT | RESTRICT | resq_0e9a7f3f11c8990f_fk |
| request_validations.request_id | resource_requests.request_id | `||..o{` | CASCADE | CASCADE | fk_req_validations_request |
| request_validations.validator_user_id | users.user_id | `|o..o{` | SET NULL | CASCADE | fk_req_validations_validator |
| rescue_criteria_contact_baselines.event_id | disaster_events.event_id | `||--o{` | RESTRICT | RESTRICT | resq_6477cf95f637ff7a_fk |
| rescue_criteria_contact_baselines.household_id | households.household_id | `||--o{` | RESTRICT | RESTRICT | resq_6f1f8b058f28b61c_fk |
| rescue_criteria_line_snapshots.rescue_priority_version | rescue_priority_settings.version | `|o..o{` | RESTRICT | RESTRICT | resq_31d787d3b1908fca_fk |
| rescue_criteria_line_snapshots.event_id | disaster_events.event_id | `||..o{` | RESTRICT | RESTRICT | resq_bf9c5df1878e11ac_fk |
| rescue_criteria_snapshots.rescue_priority_version | rescue_priority_settings.version | `|o..o{` | RESTRICT | RESTRICT | resq_5a227d93d486e431_fk |
| rescue_criteria_snapshots.event_id | disaster_events.event_id | `||..o{` | RESTRICT | RESTRICT | resq_a925bd424181332c_fk |
| rescue_priority_settings.updated_by_user_id | users.user_id | `|o..o{` | RESTRICT | RESTRICT | resq_68ee510152684dbb_fk |
| rescue_teams.assigned_purok_id | puroks.purok_id | `|o..o{` | SET NULL | CASCADE | fk_rescue_teams_purok |
| rescue_teams.leader_responder_id | responders.responder_id | `|o..o{` | RESTRICT | RESTRICT | resq_b8b8912433edb420_fk |
| resource_requests.evacuation_center_id | evacuation_centers.evacuation_center_id | `|o..o{` | SET NULL | CASCADE | fk_rr_center |
| resource_requests.handled_by | users.user_id | `|o..o{` | SET NULL | CASCADE | fk_rr_handled_by |
| resource_requests.requested_by | users.user_id | `|o..o{` | SET NULL | CASCADE | fk_rr_requested_by |
| resource_requests.status_id | resource_request_status.status_id | `|o..o{` | SET NULL | CASCADE | fk_rr_status |
| resource_requests.validated_by_user_id | users.user_id | `|o..o{` | SET NULL | CASCADE | fk_rr_validated_by |
| resource_requests.urgency_id | urgency_levels.urgency_id | `|o..o{` | RESTRICT | NO ACTION | resource_requests_urgency_id_foreign |
| responder_assignments.disaster_id | disaster_events.event_id | `|o..o{` | SET NULL | CASCADE | fk_ra_disaster |
| responder_assignments.household_id | households.household_id | `|o..o{` | SET NULL | CASCADE | fk_ra_household |
| responder_assignments.responder_id | responders.responder_id | `||..o{` | RESTRICT | CASCADE | fk_ra_responder |
| responder_assignments.status | dispatch_statuses.status_key | `|o..o{` | SET NULL | CASCADE | fk_ra_status |
| responder_assignments.team_id | rescue_teams.team_id | `|o..o{` | SET NULL | CASCADE | fk_ra_team |
| responder_assignments.affected_area_id | affected_areas.affected_area_id | `|o..o{` | RESTRICT | RESTRICT | resq_4ed1f5a1527836f8_fk |
| responder_check_ins.disaster_id | disaster_events.event_id | `|o..o{` | SET NULL | CASCADE | fk_rci_disaster |
| responder_check_ins.household_id | households.household_id | `|o..o{` | SET NULL | CASCADE | fk_rci_household |
| responder_check_ins.responder_id | responders.responder_id | `||..o{` | CASCADE | CASCADE | fk_rci_responder |
| responder_check_ins.team_id | rescue_teams.team_id | `|o..o{` | SET NULL | CASCADE | fk_rci_team |
| responder_check_ins.member_id | household_members.member_id | `|o..o{` | RESTRICT | RESTRICT | resq_64f15fb7b5ec9834_fk |
| responder_check_ins.affected_area_id | affected_areas.affected_area_id | `|o..o{` | RESTRICT | RESTRICT | resq_d91b5f847846ce32_fk |
| responder_communication_logs.disaster_id | disaster_events.event_id | `|o..o{` | SET NULL | CASCADE | fk_rcl_disaster |
| responder_communication_logs.responder_id | responders.responder_id | `||..o{` | CASCADE | CASCADE | fk_rcl_responder |
| responder_communication_logs.team_id | rescue_teams.team_id | `|o..o{` | SET NULL | CASCADE | fk_rcl_team |
| responder_field_report_details.category_id | field_report_categories.category_id | `||..o{` | RESTRICT | CASCADE | fk_rfrd_category |
| responder_field_report_details.report_id | responder_field_reports.report_id | `||..o{` | CASCADE | CASCADE | fk_rfrd_report |
| responder_field_report_members.disaster_id | disaster_events.event_id | `||..o{` | CASCADE | CASCADE | fk_rfrm_disaster |
| responder_field_report_members.household_id | households.household_id | `||..o{` | CASCADE | CASCADE | fk_rfrm_household |
| responder_field_report_members.member_id | household_members.member_id | `||..o{` | CASCADE | CASCADE | fk_rfrm_member |
| responder_field_report_members.report_id | responder_field_reports.report_id | `||..o{` | CASCADE | CASCADE | fk_rfrm_report |
| responder_field_report_members.status_id | member_statuses.status_id | `|o..o{` | SET NULL | CASCADE | fk_rfrm_status |
| responder_field_reports.assignment_id | responder_assignments.assignment_id | `|o..o{` | SET NULL | CASCADE | fk_rfr_assignment |
| responder_field_reports.disaster_id | disaster_events.event_id | `|o..o{` | SET NULL | CASCADE | fk_rfr_disaster |
| responder_field_reports.household_id | households.household_id | `|o..o{` | SET NULL | CASCADE | fk_rfr_household |
| responder_field_reports.responder_id | responders.responder_id | `||..o{` | RESTRICT | CASCADE | fk_rfr_responder |
| responder_field_reports.property_damage | property_damage_levels.damage_key | `|o..o{` | RESTRICT | RESTRICT | resq_5bd01543efdb9459_fk |
| responder_field_reports.status_log_id | household_status_logs.status_log_id | `|o..o{` | RESTRICT | RESTRICT | resq_6beb664e75439fd1_fk |
| responder_location_logs.responder_id | responders.responder_id | `||..o{` | CASCADE | CASCADE | fk_rll_responder |
| responder_routes.assignment_id | responder_assignments.assignment_id | `||..o{` | CASCADE | CASCADE | fk_rr_route_assignment |
| responder_routes.household_id | households.household_id | `|o..o{` | SET NULL | CASCADE | fk_rr_route_household |
| responder_routes.responder_id | responders.responder_id | `|o..o{` | SET NULL | CASCADE | fk_rr_route_responder |
| responders.team_id | rescue_teams.team_id | `|o..o{` | SET NULL | CASCADE | fk_responders_team |
| responders.user_id | users.user_id | `|o..o{` | SET NULL | CASCADE | fk_responders_user |
| route_coordinates.route_id | responder_routes.route_id | `||..o{` | CASCADE | CASCADE | fk_route_coords_route |
| sitios.barangay_id | barangays.barangay_id | `||..o{` | RESTRICT | CASCADE | fk_sitios_barangay |
| situation_report_submissions.sit_rep_id | situation_reports.sit_rep_id | `||..o{` | RESTRICT | RESTRICT | resq_65e805833d7f909a_fk |
| situation_reports.disaster_id | disaster_events.event_id | `|o..o{` | SET NULL | CASCADE | fk_sitrep_disaster |
| situation_reports.household_id | households.household_id | `|o..o{` | SET NULL | CASCADE | fk_sitrep_household |
| status_reminders.event_id | disaster_events.event_id | `||..o{` | CASCADE | CASCADE | fk_status_reminders_event |
| status_reminders.household_id | households.household_id | `||..o{` | CASCADE | CASCADE | fk_status_reminders_household |
| status_reminders.member_id | household_members.member_id | `||..o{` | CASCADE | CASCADE | fk_status_reminders_member |
| sync_events.device_id | device_tokens.id | `||..o{` | CASCADE | NO ACTION | sync_events_device_id_foreign |
| trip_points.trip_id | dispatch_trips.id | `||..o{` | CASCADE | NO ACTION | trip_points_trip_id_foreign |
| trusted_households.requesting_household_id | households.household_id | `||..o{` | CASCADE | CASCADE | fk_trusted_hh_requesting |
| trusted_households.trusted_household_id | households.household_id | `||..o{` | CASCADE | CASCADE | fk_trusted_hh_trusted |
| user_notifications.user_id | users.user_id | `||..o{` | CASCADE | CASCADE | fk_user_notifications_user |
| users.assigned_center_id | evacuation_centers.evacuation_center_id | `|o..o{` | SET NULL | CASCADE | fk_users_assigned_center |
| users.household_id | households.household_id | `|o..o{` | SET NULL | CASCADE | fk_users_household |
| users.member_id | household_members.member_id | `|o..o|` | SET NULL | CASCADE | fk_users_member |
| users.role_id | roles.role_id | `|o..o{` | SET NULL | CASCADE | fk_users_role |
| weather_logs.disaster_id | disaster_events.event_id | `|o..o{` | SET NULL | CASCADE | fk_weather_logs_event |
| web_push_deliveries.subscription_id | web_push_subscriptions.id | `||..o{` | CASCADE | CASCADE | fk_web_push_deliveries_sub |
| web_push_subscriptions.user_id | users.user_id | `||..o{` | CASCADE | CASCADE | fk_web_push_subs_user |
| web_push_subscriptions.token_id | personal_access_tokens.id | `|o..o{` | SET NULL | RESTRICT | resq_e20d31d8baa70e39_fk |
| zipcodes.city_id | cities.city_id | `||..o{` | RESTRICT | CASCADE | fk_zipcodes_city |

## Excluded tables

Outside demonstrated current Resq query/model usage and its FK parent closure. This does not assign ownership to another team:

`analytics`, `analytics_job_logs`, `analytics_job_status`, `center_issue_categories`, `center_issue_report_statuses`, `center_issue_reports`, `csv_uploads`, `data_sources`, `evacuated_members`, `event_center_history`, `import_logs`, `inquiries`, `notification_channels`, `notification_logs`, `notification_recipients`, `notification_statuses`, `unit_allocations`

The separate inquiries table is unconfirmed; current Resq CRUD uses landing_inquiries.
