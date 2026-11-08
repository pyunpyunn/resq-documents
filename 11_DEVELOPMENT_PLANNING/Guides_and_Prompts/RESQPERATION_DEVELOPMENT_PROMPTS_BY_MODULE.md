# RESQPERATION Development Prompts by Module

Use these prompts when starting actual development. They are written so Codex can work from the token-friendly module references instead of repeatedly scanning the full prototype.

Main rule for every prompt:

```text
Use beginner-friendly code. Do not over-engineer. Keep Laravel API-only, React web separated, Expo mobile separated, and MySQL shared database. Match the prototype UI/UX, but do not copy the 10k-line HTML as one file. Use reusable components, arrays, .map(), simple controllers, simple API files, and clear naming.
```

Recommended workflow:

1. Start with the global project setup prompt.
2. Build backend foundations first.
3. Build frontend shell and shared components.
4. Build one module at a time.
5. Connect each module to backend endpoints.
6. Use the verification prompts before moving to the next module.


## 1. Global Starter Prompt

```text
We are starting the actual development of RESQPERATION from the prototype references in c:\resq.

Use these files:
- RESQPERATION_ACTUAL_DEVELOPMENT_PLAN.md
- RESQPERATION_REQUIREMENTS_BREAKDOWN.md
- RESQPERATION_UPDATED_STEP_GUIDE.md
- RESQPERATION_RESOURCES.txt
- RESQPERATION_UIUX_NAMING_AND_FLOW_GUIDE.txt
- RESQPERATION_PROTOTYPE_MODULES/README.md

Important:
- Do not scan the full resqperation-2 (1).html unless absolutely needed.
- Use RESQPERATION_PROTOTYPE_MODULES/modules/*.html as the UI reference per module.
- Use RESQPERATION_PROTOTYPE_MODULES/shared/global-styles.css for style reference.
- Use RESQPERATION_PROTOTYPE_MODULES/shared/function-index.txt to locate prototype behaviors.
- Use rg before reading large files.

Build the real system with:
- backend-laravel: Laravel API only
- frontend-web: React + Vite
- frontend-mobile: Expo React Native
- database: shared MySQL

Use beginner-friendly code. Do not over-engineer. No Laravel Blade dashboard pages, no TypeScript, no Redux/Zustand, no WebSockets in version 1. Use simple Laravel controllers, migrations, models, Form Requests, API Resources, React function components, useState/useEffect, Axios API files, and reusable UI components.
```


## 2. Project Scaffold Prompt

```text
Create the initial RESQPERATION project folder structure.

Target structure:
resqperation-system/
  backend-laravel/
  frontend-web/
  frontend-mobile/
  docs/

Use Laravel API-only for backend, React + Vite for web, and Expo React Native for mobile. Do not implement all modules yet. Create only the starting structure, environment notes, README files, and placeholder folders that match RESQPERATION_ACTUAL_DEVELOPMENT_PLAN.md.

Keep commands and code beginner-friendly. Explain what each folder is for.
```


## 3. Backend Foundation Prompt

```text
Build the Laravel backend foundation for RESQPERATION.

Use backend-laravel only. Laravel must be API-only. Do not create Blade dashboard pages.

Database credentials:
DB_HOST=10.150.111.114
DB_PORT=3306
DB_DATABASE=klint
DB_USERNAME=groupmate
DB_PASSWORD=REDACTED

Create:
- API routes under /api/v1
- Laravel Sanctum authentication
- User and role structure
- beginner-friendly controllers
- Form Requests for validation
- API Resources for JSON responses
- seeders for sample roles and users

Use the planning docs:
- RESQPERATION_ACTUAL_DEVELOPMENT_PLAN.md
- RESQPERATION_REQUIREMENTS_BREAKDOWN.md

Do not build every module yet. Set up the backend base cleanly so modules can be added one by one.
```


## 4. Backend Database Prompt

