# Exact physical data dictionary

All full-ERD columns. Mermaid uses normalized types; actual MySQL types/nullability and composite unique groups are recorded here.

## _archive_orphan_household_disasters

LEGACY RECOVERY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `household_disaster_id` | `int` | NO | PK |
| `household_id` | `varchar(255)` | YES |  |
| `disaster_id` | `varchar(255)` | YES |  |
| `initial_status_id` | `int` | YES |  |
| `current_status_id` | `int` | YES |  |
| `last_status_source` | `varchar(50)` | YES |  |
| `last_status_notes` | `text` | YES |  |
| `last_reported_by_user_id` | `varchar(255)` | YES |  |
| `last_responder_id` | `int` | YES |  |
| `last_device_token_id` | `bigint` | YES |  |
| `last_latitude` | `decimal(10,7)` | YES |  |
| `last_longitude` | `decimal(10,7)` | YES |  |
| `last_battery_level` | `int` | YES |  |
| `last_reported_at` | `datetime` | YES |  |
| `priority_level` | `varchar(30)` | YES |  |
| `needs_dispatch` | `tinyint(1)` | NO |  |
| `updated_at` | `datetime` | YES |  |
| `created_at` | `datetime` | NO |  |

## _archive_orphan_household_status_logs

LEGACY RECOVERY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `status_log_id` | `int` | NO | PK |
| `disaster_id` | `varchar(255)` | YES |  |
| `household_id` | `varchar(255)` | NO |  |
| `status_id` | `int` | NO |  |
| `source` | `varchar(50)` | NO |  |
| `submitted_by_user_id` | `varchar(255)` | YES |  |
| `responder_id` | `int` | YES |  |
| `device_token_id` | `bigint` | YES |  |
| `latitude` | `decimal(10,7)` | YES |  |
| `longitude` | `decimal(10,7)` | YES |  |
| `location_label` | `varchar(255)` | YES |  |
| `location_accuracy_m` | `decimal(8,2)` | YES |  |
| `battery_level` | `int` | YES |  |
| `signal_strength` | `int` | YES |  |
| `notes` | `text` | YES |  |
| `submitted_at` | `datetime` | YES |  |
| `reviewed_by_user_id` | `varchar(255)` | YES |  |
| `reviewed_at` | `datetime` | YES |  |
| `created_at` | `datetime` | YES |  |
| `updated_at` | `datetime` | YES |  |

## accommodation_types

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `type_id` | `int` | NO | PK |
| `type_key` | `varchar(50)` | YES | UK |
| `type_label` | `varchar(100)` | YES |  |

## accommodation_units

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `unit_id` | `int` | NO | PK |
| `center_id` | `varchar(255)` | YES | FK |
| `name` | `varchar(100)` | YES |  |
| `type_id` | `int` | YES | FK |
| `max_capacity` | `int` | YES |  |
| `created_at` | `datetime` | YES |  |
| `deleted_at` | `datetime` | YES |  |

## addresses

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `address_id` | `int` | NO | PK |
| `street_address` | `int` | YES |  |
| `street` | `varchar(255)` | YES |  |
| `barangay_id` | `int` | YES | FK |
| `barangay_name` | `varchar(255)` | YES |  |
| `sitio_id` | `int` | YES | FK |
| `purok_sitio` | `varchar(255)` | YES |  |
| `house_number` | `varchar(255)` | YES |  |
| `purok_id` | `int` | YES | FK |
| `zipcode_id` | `int` | YES | FK |
| `zip_code` | `varchar(50)` | YES |  |
| `full_address` | `varchar(500)` | YES |  |
| `created_at` | `timestamp` | NO |  |
| `updated_at` | `timestamp` | YES |  |
| `deleted_at` | `timestamp` | YES |  |
| `is_apartment` | `tinyint(1)` | YES |  |
| `building_name` | `varchar(120)` | YES |  |
| `floor_number` | `varchar(30)` | YES |  |
| `unit_number` | `varchar(80)` | YES |  |
| `room_number` | `varchar(80)` | YES |  |
| `landmark` | `varchar(255)` | YES |  |

## affected_areas

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `affected_area_id` | `int` | NO | PK |
| `disaster_id` | `varchar(255)` | YES | FK |
| `confirmed_by_admin_id` | `varchar(255)` | YES |  |
| `severity_id` | `int` | YES | FK |
| `purok_id` | `int` | YES | FK |
| `sitio_id` | `int` | YES | FK |
| `barangay_id` | `int` | YES | FK |
| `confirmed_by_hq` | `tinyint(1)` | YES |  |
| `confirmed_at` | `datetime` | YES |  |

## audit_logs

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `audit_log_id` | `int` | NO | PK |
| `user_id` | `varchar(255)` | YES | FK |
| `role_key` | `varchar(50)` | YES |  |
| `module` | `varchar(80)` | NO |  |
| `action` | `varchar(80)` | NO |  |
| `reference_table` | `varchar(80)` | YES |  |
| `reference_id` | `varchar(255)` | YES |  |
| `old_values` | `json` | YES |  |
| `new_values` | `json` | YES |  |
| `ip_address` | `varchar(45)` | YES |  |
| `user_agent` | `varchar(255)` | YES |  |
| `created_at` | `datetime` | YES |  |

## barangay_boundaries

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `psgc_code` | `varchar(12)` | NO | PK |
| `barangay_id` | `int` | YES | FK |
| `barangay_code` | `varchar(12)` | YES |  |
| `barangay_name` | `varchar(100)` | NO |  |
| `city_name` | `varchar(100)` | NO |  |
| `geometry_json` | `longtext` | NO |  |
| `source_url` | `varchar(500)` | NO |  |
| `source_note` | `varchar(255)` | NO |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |

## barangays

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `barangay_id` | `int` | NO | PK |
| `barangay_code` | `varchar(20)` | YES | UK |
| `barangay_name` | `varchar(100)` | YES |  |
| `city_id` | `int` | NO | FK |

## cache

SHARED FRAMEWORK

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `key` | `varchar(255)` | NO | PK |
| `value` | `mediumtext` | NO |  |
| `expiration` | `bigint` | NO |  |

## cache_locks

SHARED FRAMEWORK

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `key` | `varchar(255)` | NO | PK |
| `owner` | `varchar(255)` | YES |  |
| `expiration` | `bigint` | NO |  |

## cached_routes

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `bigint unsigned` | NO | PK |
| `team_id` | `int` | NO | FK |
| `household_id` | `varchar(255)` | YES | FK |
| `evac_center_id` | `varchar(255)` | YES | FK |
| `target_key` | `varchar(300)` | NO |  |
| `profile` | `enum('auto','pedestrian')` | NO |  |
| `polyline6` | `longtext` | YES |  |
| `steps` | `json` | YES |  |
| `distance_m` | `int unsigned` | YES |  |
| `duration_s` | `int unsigned` | YES |  |
| `status` | `enum('ready','failed')` | NO |  |
| `failure_reason` | `varchar(255)` | YES |  |
| `computed_at` | `timestamp` | YES |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |

Composite unique groups; components are not individually unique:
- cached_routes_team_target_profile_unique: team_id, target_key, profile

## cities

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `city_id` | `int` | NO | PK |
| `city_code` | `varchar(20)` | YES | UK |
| `city_name` | `varchar(100)` | YES |  |
| `province_id` | `int` | NO | FK |

## civil_statuses

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `status_id` | `int` | NO | PK |
| `status_key` | `varchar(20)` | YES | UK |
| `status_label` | `varchar(100)` | YES |  |