```text
Create Laravel migrations and models for the RESQPERATION core data structure.

Use beginner-friendly naming and relationships. Create only necessary fields based on RESQPERATION_REQUIREMENTS_BREAKDOWN.md.

Required tables:
- users
- roles
- role_user
- disaster_events
- broadcast_logs
- weather_logs
- households
- household_members
- household_devices
- household_geotags
- household_status_logs
- evacuation_sites
- rescue_teams
- rescuer_profiles
- rescue_dispatches
- dispatch_routes
- resource_items
- resource_requests
- request_validations
- situation_reports
- audit_logs

Keep migrations readable. Add indexes for disaster_event_id, household_id, team_id, status, date/time fields, and geotag fields where needed. Do not add advanced database patterns unless required.
```


## 5. Frontend Foundation Prompt

```text
Build the React + Vite frontend foundation for RESQPERATION.

Use:
- frontend-web
- React + Vite
- JavaScript, not TypeScript
- React Router
- Axios
- Lucide React
- plain CSS based on the prototype

Use these references:
- RESQPERATION_PROTOTYPE_MODULES/modules/00-shell-landing-login-navigation.html
- RESQPERATION_PROTOTYPE_MODULES/shared/global-styles.css
- RESQPERATION_UIUX_NAMING_AND_FLOW_GUIDE.txt

Create:
- AppShell
- Sidebar
- Topbar
- PageHeader
- Button
- Badge
- Modal
- Drawer
- DataTable
- ActionMenu
- FilterBar
- SearchInput
- StatCard
- Toast

Do not build all pages yet. First create routing, layout, shared styles, and placeholder pages. Match the prototype's sidebar, topbar, typography, spacing, colors, button style, modal layering, and page layout.
```


## 6. Shared Frontend API Prompt

```text
Create frontend API files for RESQPERATION.

All API calls must be inside frontend-web/src/api files. Components should not contain raw API URLs.

Create:
- authApi.js
- dashboardApi.js
- broadcastApi.js
- weatherApi.js
- mappingApi.js
- householdApi.js
- dispatchApi.js
- rescuerApi.js
- resourceRequestApi.js
- situationReportApi.js
- archiveApi.js

Use Axios. Create one configured axios client with base URL from .env. Keep functions simple and beginner-friendly. Use consistent names like getHouseholds, createBroadcast, getArchiveRecords, generateSituationReport.
```


## 7. Module Prompt: Shell, Landing, Login, Navigation

```text
Build the RESQPERATION web shell, landing/login flow, and sidebar navigation.

Use only these prototype references unless more is needed:
- RESQPERATION_PROTOTYPE_MODULES/modules/00-shell-landing-login-navigation.html
- RESQPERATION_PROTOTYPE_MODULES/shared/global-styles.css
- RESQPERATION_PROTOTYPE_MODULES/shared/function-index.txt

Requirements:
- Landing page matches the prototype.
- Login modal/page matches the prototype.
- After login, show AppShell.
- Sidebar navigation shows the same modules and grouping.
- Active page state works.
- Logout returns to landing/login state.
- Modals must appear above header/sidebar.
- Switching pages must close page-owned modals and action menus.

Use beginner-friendly React state. Do not connect real authentication yet unless backend auth is ready. Use simple placeholder login first, then prepare for Sanctum later.
```


## 8. Module Prompt: Dashboard

```text
Build the Dashboard page.

Use:
- RESQPERATION_PROTOTYPE_MODULES/modules/01-dashboard.html
- shared/global-styles.css

The Dashboard must match the prototype's operational command center layout:
- status summary
- urgent alerts
- weather snapshot
- household status overview
- dispatch overview
- recent activity/logs
- quick navigation actions

Do not make the dashboard a heavy archive or huge table page. Use summary cards and compact panels only.

Use arrays and .map() for repeated cards/logs. Use dashboardApi.js for future backend data. For now, use sample data in a clear sampleData object.
```


## 9. Module Prompt: Broadcast