## device_tokens

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `bigint` | NO | PK |
| `device_uuid` | `varchar(150)` | YES |  |
| `household_id` | `varchar(255)` | YES | FK |
| `member_id` | `varchar(255)` | YES | FK |
| `device_name` | `varchar(100)` | YES |  |
| `platform` | `varchar(30)` | YES |  |
| `app_role` | `varchar(30)` | YES |  |
| `push_provider` | `varchar(50)` | YES |  |
| `player_id` | `varchar(255)` | YES |  |
| `expo_push_token` | `varchar(255)` | YES |  |
| `battery_level` | `int` | YES |  |
| `signal_strength` | `int` | YES |  |
| `location_permission_status` | `varchar(30)` | NO |  |
| `notification_permission_status` | `varchar(30)` | NO |  |
| `last_latitude` | `decimal(10,7)` | YES |  |
| `last_longitude` | `decimal(10,7)` | YES |  |
| `last_location_label` | `varchar(255)` | YES |  |
| `last_location_accuracy_m` | `decimal(8,2)` | YES |  |
| `last_location_at` | `datetime` | YES |  |
| `last_seen_at` | `datetime` | YES |  |
| `is_active` | `tinyint(1)` | NO |  |
| `logged_at` | `datetime` | YES |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |
| `user_id` | `varchar(255)` | YES | FK |
| `team_id` | `int` | YES | FK |
| `last_sync_at` | `timestamp` | YES |  |
| `selection_token_id` | `bigint unsigned` | YES | FK |
| `owner_selected_at` | `timestamp` | YES |  |
| `push_token` | `varchar(255)` | YES |  |
| `one_signal_user_id` | `varchar(255)` | YES |  |
| `responder_id` | `int` | YES | FK |

## device_tracking_logs

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `tracking_id` | `int` | NO | PK |
| `device_token_id` | `bigint` | YES | FK |
| `household_id` | `varchar(255)` | YES | FK |
| `member_id` | `varchar(255)` | YES | FK |
| `latitude` | `decimal(10,7)` | YES |  |
| `longitude` | `decimal(10,7)` | YES |  |
| `location_label` | `varchar(255)` | YES |  |
| `accuracy_m` | `decimal(8,2)` | YES |  |
| `location_source` | `varchar(50)` | YES |  |
| `is_allowed_location` | `tinyint(1)` | NO |  |
| `battery_level` | `int` | YES |  |
| `signal_strength` | `int` | YES |  |
| `logged_at` | `datetime` | NO |  |

## disaster_broadcasts

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `broadcast_id` | `int` | NO | PK |
| `broadcast_title` | `varchar(150)` | YES |  |
| `disaster_id` | `varchar(255)` | YES | FK |
| `sent_by_admin_id` | `varchar(255)` | YES |  |
| `severity_id` | `int` | YES | FK |
| `scope_type` | `varchar(50)` | YES |  |
| `target_purok_id` | `int` | YES |  |
| `target_area_id` | `int` | YES |  |
| `message` | `text` | YES |  |
| `allowed_statuses` | `varchar(255)` | YES |  |
| `channel` | `varchar(50)` | YES |  |
| `status` | `varchar(50)` | NO |  |
| `notification_id` | `int` | YES | FK |
| `weather_log_id` | `int` | YES | FK |
| `sent_at` | `datetime` | NO |  |
| `created_at` | `datetime` | YES |  |
| `updated_at` | `datetime` | YES |  |
| `target_area_label` | `varchar(150)` | YES |  |
| `direct_impact_puroks_json` | `json` | YES |  |
| `allowed_statuses_json` | `json` | YES |  |
| `recipient_count` | `int` | YES |  |
| `push_status` | `varchar(50)` | YES |  |
| `sms_status` | `varchar(50)` | YES |  |
| `status_options_json` | `text` | YES |  |
| `push_provider_ids_json` | `json` | YES |  |
| `push_errors_json` | `json` | YES |  |
| `push_accepted_count` | `int unsigned` | YES |  |
| `onesignal_id` | `varchar(36)` | YES |  |

## disaster_event_types

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `event_type_id` | `int` | NO | PK |
| `event_id` | `varchar(255)` | YES | FK |
| `type_id` | `int` | NO | FK |

Composite unique groups; components are not individually unique:
- uk_disaster_event_types_pair: event_id, type_id

## disaster_events

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `event_id` | `varchar(255)` | NO | PK |
| `name` | `varchar(100)` | YES |  |
| `type_id` | `int` | NO | FK |
| `severity_level_id` | `int` | YES | FK |
| `started_at` | `datetime` | YES |  |
| `ended_at` | `datetime` | YES |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |
| `deleted_at` | `timestamp` | YES |  |
| `rescue_priority_version` | `bigint unsigned` | YES |  |

## disaster_types

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `type_id` | `int` | NO | PK |
| `type_code` | `varchar(20)` | YES | UK |
| `type_name` | `varchar(100)` | YES |  |
| `is_active` | `tinyint(1)` | YES |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |
| `deleted_at` | `timestamp` | YES |  |

## dispatch_statuses

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `status_key` | `varchar(50)` | NO | PK |
| `label` | `varchar(100)` | NO |  |
| `is_open` | `tinyint(1)` | NO |  |
| `allow_create` | `tinyint(1)` | NO |  |
| `allow_mobile` | `tinyint(1)` | NO |  |
| `dashboard_group` | `varchar(30)` | NO |  |
| `is_alias` | `tinyint(1)` | NO |  |
| `is_active` | `tinyint(1)` | NO |  |
| `sort_order` | `int unsigned` | NO |  |
| `status_code` | `varchar(20)` | NO | UK |

## dispatch_trips

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `bigint unsigned` | NO | PK |
| `dispatch_id` | `int` | NO | FK |
| `team_id` | `int` | NO | FK |
| `device_id` | `bigint` | NO | FK |
| `profile` | `enum('auto','pedestrian')` | NO |  |
| `started_at` | `datetime` | NO |  |
| `ended_at` | `datetime` | YES |  |
| `distance_m` | `int unsigned` | YES |  |
| `planned_distance_m` | `int unsigned` | YES |  |
| `moving_s` | `int unsigned` | NO |  |
| `stopped_s` | `int unsigned` | NO |  |
| `avg_speed_ms` | `decimal(8,3)` | YES |  |
| `status` | `enum('recording','completed','abandoned')` | NO |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |

## education_levels

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `education_level_id` | `int` | NO | PK |
| `education_level_key` | `varchar(20)` | YES | UK |
| `education_level_label` | `varchar(100)` | YES |  |

## evacuation_centers

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `evacuation_center_id` | `varchar(255)` | NO | PK |
| `current_event_id` | `varchar(255)` | YES | FK |
| `name` | `varchar(100)` | YES |  |
| `center_type` | `varchar(80)` | YES |  |
| `latitude` | `decimal(10,7)` | YES |  |
| `longitude` | `decimal(10,7)` | YES |  |
| `capacity` | `int` | YES |  |
| `status` | `varchar(30)` | NO |  |
| `current_occupancy` | `int` | YES |  |
| `contact_person` | `varchar(150)` | YES |  |
| `contact_number` | `varchar(30)` | YES |  |
| `created_at` | `datetime` | YES |  |
| `deleted_at` | `datetime` | YES |  |
| `osm_address` | `varchar(255)` | YES |  |
| `notes` | `text` | YES |  |
| `updated_at` | `datetime` | YES |  |

## evacuation_records

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `evacuation_id` | `int` | NO | PK |
| `event_id` | `varchar(255)` | YES | FK |
| `household_id` | `varchar(255)` | YES | FK |
| `center_id` | `varchar(255)` | YES | FK |
| `household_status_id` | `int` | YES | FK |
| `evacuated_count` | `int` | YES |  |
| `method` | `enum('qr','manual')` | YES |  |
| `verified_by` | `varchar(255)` | YES | FK |
| `verified_at` | `datetime` | YES |  |
| `created_at` | `datetime` | YES |  |
| `updated_at` | `datetime` | YES |  |

## external_report_requests

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `char(36)` | NO | PK |
| `source_system` | `varchar(40)` | NO |  |
| `reference` | `varchar(120)` | YES |  |
| `event_id` | `varchar(255)` | YES | FK |
| `sections` | `json` | NO |  |
| `format` | `varchar(8)` | NO |  |
| `purpose` | `text` | NO |  |
| `status` | `varchar(16)` | NO |  |
| `decision_note` | `text` | YES |  |
| `decided_by` | `varchar(150)` | YES |  |
| `decided_at` | `timestamp` | YES |  |
| `approved_summary` | `json` | YES |  |
| `file` | `json` | YES |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |
| `api_version` | `varchar(8)` | NO |  |
| `sitio_id` | `varchar(120)` | YES |  |

## failed_jobs

SHARED FRAMEWORK

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `bigint unsigned` | NO | PK |
| `uuid` | `varchar(255)` | YES | UK |
| `connection` | `text` | NO |  |
| `queue` | `text` | NO |  |
| `payload` | `longtext` | NO |  |
| `exception` | `longtext` | NO |  |
| `failed_at` | `timestamp` | NO |  |

## field_report_categories

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `category_id` | `int` | NO | PK |
| `category_key` | `varchar(50)` | YES | UK |
| `category_label` | `varchar(100)` | YES |  |

## genders

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `gender_id` | `int` | NO | PK |
| `gender_key` | `varchar(20)` | YES | UK |
| `gender_label` | `varchar(20)` | YES |  |

## geotagged_locations

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `location_id` | `int` | NO | PK |
| `household_id` | `varchar(255)` | YES | FK |
| `latitude` | `decimal(10,7)` | YES |  |
| `longitude` | `decimal(10,7)` | YES |  |
| `location_label` | `varchar(255)` | YES |  |
| `accuracy_m` | `decimal(8,2)` | YES |  |
| `geotag_source` | `varchar(50)` | NO |  |
| `is_verified` | `tinyint(1)` | NO |  |
| `verified_by_user_id` | `varchar(255)` | YES | FK |
| `verified_at` | `datetime` | YES |  |
| `created_at` | `datetime` | YES |  |
| `updated_at` | `datetime` | NO |  |

## household_disasters

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `household_disaster_id` | `int` | NO | PK |
| `household_id` | `varchar(255)` | YES | FK |
| `disaster_id` | `varchar(255)` | YES | FK |
| `initial_status_id` | `int` | YES | FK |
| `current_status_id` | `int` | YES | FK |
| `last_status_source` | `varchar(50)` | YES |  |
| `last_status_notes` | `text` | YES |  |
| `last_reported_by_user_id` | `varchar(255)` | YES |  |
| `last_responder_id` | `int` | YES |  |
| `last_device_token_id` | `bigint` | YES |  |
| `last_latitude` | `decimal(10,7)` | YES |  |
| `last_longitude` | `decimal(10,7)` | YES |  |
| `last_battery_level` | `int` | YES |  |
| `last_reported_at` | `datetime` | YES |  |
| `priority_level` | `varchar(30)` | YES |  |
| `needs_dispatch` | `tinyint(1)` | NO |  |
| `updated_at` | `datetime` | YES |  |
| `created_at` | `datetime` | NO |  |

Composite unique groups; components are not individually unique:
- uk_hd_event_household: disaster_id, household_id

## household_geographic_classifications

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `household_id` | `varchar(255)` | NO | PK,FK |
| `status` | `varchar(50)` | NO |  |
| `latitude` | `decimal(10,7)` | NO |  |
| `longitude` | `decimal(10,7)` | NO |  |
| `sitio_id` | `int` | YES | FK |
| `purok_id` | `int` | YES | FK |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |

## household_members

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `member_id` | `varchar(255)` | NO | PK |
| `household_id` | `varchar(255)` | YES | FK |
| `first_name` | `varchar(100)` | YES |  |
| `middle_name` | `varchar(100)` | YES |  |
| `last_name` | `varchar(100)` | YES |  |
| `birth_date` | `date` | NO |  |
| `gender_id` | `int` | YES | FK |
| `relationship_id` | `int` | YES | FK |
| `is_household_head` | `tinyint(1)` | NO |  |
| `can_report_for_household` | `tinyint(1)` | NO |  |
| `contact_number` | `varchar(50)` | YES |  |
| `civil_status_id` | `int` | YES | FK |
| `occupation` | `int` | YES | FK |
| `education_level_id` | `int` | YES | FK |
| `is_graduate` | `tinyint(1)` | YES |  |
| `deleted_at` | `timestamp` | YES |  |
| `is_pwd` | `tinyint(1)` | NO |  |
| `is_senior` | `tinyint(1)` | NO |  |
| `is_pregnant` | `tinyint(1)` | NO |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |
| `name` | `varchar(255)` | YES |  |
| `sex` | `varchar(1)` | YES |  |
| `gender` | `varchar(20)` | YES |  |
| `relation` | `varchar(50)` | YES |  |
| `civil_status` | `varchar(50)` | YES |  |
| `religion` | `varchar(100)` | YES |  |
| `education_level` | `varchar(100)` | YES |  |
| `special_needs` | `varchar(50)` | YES |  |
| `legacy_member_id` | `varchar(255)` | YES |  |

## household_mobile_notifications

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `notification_id` | `bigint unsigned` | NO | PK |
| `household_id` | `varchar(255)` | NO | FK |
| `type` | `varchar(80)` | NO |  |
| `title` | `varchar(180)` | NO |  |
| `message` | `text` | NO |  |
| `connection_id` | `varchar(100)` | YES |  |
| `read_at` | `timestamp` | YES |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |

## household_status_logs

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `status_log_id` | `int` | NO | PK |
| `disaster_id` | `varchar(255)` | YES | FK |
| `household_id` | `varchar(255)` | NO | FK |
| `status_id` | `int` | NO | FK |
| `source` | `varchar(50)` | NO |  |
| `submitted_by_user_id` | `varchar(255)` | YES |  |
| `responder_id` | `int` | YES |  |
| `device_token_id` | `bigint` | YES |  |
| `latitude` | `decimal(10,7)` | YES |  |
| `longitude` | `decimal(10,7)` | YES |  |
| `location_label` | `varchar(255)` | YES |  |
| `location_accuracy_m` | `decimal(8,2)` | YES |  |
| `battery_level` | `int` | YES |  |
| `signal_strength` | `int` | YES |  |
| `notes` | `text` | YES |  |
| `submitted_at` | `datetime` | YES |  |
| `reviewed_by_user_id` | `varchar(255)` | YES |  |
| `reviewed_at` | `datetime` | YES |  |
| `created_at` | `datetime` | YES |  |
| `updated_at` | `datetime` | YES |  |

## household_statuses

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `status_id` | `int` | NO | PK |
| `status_key` | `varchar(50)` | YES | UK |
| `status_label` | `varchar(100)` | YES |  |
| `severity_rank` | `tinyint unsigned` | NO |  |
| `requires_rescue` | `tinyint(1)` | NO |  |
| `color_hex` | `varchar(7)` | YES |  |
| `sort_order` | `smallint unsigned` | NO |  |
| `is_active` | `tinyint(1)` | NO |  |
| `safety_basis` | `varchar(6)` | YES |  |

## household_trusted_pins

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `household_id` | `varchar(255)` | NO | PK,FK |
| `pin_hash` | `varchar(255)` | NO |  |
| `updated_by_user_id` | `varchar(255)` | YES |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |

## households

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `household_id` | `varchar(255)` | NO | PK |
| `household_code` | `varchar(255)` | YES | UK |
| `household_number` | `varchar(255)` | YES |  |
| `household_name` | `varchar(100)` | YES |  |
| `email` | `varchar(255)` | YES |  |
| `member_count` | `int unsigned` | NO |  |
| `created_by` | `varchar(255)` | YES | FK |
| `address_id` | `int` | YES | FK |
| `contact_number` | `varchar(50)` | YES |  |
| `emergency_contact` | `varchar(50)` | YES |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |
| `deleted_at` | `timestamp` | YES |  |
| `login_user_id` | `varchar(255)` | YES | FK |

## hq_field_reports

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `hq_report_id` | `int` | NO | PK |
| `disaster_id` | `varchar(255)` | YES | FK |
| `household_id` | `varchar(255)` | YES | FK |
| `source` | `varchar(20)` | YES |  |
| `linked_report_id` | `int` | NO | FK |
| `created_at` | `datetime` | NO |  |