```text
Build the Broadcast page.

Use:
- RESQPERATION_PROTOTYPE_MODULES/modules/02-broadcast.html
- shared/prototype-script.js functions related to broadcast:
  - updateBroadcastRecipient
  - setBroadcastFormOpen
  - updateStatusToggleLimit
  - initializePurokSelector
  - renderDirectPuroks

Requirements:
- New broadcast/start flow matches the prototype.
- Disaster type changes recipient explanation.
- Barangay-wide and direct-impact purok flow works.
- Status update selection limit works.
- Broadcast logs display.
- Submit button validates required fields.
- Cancel resets/closes the form.

Use beginner-friendly React state and arrays. Store API calls in broadcastApi.js. Do not hardcode many repeated rows manually.
```


## 10. Module Prompt: Weather

```text
Build the Weather page.

Use:
- RESQPERATION_PROTOTYPE_MODULES/modules/03-weather.html

Requirements:
- Live condition updates
- Temperature monitoring
- Rainfall monitoring
- Wind speed and direction monitoring
- Weather condition display: sunny, rainy, stormy, cloudy, storm
- Weather logs
- Refresh button

Backend rule:
- React calls weatherApi.js.
- Laravel backend fetches trusted weather data and stores weather_logs.
- If live API fails, show latest stored weather log.

Use sample weather data first if backend is not ready. Keep the UI identical to the prototype style.
```


## 11. Module Prompt: Mapping / Geotagging

```text
Build the Mapping page.

Use:
- RESQPERATION_PROTOTYPE_MODULES/modules/04-mapping.html
- shared/prototype-script.js function initializeMapDots if needed for visual behavior reference

Requirements:
- Geotagged household map
- Evacuation site pins
- Vacancy display
- Route to vacant sites
- Rescue dispatched routes by team
- Legend/role of geotagged map
- Household marker colors only:
  - green = safe / evacuated / checked
  - red = unsafe / missing / injured
  - grey = unchecked

Use Leaflet / React Leaflet for the real map if building actual map functionality. If Leaflet is not installed yet, first build the static prototype-matching map panel, then connect map data later.

Keep controls compact and professional. Avoid unnecessary scrolling.
```


## 12. Module Prompt: Households

```text
Build the Households page.

Use:
- RESQPERATION_PROTOTYPE_MODULES/modules/05-households.html
- shared/prototype-script.js functions:
  - openHHDrawer
  - closeHHDrawer
  - applyHHFilters
  - setHHFilter
  - setHHPurokFilter
  - filterHH

Requirements:
- Household summary and progress display
- Search bar
- All Puroks dropdown beside search bar
- Status filter chips
- Household table
- Household detail drawer/modal
- Members table
- Devices table
- History table
- Dispatch button when household needs rescue

Use DataTable, FilterBar, Drawer, Badge, and Button components. Render household rows from an array. Do not manually paste many rows in JSX.
```


## 13. Module Prompt: Rescue Dispatch

```text
Build the Rescue Dispatch page.

Use:
- RESQPERATION_PROTOTYPE_MODULES/modules/06-dispatch.html
- shared/prototype-script.js functions:
  - getDispatchAreaStats
  - renderDispatchRiskAreas
  - updateDispatchAreaPlan
  - syncDispatchOutcomeState
  - openDPModal
  - closeDPModal
  - filterDPTeams

Requirements:
- Team status summary
- Team cards
- Dispatch log
- New dispatch/update dispatch modal
- Affected/unsafe area selection
- Recommended households to cover
- Team selection
- Field status selection
- On-scene outcome fields enable only when status is on-scene
- Dispatch update saves to backend later

Use simple React state. Keep the modal centered and page-scoped. Use dispatchApi.js for future backend calls.
```


## 14. Module Prompt: Rescuers