## incident_archives

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `archive_id` | `int` | NO | PK |
| `archive_type` | `varchar(50)` | YES |  |
| `disaster_id` | `varchar(255)` | YES | FK |
| `reference_table` | `varchar(80)` | YES |  |
| `reference_id` | `varchar(255)` | YES |  |
| `archived_by_admin_id` | `varchar(255)` | YES | FK |
| `archive_note` | `text` | YES |  |
| `archived_at` | `datetime` | NO |  |
| `created_at` | `datetime` | YES |  |

## job_batches

SHARED FRAMEWORK

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `varchar(255)` | NO | PK |
| `name` | `varchar(255)` | YES |  |
| `total_jobs` | `int` | NO |  |
| `pending_jobs` | `int` | NO |  |
| `failed_jobs` | `int` | NO |  |
| `failed_job_ids` | `longtext` | NO |  |
| `options` | `mediumtext` | YES |  |
| `cancelled_at` | `int` | YES |  |
| `created_at` | `int` | NO |  |
| `finished_at` | `int` | YES |  |

## jobs

SHARED FRAMEWORK

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `bigint unsigned` | NO | PK |
| `queue` | `varchar(255)` | YES |  |
| `payload` | `longtext` | NO |  |
| `attempts` | `tinyint unsigned` | NO |  |
| `reserved_at` | `int unsigned` | YES |  |
| `available_at` | `int unsigned` | NO |  |
| `created_at` | `int unsigned` | NO |  |

## landing_inquiries

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `inquiry_id` | `bigint unsigned` | NO | PK |
| `name` | `varchar(150)` | NO |  |
| `organization` | `varchar(150)` | YES |  |
| `email` | `varchar(255)` | YES |  |
| `message` | `text` | NO |  |
| `status` | `varchar(30)` | NO |  |
| `source_page` | `varchar(80)` | NO |  |
| `ip_address` | `varchar(80)` | YES |  |
| `user_agent` | `varchar(255)` | YES |  |
| `responded_at` | `timestamp` | YES |  |
| `handled_by_user_id` | `varchar(255)` | YES | FK |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |

## map_tile_metadata

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `tile_id` | `int` | NO | PK |
| `zoom_level` | `int` | NO |  |
| `tile_x` | `int` | NO |  |
| `tile_y` | `int` | NO |  |
| `tile_url` | `varchar(500)` | YES |  |
| `cached_at` | `datetime` | NO |  |
| `expires_at` | `datetime` | YES |  |

Composite unique groups; components are not individually unique:
- uk_map_tile_zxy: zoom_level, tile_x, tile_y

## mapping_hazard_layers

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `bigint unsigned` | NO | PK |
| `barangay_id` | `int` | NO | FK |
| `name` | `varchar(255)` | NO |  |
| `source` | `varchar(255)` | NO |  |
| `source_url` | `varchar(255)` | YES |  |
| `assessed_at` | `date` | NO |  |
| `geojson` | `json` | NO |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |

## member_disaster_statuses

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `member_status_id` | `bigint` | NO | PK |
| `disaster_id` | `varchar(255)` | NO | FK |
| `household_id` | `varchar(255)` | NO | FK |
| `member_id` | `varchar(255)` | NO | FK |
| `status_id` | `int` | NO | FK |
| `previous_status_id` | `int` | YES | FK |
| `report_source` | `enum('self','household_head','proxy_member','responder','hq','sms','system')` | NO |  |
| `reported_by_user_id` | `varchar(255)` | YES |  |
| `reported_by_member_id` | `varchar(255)` | YES |  |
| `responder_id` | `int` | YES |  |
| `device_token_id` | `bigint` | YES |  |
| `latitude` | `decimal(10,7)` | YES |  |
| `longitude` | `decimal(10,7)` | YES |  |
| `location_label` | `varchar(255)` | YES |  |
| `location_accuracy_m` | `decimal(8,2)` | YES |  |
| `battery_level` | `int` | YES |  |
| `signal_strength` | `int` | YES |  |
| `evacuation_center_id` | `varchar(255)` | YES |  |
| `needs_rescue` | `tinyint(1)` | NO |  |
| `severity_rank` | `tinyint unsigned` | NO |  |
| `priority_level` | `enum('low','medium','high','critical')` | NO |  |
| `notes` | `text` | YES |  |
| `is_verified` | `tinyint(1)` | NO |  |
| `verified_by_user_id` | `varchar(255)` | YES |  |
| `verified_at` | `datetime` | YES |  |
| `reported_at` | `datetime` | YES |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |

Composite unique groups; components are not individually unique:
- uk_mds_event_member: disaster_id, member_id

## member_status_logs

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `member_status_log_id` | `bigint` | NO | PK |
| `disaster_id` | `varchar(255)` | NO | FK |
| `household_id` | `varchar(255)` | NO | FK |
| `member_id` | `varchar(255)` | NO | FK |
| `from_status_id` | `int` | YES | FK |
| `to_status_id` | `int` | NO | FK |
| `report_source` | `varchar(30)` | NO |  |
| `reported_by_user_id` | `varchar(255)` | YES | FK |
| `reported_by_member_id` | `varchar(255)` | YES | FK |
| `responder_id` | `int` | YES | FK |
| `device_token_id` | `bigint` | YES | FK |
| `latitude` | `decimal(10,7)` | YES |  |
| `longitude` | `decimal(10,7)` | YES |  |
| `location_label` | `varchar(255)` | YES |  |
| `location_accuracy_m` | `decimal(8,2)` | YES |  |
| `battery_level` | `int` | YES |  |
| `signal_strength` | `int` | YES |  |
| `notes` | `text` | YES |  |
| `reported_at` | `datetime` | YES |  |
| `logged_at` | `timestamp` | YES |  |

## member_statuses

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `status_id` | `int` | NO | PK |
| `status_key` | `varchar(50)` | NO | UK |
| `status_label` | `varchar(100)` | NO |  |
| `description` | `varchar(255)` | YES |  |
| `severity_rank` | `tinyint unsigned` | NO |  |
| `requires_rescue` | `tinyint(1)` | NO |  |
| `is_terminal` | `tinyint(1)` | NO |  |
| `color_hex` | `varchar(7)` | YES |  |
| `sort_order` | `smallint unsigned` | NO |  |
| `is_active` | `tinyint(1)` | NO |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |
| `counts_as_death` | `tinyint(1)` | YES |  |
| `counts_as_injury` | `tinyint(1)` | YES |  |

## member_vulnerable_groups

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `int` | NO | PK |
| `member_id` | `varchar(255)` | YES | FK |
| `vulnerable_group_id` | `int` | NO | FK |

Composite unique groups; components are not individually unique:
- uk_mvg_member_group: member_id, vulnerable_group_id

## migrations

SHARED FRAMEWORK

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `int unsigned` | NO | PK |
| `migration` | `varchar(255)` | YES |  |
| `batch` | `int` | NO |  |

## notifications

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `notif_id` | `int` | NO | PK |
| `message` | `text` | YES |  |
| `sent_by` | `varchar(255)` | YES | FK |
| `evacuation_event_id` | `varchar(255)` | YES | FK |
| `evacuation_center_id` | `varchar(255)` | YES | FK |
| `scheduled_at` | `datetime` | YES |  |
| `is_recurring` | `tinyint(1)` | YES |  |
| `recurrence_type_id` | `int` | YES | FK |
| `recurrence_end_at` | `datetime` | YES |  |
| `last_sent_at` | `datetime` | YES |  |
| `created_at` | `datetime` | YES |  |
| `channel` | `varchar(50)` | YES |  |
| `status` | `varchar(50)` | YES |  |
| `target_filter` | `varchar(50)` | YES |  |
| `source_key` | `varchar(120)` | YES | UK |
| `onesignal_id` | `varchar(36)` | YES |  |
| `onesignal_ids_json` | `json` | YES |  |
| `feed_payload_json` | `json` | YES |  |
| `advisory_source` | `varchar(16)` | YES |  |
| `advisory_fingerprint` | `varchar(64)` | YES | UK |
| `advisory_title` | `varchar(255)` | YES |  |
| `advisory_source_url` | `text` | YES |  |

## occupations

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `occuaption_id` | `int` | NO | PK |
| `occupation_id` | `int` | YES |  |
| `occupation_name` | `varchar(100)` | YES |  |

## offline_packs

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `version` | `varchar(64)` | NO | PK |
| `bbox` | `json` | NO |  |
| `style_url` | `varchar(500)` | NO |  |
| `size_bytes` | `bigint unsigned` | NO |  |
| `checksum` | `char(64)` | NO |  |
| `is_active` | `tinyint(1)` | NO |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |
| `pack_format` | `varchar(32)` | NO |  |

## operational_sequences

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `sequence_key` | `varchar(255)` | NO | PK |
| `next_value` | `bigint unsigned` | NO |  |
| `sequence_prefix` | `varchar(120)` | YES |  |

## password_reset_requests

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `request_id` | `char(36)` | NO | PK |
| `user_id` | `varchar(255)` | YES | FK |
| `login_value` | `varchar(255)` | YES |  |
| `verification_method` | `enum('previous_password','security_questions','sms_otp')` | NO |  |
| `token_hash` | `varchar(255)` | YES | UK |
| `failed_attempts` | `tinyint unsigned` | NO |  |
| `expires_at` | `timestamp` | NO |  |
| `verified_at` | `timestamp` | YES |  |
| `consumed_at` | `timestamp` | YES |  |
| `requested_ip` | `varchar(45)` | YES |  |
| `user_agent` | `text` | YES |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |
| `otp_subject_key` | `char(64)` | YES | UK |
| `household_id` | `varchar(255)` | YES | FK |
| `code_hash` | `varchar(255)` | YES |  |
| `sent_at` | `timestamp` | YES |  |

## password_reset_tokens

SHARED FRAMEWORK

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `email` | `varchar(255)` | NO | PK |
| `token` | `varchar(255)` | NO |  |
| `created_at` | `timestamp` | YES |  |

## personal_access_tokens

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `bigint unsigned` | NO | PK |
| `tokenable_id` | `varchar(255)` | YES |  |
| `tokenable_type` | `varchar(255)` | YES |  |
| `name` | `text` | NO |  |
| `token` | `varchar(64)` | YES | UK |
| `abilities` | `text` | YES |  |
| `last_used_at` | `timestamp` | YES |  |
| `expires_at` | `timestamp` | YES |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |

## property_damage_levels

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `damage_key` | `varchar(80)` | NO | PK |
| `label` | `varchar(255)` | NO |  |
| `sort_order` | `int unsigned` | NO |  |
| `is_active` | `tinyint(1)` | NO |  |

## provinces

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `province_id` | `int` | NO | PK |
| `province_code` | `varchar(20)` | YES | UK |
| `province_name` | `varchar(100)` | YES |  |
| `region_id` | `int` | NO | FK |

## purok_boundaries

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `purok_id` | `int` | NO | PK,FK |
| `geometry_json` | `longtext` | NO |  |
| `source` | `text` | NO |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |

## puroks

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `purok_id` | `int` | NO | PK |
| `purok_name` | `varchar(100)` | YES |  |
| `sitio_id` | `int` | NO | FK |

## realtime_outbox

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `bigint unsigned` | NO | PK |
| `topics` | `text` | NO |  |
| `available_at` | `int unsigned` | NO |  |
| `claim_token` | `char(36)` | YES |  |
| `claimed_until` | `int unsigned` | YES |  |
| `attempts` | `int unsigned` | NO |  |
| `created_at` | `timestamp` | NO |  |
| `delivered_at` | `timestamp` | YES |  |

## recurrence_types

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `type_id` | `int` | NO | PK |
| `type_key` | `varchar(50)` | YES | UK |
| `type_label` | `varchar(100)` | YES |  |

## regions

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `region_id` | `int` | NO | PK |
| `region_code` | `varchar(20)` | YES | UK |
| `region_name` | `varchar(100)` | YES |  |

## relationships

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `relationship_id` | `int` | NO | PK |
| `relationship_key` | `varchar(50)` | YES | UK |
| `relationship_label` | `varchar(100)` | YES |  |
| `is_head` | `tinyint(1)` | NO |  |
| `is_immediate_family` | `tinyint(1)` | NO |  |
| `can_report_for_household` | `tinyint(1)` | NO |  |
| `sort_order` | `smallint unsigned` | NO |  |
| `is_active` | `tinyint(1)` | NO |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |

## remembered_devices

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `remembered_device_id` | `char(36)` | NO | PK |
| `user_id` | `varchar(255)` | NO | FK |
| `token_hash` | `varchar(255)` | NO | UK |
| `device_name` | `varchar(150)` | YES |  |
| `platform` | `varchar(30)` | YES |  |
| `ip_address` | `varchar(45)` | YES |  |
| `user_agent` | `text` | YES |  |
| `last_used_at` | `timestamp` | YES |  |
| `expires_at` | `timestamp` | NO |  |
| `revoked_at` | `timestamp` | YES |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |

## report_idempotency

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `scope` | `char(64)` | NO | PK |
| `request_hash` | `char(64)` | NO |  |
| `response_status` | `smallint unsigned` | YES |  |
| `response_body` | `longtext` | YES |  |
| `content_type` | `varchar(255)` | YES |  |
| `created_at` | `timestamp` | NO |  |
| `expires_at` | `timestamp` | NO |  |

## request_validations

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `validation_id` | `int` | NO | PK |
| `request_id` | `varchar(255)` | NO | FK |
| `validation_status` | `varchar(30)` | NO |  |
| `validator_user_id` | `varchar(255)` | YES | FK |
| `validation_notes` | `text` | YES |  |
| `missing_information` | `text` | YES |  |
| `duplicate_request_id` | `varchar(255)` | YES |  |
| `validated_at` | `datetime` | YES |  |
| `created_at` | `datetime` | YES |  |
| `updated_at` | `datetime` | YES |  |

## rescue_criteria_contact_baselines

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `event_id` | `varchar(255)` | NO | PK,FK |
| `household_id` | `varchar(255)` | NO | PK,FK |
| `no_contact` | `tinyint(1)` | NO |  |
| `captured_at` | `timestamp` | NO |  |

Composite unique groups; components are not individually unique:
- PRIMARY: event_id, household_id

## rescue_criteria_line_snapshots

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `bigint unsigned` | NO | PK |
| `event_id` | `varchar(255)` | NO | FK |
| `bucket_hour` | `int unsigned` | NO |  |
| `observed_at` | `timestamp` | NO |  |
| `impact_open` | `int unsigned` | NO |  |
| `household_total` | `int unsigned` | NO |  |
| `special_open` | `int unsigned` | NO |  |
| `vulnerable_total` | `int unsigned` | NO |  |
| `unreported_open` | `int unsigned` | NO |  |
| `member_total` | `int unsigned` | NO |  |
| `no_contact_open` | `int unsigned` | NO |  |
| `no_contact_total` | `int unsigned` | NO |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |
| `rescue_priority_version` | `bigint unsigned` | YES | FK |

Composite unique groups; components are not individually unique:
- rescue_criteria_event_bucket_unique: event_id, bucket_hour

## rescue_criteria_snapshots

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `bigint unsigned` | NO | PK |
| `event_id` | `varchar(255)` | NO | FK |
| `observed_at` | `timestamp` | NO |  |
| `impact` | `decimal(5,1)` | YES |  |
| `special_needs` | `decimal(5,1)` | YES |  |
| `unreported` | `decimal(5,1)` | YES |  |
| `no_contact` | `decimal(5,1)` | YES |  |
| `purok_count` | `int unsigned` | NO |  |
| `rescue_priority_version` | `bigint unsigned` | YES | FK |
| `definition_version` | `tinyint unsigned` | NO |  |