```text
Build the Rescuers page.

Use:
- RESQPERATION_PROTOTYPE_MODULES/modules/09-rescuers.html
- shared/prototype-script.js functions:
  - openRescuerAccountModal
  - closeRescuerAccountModal
  - row action menu behavior

Requirements:
- Rescuer roster table
- Search and filter design consistent with other pages
- All Puroks dropdown beside search if location filtering exists
- One action icon per row instead of many buttons
- Row action menu
- Create/view/edit rescuer account modal
- Modal centered and above header
- Form fields match prototype

Use ActionMenu and Modal components. Use rescuerApi.js for backend calls later.
```


## 15. Module Prompt: Resources and Requests

```text
Build the Resources & Requests page.

Use:
- RESQPERATION_PROTOTYPE_MODULES/modules/10-resources-requests.html
- shared/prototype-script.js functions:
  - getValidationRequestData
  - openValidationRecordModal
  - closeValidationRecordModal
  - row action menu behavior

Requirements:
- Intake / validate / approve / forward flow
- Validation queue table
- TrackingAid resource mirror
- Search/filter row consistent with other pages
- All Puroks dropdown beside search
- One action icon per request row
- Validation record opens in a modal, not inside current page content
- Validation modal centered and above header

Use ActionMenu, DataTable, Modal, FilterBar, Badge. Use resourceRequestApi.js for backend calls later.
```


## 16. Module Prompt: Situation Reporting

```text
Build the Situation Reporting page.

Use:
- RESQPERATION_PROTOTYPE_MODULES/modules/11-situation.html
- shared/prototype-script.js functions:
  - renderSitrepEventSummary
  - generateSitrep

Requirements:
- HQ/Admin must select a disaster event from a dropdown before the summary appears.
- No full SitRep summary should show by default.
- If Generate SitRep is clicked without selecting an event, show a clear message.
- Selected event summary includes:
  - disaster type
  - date declared
  - date finished
  - household status summary
  - dispatched team summary
  - weather summary for that disaster event
  - resources and requests summary
- Export dropdown supports CSV/PDF options.

Use situationReportApi.js for:
- getDisasterEvents
- getSituationSummary(eventId)
- createSituationReport(eventId)
- exportSituationReport(id, type)

Use simple React state: selectedEventId, summary, isLoading, error.
```


## 17. Module Prompt: Archive

```text
Build the Archive page.

Use:
- RESQPERATION_PROTOTYPE_MODULES/modules/12-archive.html
- shared/prototype-script.js functions:
  - showArchiveTab
  - setArchiveStatusFilter
  - filterArchiveRows

Requirements:
- Full-width evenly aligned tab row.
- Tabs/categories:
  - Disaster Event
  - Household Status Logs
  - Rescue Dispatch Logs
  - Resources & Requests
  - Situation Reporting
- Do not show unnecessary archive count cards above the tabs.
- Each tab must show only relevant historical records.
- Archive records must be based on history, dates, entries, event name, status changes, and user actions.
- Search bar and filters must be consistent with other pages.
- All Puroks dropdown sits beside the search bar.
- Download is a dropdown with CSV and PDF, not two separate buttons.

Use archiveApi.js for:
- getDisasterEventArchives
- getHouseholdStatusLogs
- getDispatchLogs
- getResourceRequestArchives
- getSituationReportArchives
- exportArchive(category, type)

Use DataTable, FilterBar, Button, Badge. Render tab content from arrays and .map().
```


## 18. Module Prompt: Legacy Pages

```text
Review the legacy prototype modules only as reference.

Use:
- RESQPERATION_PROTOTYPE_MODULES/modules/07-households-legacy.html
- RESQPERATION_PROTOTYPE_MODULES/modules/08-dispatch-legacy.html

Do not build separate legacy pages unless the instructor requires them.
Use legacy modules only to confirm missing fields, labels, old table columns, or previous behavior ideas.

If a field exists only in legacy and is still useful, add it to the current Households or Dispatch module in a clean beginner-friendly way.
```


## 19. Mobile Prompt: Household Role