Composite unique groups; components are not individually unique:
- rescue_criteria_snapshots_event_id_observed_at_unique: event_id, observed_at

## rescue_priority_settings

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `version` | `bigint unsigned` | NO | PK |
| `impact_weight` | `tinyint unsigned` | NO |  |
| `vulnerability_weight` | `tinyint unsigned` | NO |  |
| `unreported_weight` | `tinyint unsigned` | NO |  |
| `no_contact_weight` | `tinyint unsigned` | NO |  |
| `updated_by_user_id` | `varchar(255)` | YES | FK |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |
| `change_reason` | `varchar(255)` | YES |  |
| `high_percent` | `decimal(5,1)` | NO |  |
| `medium_percent` | `decimal(5,1)` | NO |  |
| `deploy_first_percent` | `decimal(5,1)` | NO |  |

## rescue_teams

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `team_id` | `int` | NO | PK |
| `team_code` | `varchar(50)` | YES | UK |
| `team_name` | `varchar(100)` | YES |  |
| `team_type` | `varchar(80)` | YES |  |
| `assigned_purok_id` | `int` | YES | FK |
| `leader_responder_id` | `int` | YES | FK |
| `duty_status` | `varchar(30)` | NO |  |
| `created_at` | `datetime` | YES |  |
| `updated_at` | `datetime` | YES |  |
| `base_name` | `varchar(120)` | YES |  |
| `base_latitude` | `decimal(10,7)` | YES |  |
| `base_longitude` | `decimal(10,7)` | YES |  |

## resource_request_status

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `status_id` | `int` | NO | PK |
| `status_key` | `varchar(50)` | YES | UK |
| `status_label` | `varchar(100)` | YES |  |

## resource_requests

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `request_id` | `varchar(255)` | NO | PK |
| `request_source` | `varchar(80)` | YES |  |
| `source_reference` | `varchar(120)` | YES |  |
| `request_category` | `varchar(50)` | YES |  |
| `evacuation_center_id` | `varchar(255)` | YES | FK |
| `requested_by` | `varchar(255)` | YES | FK |
| `handled_by` | `varchar(255)` | YES | FK |
| `resource_type` | `varchar(100)` | YES |  |
| `item_name` | `varchar(150)` | YES |  |
| `quantity` | `int` | YES |  |
| `unit` | `varchar(50)` | YES |  |
| `description` | `text` | YES |  |
| `status_id` | `int` | YES | FK |
| `validation_status` | `varchar(30)` | NO |  |
| `validation_notes` | `text` | YES |  |
| `validated_by_user_id` | `varchar(255)` | YES | FK |
| `validated_at` | `datetime` | YES |  |
| `released_for_tracking_at` | `datetime` | YES |  |
| `tracking_reference` | `varchar(120)` | YES |  |
| `created_at` | `datetime` | YES |  |
| `updated_at` | `datetime` | YES |  |
| `urgency_id` | `int unsigned` | YES | FK |

## responder_assignments

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `assignment_id` | `int` | NO | PK |
| `assignment_code` | `varchar(80)` | YES | UK |
| `responder_id` | `int` | NO | FK |
| `team_id` | `int` | YES | FK |
| `disaster_id` | `varchar(255)` | YES | FK |
| `affected_area_id` | `int` | YES | FK |
| `household_id` | `varchar(255)` | YES | FK |
| `status_log_id` | `int` | YES |  |
| `assigned_area` | `varchar(150)` | YES |  |
| `route_notes` | `text` | YES |  |
| `priority_level` | `varchar(30)` | YES |  |
| `dispatch_notes` | `text` | YES |  |
| `created_by_admin_id` | `varchar(255)` | YES |  |
| `status` | `varchar(50)` | YES | FK |
| `assigned_at` | `datetime` | NO |  |
| `accepted_at` | `datetime` | YES |  |
| `en_route_at` | `datetime` | YES |  |
| `arrived_at` | `datetime` | YES |  |
| `completed_at` | `datetime` | YES |  |
| `outcome_notes` | `text` | YES |  |
| `updated_at` | `datetime` | YES |  |
| `responder_count` | `smallint unsigned` | NO |  |
| `dispatch_type` | `varchar(30)` | NO |  |

## responder_check_ins

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `check_in_id` | `int` | NO | PK |
| `responder_id` | `int` | NO | FK |
| `disaster_id` | `varchar(255)` | YES | FK |
| `team_id` | `int` | YES | FK |
| `affected_area_id` | `int` | YES | FK |
| `household_id` | `varchar(255)` | YES | FK |
| `member_id` | `varchar(255)` | YES | FK |
| `latitude` | `decimal(10,7)` | YES |  |
| `longitude` | `decimal(10,7)` | YES |  |
| `check_in_method` | `varchar(10)` | YES |  |
| `status_id` | `int` | YES |  |
| `notes` | `text` | YES |  |
| `checked_in_at` | `datetime` | NO |  |
| `checked_out_at` | `datetime` | YES |  |
| `verified_by` | `varchar(255)` | YES |  |

## responder_communication_logs

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `communication_id` | `int` | NO | PK |
| `responder_id` | `int` | NO | FK |
| `team_id` | `int` | YES | FK |
| `team_name` | `varchar(100)` | YES |  |
| `disaster_id` | `varchar(255)` | YES | FK |
| `message` | `text` | YES |  |
| `timestamp` | `datetime` | NO |  |

## responder_field_report_details

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `detail_id` | `int` | NO | PK |
| `report_id` | `int` | NO | FK |
| `category_id` | `int` | NO | FK |
| `value` | `int` | YES |  |
| `notes` | `text` | YES |  |

## responder_field_report_members

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `detail_id` | `bigint unsigned` | NO | PK |
| `report_id` | `int` | NO | FK |
| `household_id` | `varchar(255)` | NO | FK |
| `disaster_id` | `varchar(255)` | NO | FK |
| `member_id` | `varchar(255)` | NO | FK |
| `status_id` | `int` | YES | FK |
| `status_key` | `varchar(50)` | NO |  |
| `assessed_at` | `timestamp` | YES |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |

Composite unique groups; components are not individually unique:
- rf_report_member_unique: report_id, member_id

## responder_field_reports

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `report_id` | `int` | NO | PK |
| `responder_id` | `int` | NO | FK |
| `disaster_id` | `varchar(255)` | YES | FK |
| `household_id` | `varchar(255)` | YES | FK |
| `latitude` | `decimal(10,7)` | YES |  |
| `longitude` | `decimal(10,7)` | YES |  |
| `notes` | `text` | YES |  |
| `created_at` | `datetime` | NO |  |
| `assignment_id` | `int` | YES | FK |
| `submitted_by_user_id` | `varchar(255)` | YES |  |
| `status_log_id` | `int` | YES | FK |
| `incident_type` | `varchar(80)` | YES |  |
| `incident_type_other` | `varchar(255)` | YES |  |
| `property_damage` | `varchar(80)` | YES | FK |
| `death_count` | `int unsigned` | YES |  |
| `injured_count` | `int unsigned` | YES |  |
| `idempotency_key` | `varchar(100)` | YES | UK |
| `payload_hash` | `varchar(64)` | YES |  |
| `submitted_at` | `timestamp` | YES |  |

## responder_location_logs

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `log_id` | `int` | NO | PK |
| `responder_id` | `int` | NO | FK |
| `latitude` | `decimal(10,7)` | YES |  |
| `longitude` | `decimal(10,7)` | YES |  |
| `battery_level` | `int` | YES |  |
| `signal_strength` | `int` | YES |  |
| `logged_at` | `datetime` | NO |  |

## responder_routes

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `route_id` | `int` | NO | PK |
| `assignment_id` | `int` | NO | FK |
| `route_name` | `varchar(150)` | YES |  |
| `route_status` | `varchar(30)` | NO |  |
| `start_latitude` | `decimal(10,7)` | YES |  |
| `start_longitude` | `decimal(10,7)` | YES |  |
| `end_latitude` | `decimal(10,7)` | YES |  |
| `end_longitude` | `decimal(10,7)` | YES |  |
| `estimated_distance_km` | `decimal(8,2)` | YES |  |
| `estimated_duration_min` | `int` | YES |  |
| `route_polyline` | `mediumtext` | YES |  |
| `created_at` | `datetime` | NO |  |
| `updated_at` | `datetime` | YES |  |
| `responder_id` | `int` | YES | FK |
| `household_id` | `varchar(255)` | YES | FK |
| `navigation_steps` | `json` | YES |  |

## responders

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `responder_id` | `int` | NO | PK |
| `user_id` | `varchar(255)` | YES | FK |
| `responder_code` | `varchar(80)` | YES | UK |
| `created_by_admin_id` | `varchar(255)` | YES |  |
| `team_id` | `int` | YES | FK |
| `username` | `varchar(100)` | YES |  |
| `password_hash` | `varchar(255)` | YES |  |
| `full_name` | `varchar(100)` | YES |  |
| `title` | `varchar(100)` | YES |  |
| `contact_number` | `varchar(20)` | YES |  |
| `emergency_contact_name` | `varchar(150)` | YES |  |
| `emergency_contact_number` | `varchar(30)` | YES |  |
| `date_of_birth` | `date` | YES |  |
| `gender` | `varchar(20)` | YES |  |
| `blood_type` | `varchar(10)` | YES |  |
| `address` | `text` | YES |  |
| `skills` | `text` | YES |  |
| `training_notes` | `text` | YES |  |
| `certification_reference` | `varchar(150)` | YES |  |
| `equipment_notes` | `text` | YES |  |
| `is_validated` | `tinyint(1)` | YES |  |
| `is_deployed` | `tinyint(1)` | YES |  |
| `duty_status` | `varchar(30)` | NO |  |
| `last_active_at` | `datetime` | YES |  |
| `created_at` | `datetime` | NO |  |
| `updated_at` | `datetime` | YES |  |
| `deleted_at` | `datetime` | YES |  |

## resq_orphan_references

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `bigint unsigned` | NO | PK |
| `source_table` | `varchar(64)` | NO |  |
| `source_key` | `varchar(255)` | NO |  |
| `source_column` | `varchar(64)` | NO |  |
| `original_value` | `varchar(255)` | NO |  |
| `parent_table` | `varchar(64)` | NO |  |
| `preserved_at` | `timestamp` | NO |  |

Composite unique groups; components are not individually unique:
- resq_orphan_source_unique: source_table, source_key, source_column

## roles

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `role_id` | `int` | NO | PK |
| `role_key` | `varchar(50)` | YES | UK |
| `role_name` | `varchar(100)` | YES |  |
| `name` | `varchar(255)` | YES |  |
| `base_role_key` | `varchar(80)` | YES |  |
| `web_modules` | `json` | YES |  |
| `can_manage_personnel` | `tinyint(1)` | YES |  |
| `can_approve_requests` | `tinyint(1)` | YES |  |

## route_coordinates

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `coordinate_id` | `int` | NO | PK |
| `route_id` | `int` | NO | FK |
| `latitude` | `decimal(10,7)` | YES |  |
| `longitude` | `decimal(10,7)` | YES |  |
| `sequence_order` | `int` | NO |  |
| `recorded_at` | `datetime` | YES |  |
| `accuracy_m` | `decimal(8,2)` | YES |  |

## sessions

SHARED FRAMEWORK

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `varchar(255)` | NO | PK |
| `user_id` | `varchar(255)` | YES |  |
| `ip_address` | `varchar(45)` | YES |  |
| `user_agent` | `text` | YES |  |
| `payload` | `longtext` | NO |  |
| `last_activity` | `int` | NO |  |

## severity_levels

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `severity_id` | `int` | NO | PK |
| `severity_key` | `varchar(50)` | YES | UK |
| `severity_label` | `varchar(100)` | YES |  |

## sitios

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `sitio_id` | `int` | NO | PK |
| `sitio_name` | `varchar(100)` | YES |  |
| `barangay_id` | `int` | NO | FK |

## situation_report_submissions

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `bigint unsigned` | NO | PK |
| `sit_rep_id` | `int` | NO | FK |
| `submitted_at` | `timestamp` | NO |  |
| `delivered_by` | `varchar(150)` | NO |  |
| `received_by` | `varchar(150)` | NO |  |
| `recorded_by` | `varchar(255)` | NO |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |

## situation_reports

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `sit_rep_id` | `int` | NO | PK |
| `report_number` | `varchar(80)` | YES | UK |
| `disaster_id` | `varchar(255)` | YES | FK |
| `created_by_admin_id` | `varchar(255)` | YES |  |
| `household_id` | `varchar(255)` | YES | FK |
| `summary` | `text` | YES |  |
| `report_status` | `varchar(30)` | NO |  |
| `reviewed_by_user_id` | `varchar(255)` | YES |  |
| `reviewed_at` | `datetime` | YES |  |
| `escalated_to` | `varchar(150)` | YES |  |
| `is_archived` | `tinyint(1)` | YES |  |
| `generated_at` | `datetime` | NO |  |
| `archived_at` | `datetime` | YES |  |
| `updated_at` | `datetime` | YES |  |
| `schema_version` | `varchar(8)` | NO |  |
| `sitrep_type` | `varchar(16)` | YES |  |
| `approved_by` | `varchar(150)` | YES |  |
| `operator_inputs` | `json` | YES |  |

## status_reminders

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `reminder_id` | `bigint unsigned` | NO | PK |
| `event_id` | `varchar(255)` | NO | FK |
| `household_id` | `varchar(255)` | NO | FK |
| `member_id` | `varchar(255)` | NO | FK |
| `attempt` | `tinyint unsigned` | NO |  |
| `status` | `varchar(20)` | NO |  |
| `scheduled_at` | `timestamp` | NO |  |
| `sent_at` | `timestamp` | YES |  |
| `stopped_at` | `timestamp` | YES |  |
| `member_delivery` | `varchar(30)` | YES |  |
| `household_delivery` | `varchar(30)` | YES |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |

Composite unique groups; components are not individually unique:
- status_reminders_event_member_attempt_unique: event_id, member_id, attempt

## sync_events

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `bigint unsigned` | NO | PK |
| `client_event_id` | `char(36)` | NO | UK |
| `device_id` | `bigint` | NO | FK |
| `type` | `varchar(40)` | NO |  |
| `status` | `enum('received','processed','failed')` | NO |  |
| `error_message` | `varchar(255)` | YES |  |
| `received_at` | `timestamp` | NO |  |
| `result_json` | `json` | YES |  |

## trip_points

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `bigint unsigned` | NO | PK |
| `trip_id` | `bigint unsigned` | NO | FK |
| `lat` | `decimal(10,7)` | NO |  |
| `lng` | `decimal(10,7)` | NO |  |
| `accuracy` | `decimal(8,2)` | YES |  |
| `speed` | `decimal(8,3)` | YES |  |
| `heading` | `decimal(6,2)` | YES |  |
| `recorded_at` | `datetime(6)` | NO |  |

## trusted_households

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `connection_id` | `varchar(80)` | NO | PK |
| `requesting_household_id` | `varchar(255)` | NO | FK |
| `trusted_household_id` | `varchar(255)` | NO | FK |
| `reason` | `text` | NO |  |
| `validation_status` | `varchar(30)` | NO |  |
| `member_relationships` | `json` | YES |  |
| `created_by_user_id` | `varchar(255)` | YES |  |
| `validated_by_user_id` | `varchar(255)` | YES |  |
| `validated_at` | `datetime` | YES |  |
| `created_at` | `datetime` | YES |  |
| `updated_at` | `datetime` | YES |  |

## urgency_levels

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `urgency_id` | `int unsigned` | NO | PK |
| `urgency_key` | `varchar(50)` | NO | UK |
| `urgency_label` | `varchar(100)` | NO |  |