```text
Build the Expo mobile household role screens for RESQPERATION.

Use the web prototype for labels and status rules, but design for mobile.

Requirements:
- login
- active disaster alert
- submit household status
- status options: safe, evacuated, unsafe, injured, missing, unchecked
- household member list
- geotag/location permission
- allowed locations / current location
- receive broadcast alerts later
- simple status history

Use Expo React Native, JavaScript, React Navigation, Axios, Expo SecureStore, Expo Location.
Keep code beginner-friendly. Use householdApi/mobile API functions, not raw URLs in screens.
```


## 20. Mobile Prompt: Rescuer Role

```text
Build the Expo mobile rescuer role screens for RESQPERATION.

Use web dispatch and household prototype references for labels and flow.

Requirements:
- login
- assigned rescue dispatches
- route/area details
- household status update from field
- report safe/evacuated/unsafe/injured/missing
- request resources/personnel
- update dispatch status: standby, dispatched, on-scene, returning, completed
- geotag rescuer location if permission is granted

Use simple mobile screens and clear buttons. Do not overbuild maps first; start with dispatch list and status update flow, then add map.
```


## 21. Backend Module Prompt: Archive and SitRep APIs

```text
Build Laravel API endpoints for Situation Reporting and Archive.

Situation Reporting:
- GET /api/v1/disaster-events/{id}/situation-summary
- GET /api/v1/situation-reports
- POST /api/v1/situation-reports
- GET /api/v1/situation-reports/{id}
- GET /api/v1/situation-reports/{id}/pdf

Archive:
- GET /api/v1/archive/disaster-events
- GET /api/v1/archive/household-status-logs
- GET /api/v1/archive/dispatch-logs
- GET /api/v1/archive/resource-requests
- GET /api/v1/archive/situation-reports
- GET /api/v1/archive/export?category=disaster-events&type=csv
- GET /api/v1/archive/export?category=disaster-events&type=pdf

Archive should query existing log tables. Do not duplicate archive data unless required. Use date filters, event filters, purok filters, status filters, and pagination.

Keep controllers beginner-friendly. Return consistent JSON:
{ success, message, data }
```


## 22. Verification Prompt for Each Module

```text
Review the current module implementation against the prototype reference.

Check:
- visual layout
- spacing
- colors
- button style
- top-right page actions
- search/filter row
- All Puroks dropdown beside search when applicable
- modal centering and z-index
- row action menus
- no dead buttons
- loading state
- empty state
- error state
- API file usage
- repeated UI rendered with .map()
- no unrelated refactors

Tell me what matches, what does not match, and patch the code if needed.
```


## 23. Final Integration Prompt

```text
Run an end-to-end review of RESQPERATION.

Check backend-laravel, frontend-web, and frontend-mobile.

Verify:
- Laravel API routes exist and return JSON.
- React web pages match the prototype modules.
- Expo mobile role flows work for household and rescuer.
- Authentication and roles are consistent.
- Weather refresh works or safely falls back to cached logs.
- Map/geotag status colors are correct.
- Archive tabs work.
- Archive CSV/PDF dropdown works.
- Situation Reporting requires event selection first.
- Resources validation opens in a modal.
- Modals close when switching pages.
- No button is dead.
- Large data uses pagination or summary endpoints.

Do not rewrite the whole system. Patch only the issues found.
```


## 24. Short Prompt Template for Daily Use

```text
Focus only on [MODULE_NAME].

Use:
- RESQPERATION_PROTOTYPE_MODULES/modules/[MODULE_FILE].html
- RESQPERATION_PROTOTYPE_MODULES/shared/global-styles.css
- RESQPERATION_PROTOTYPE_MODULES/shared/function-index.txt if behavior is needed

Do not scan the full resqperation-2 (1).html unless necessary.
Build/patch the real project code using beginner-friendly Laravel/React/Expo patterns.
Match the prototype UI/UX exactly for this module.
Use reusable components and .map() for repeated UI.
Verify the module before finishing.
```