## user_notifications

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `bigint unsigned` | NO | PK |
| `user_id` | `varchar(255)` | NO | FK |
| `type` | `varchar(50)` | NO |  |
| `title` | `varchar(255)` | NO |  |
| `message` | `text` | NO |  |
| `data` | `json` | YES |  |
| `read_at` | `timestamp` | YES |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |

## users

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `user_id` | `varchar(255)` | NO | PK |
| `first_name` | `varchar(100)` | YES |  |
| `last_name` | `varchar(100)` | YES |  |
| `name` | `varchar(255)` | YES |  |
| `username` | `varchar(100)` | YES |  |
| `email` | `varchar(255)` | YES |  |
| `email_verified_at` | `timestamp` | YES |  |
| `password` | `varchar(255)` | YES |  |
| `role_id` | `int` | YES | FK |
| `contact_number` | `varchar(50)` | YES |  |
| `assigned_center_id` | `varchar(255)` | YES | FK |
| `household_id` | `varchar(255)` | YES | FK |
| `member_id` | `varchar(255)` | YES | FK,UK |
| `is_active` | `tinyint(1)` | YES |  |
| `must_change_password` | `tinyint(1)` | NO |  |
| `temp_password` | `varchar(255)` | YES |  |
| `remember_token` | `varchar(100)` | YES |  |
| `updated_at` | `timestamp` | YES |  |
| `created_at` | `datetime` | YES |  |
| `deleted_at` | `datetime` | YES |  |
| `profile_photo` | `varchar(255)` | YES |  |
| `security_question_1` | `varchar(100)` | YES |  |
| `security_answer_1` | `varchar(255)` | YES |  |
| `security_question_2` | `varchar(100)` | YES |  |
| `security_answer_2` | `varchar(255)` | YES |  |
| `password_changed_at` | `timestamp` | YES |  |

## v_household_status_board

VIEW

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `disaster_id` | `varchar(255)` | NO |  |
| `household_id` | `varchar(255)` | NO |  |
| `household_code` | `varchar(255)` | YES |  |
| `household_name` | `varchar(100)` | YES |  |
| `household_status_id` | `int` | YES |  |
| `household_status_label` | `varchar(100)` | YES |  |
| `household_status_color` | `varchar(7)` | YES |  |
| `total_members` | `bigint` | NO |  |
| `unreported` | `decimal(23,0)` | YES |  |
| `accounted_safe` | `decimal(23,0)` | YES |  |
| `needs_rescue_count` | `decimal(23,0)` | YES |  |
| `missing_count` | `decimal(23,0)` | YES |  |
| `injured_count` | `decimal(23,0)` | YES |  |
| `deceased_count` | `decimal(23,0)` | YES |  |
| `worst_severity` | `tinyint unsigned` | YES |  |
| `last_reported_at` | `datetime` | YES |  |
| `latitude` | `decimal(10,7)` | YES |  |
| `longitude` | `decimal(10,7)` | YES |  |

## v_member_status_monitor

VIEW

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `member_status_id` | `bigint` | NO |  |
| `disaster_id` | `varchar(255)` | NO |  |
| `event_name` | `varchar(100)` | YES |  |
| `event_started_at` | `datetime` | YES |  |
| `event_ended_at` | `datetime` | YES |  |
| `event_is_active` | `int` | NO |  |
| `household_id` | `varchar(255)` | NO |  |
| `household_code` | `varchar(255)` | YES |  |
| `household_number` | `varchar(255)` | YES |  |
| `household_name` | `varchar(100)` | YES |  |
| `household_contact` | `varchar(50)` | YES |  |
| `member_id` | `varchar(255)` | NO |  |
| `member_name` | `varchar(302)` | YES |  |
| `age` | `bigint` | YES |  |
| `gender` | `varchar(20)` | YES |  |
| `relationship_label` | `varchar(100)` | YES |  |
| `is_household_head` | `tinyint(1)` | NO |  |
| `is_pwd` | `tinyint(1)` | NO |  |
| `is_senior` | `tinyint(1)` | NO |  |
| `is_pregnant` | `tinyint(1)` | NO |  |
| `account_user_id` | `varchar(255)` | YES |  |
| `account_username` | `varchar(100)` | YES |  |
| `account_email` | `varchar(255)` | YES |  |
| `has_account` | `int` | NO |  |
| `status_id` | `int` | NO |  |
| `status_key` | `varchar(50)` | NO |  |
| `status_label` | `varchar(100)` | NO |  |
| `status_color` | `varchar(7)` | YES |  |
| `severity_rank` | `tinyint unsigned` | NO |  |
| `needs_rescue` | `tinyint(1)` | NO |  |
| `priority_level` | `enum('low','medium','high','critical')` | NO |  |
| `previous_status_label` | `varchar(100)` | YES |  |
| `report_source` | `enum('self','household_head','proxy_member','responder','hq','sms','system')` | NO |  |
| `reported_by_user_id` | `varchar(255)` | YES |  |
| `reported_by_member_id` | `varchar(255)` | YES |  |
| `reported_by_name` | `varchar(201)` | YES |  |
| `latitude` | `decimal(10,7)` | YES |  |
| `longitude` | `decimal(10,7)` | YES |  |
| `location_label` | `varchar(255)` | YES |  |
| `location_accuracy_m` | `decimal(8,2)` | YES |  |
| `battery_level` | `int` | YES |  |
| `signal_strength` | `int` | YES |  |
| `evacuation_center_id` | `varchar(255)` | YES |  |
| `notes` | `text` | YES |  |
| `is_verified` | `tinyint(1)` | NO |  |
| `verified_at` | `datetime` | YES |  |
| `reported_at` | `datetime` | YES |  |
| `updated_at` | `timestamp` | YES |  |
| `minutes_since_report` | `bigint` | YES |  |

## vulnerable_groups

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `vulnerable_group_id` | `int` | NO | PK |
| `vulnerable_group_key` | `varchar(20)` | YES | UK |
| `vulnerable_group_label` | `varchar(100)` | YES |  |

## weather_logs

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `weather_log_id` | `int` | NO | PK |
| `disaster_id` | `varchar(255)` | YES | FK |
| `source_name` | `varchar(80)` | NO |  |
| `source_url` | `varchar(255)` | YES |  |
| `condition_name` | `varchar(80)` | YES |  |
| `temperature` | `decimal(5,2)` | YES |  |
| `rainfall_mm` | `decimal(8,2)` | YES |  |
| `wind_speed` | `decimal(8,2)` | YES |  |
| `wind_direction` | `varchar(50)` | YES |  |
| `humidity` | `int` | YES |  |
| `advisory_title` | `varchar(255)` | YES |  |
| `advisory_text` | `text` | YES |  |
| `raw_payload` | `json` | YES |  |
| `observed_at` | `datetime` | YES |  |
| `created_at` | `datetime` | YES |  |
| `updated_at` | `datetime` | YES |  |

## web_push_deliveries

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `bigint unsigned` | NO | PK |
| `subscription_id` | `bigint unsigned` | NO | FK |
| `notice_hash` | `varchar(64)` | NO |  |
| `created_at` | `timestamp` | NO |  |

Composite unique groups; components are not individually unique:
- web_push_deliveries_subscription_id_notice_hash_unique: subscription_id, notice_hash

## web_push_subscriptions

RESQ MAPPING

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `id` | `bigint unsigned` | NO | PK |
| `user_id` | `varchar(255)` | NO | FK |
| `token_id` | `bigint unsigned` | YES | FK |
| `endpoint_hash` | `varchar(64)` | NO | UK |
| `subscription` | `text` | NO |  |
| `expires_at` | `timestamp` | YES |  |
| `created_at` | `timestamp` | YES |  |
| `updated_at` | `timestamp` | YES |  |
| `push_after` | `timestamp` | YES |  |

## zipcodes

SHARED DEPENDENCY

| Column | MySQL type | Nullable | Keys |
|---|---|---|---|
| `zipcode_id` | `int` | NO | PK |
| `zipcode` | `varchar(10)` | YES |  |
| `city_id` | `int` | NO | FK |
