# RESQPERATION Updated System Stack

**Checked:** 29 October 2026  
**Basis:** Organized project documentation and current backend/web/mobile dependency manifests. Version ranges below are declared in the manifests; they are not a claim about the exact package versions installed in a particular deployment.

## System overview

RESQPERATION is a three-client system: an HQ/Admin web dashboard, a mobile app with household and rescuer role-specific workflows, and a Laravel JSON API. Web and mobile clients communicate with the backend over `/api/v1`; clients do not connect directly to the operational databases.

```text
HQ/Admin web ─────┐
Household mobile ─┼── HTTPS/JSON API (/api/v1) ── Laravel backend ── operational MySQL
Rescuer mobile ───┘                                      ├──────────── TrackingAid DB
                                                        ├──────────── file/audio storage
                                                        └──────────── external providers
```

## Technology stack

| Layer | Technology in current project | Role |
|---|---|---|
| Backend language/runtime | PHP `^8.3` | Runs the API and background work. |
| Backend framework | Laravel `^13.8` | Routing, middleware, validation, database access, services, queues, scheduler, and API responses. |
| API/authentication | Versioned JSON API at `/api/v1`; Laravel Sanctum `^4.0` | Authenticated web/mobile requests, token-based access, and role-protected route groups. |
| Main persistence | MySQL-compatible database, active Laravel connection `resq_local` by default | Operational system records; the actual database endpoint is environment-configured. |
| Secondary persistence | Separately configured MySQL-compatible `trackingaid` connection | Downstream request handoff; not the primary RESQPERATION database. |
| Local/test persistence | Laravel SQLite connection is configured | Local or test use where selected; does not mean production uses SQLite. |
| Backend events/realtime | Laravel Reverb `^1.12`, Laravel Echo `^2.6.1` on web, Pusher JS `^8.6.0` | Realtime/event delivery where configured. Provider, deployment, and network settings are required. |
| Backend queues/cache | Laravel queues and scheduler; Predis `^3.7` is available | Asynchronous notifications, integrations, and scheduled work. The queue/cache driver depends on environment configuration. |
| Backend files/exports | Laravel filesystem; Flysystem S3 adapter `^3.35`; DomPDF `^3.1`; OpenSpout `^5.12` | File storage and generated PDF/spreadsheet or streamed exports where those flows use them. S3 use is configuration-dependent. |
| Web language/build | JavaScript ES modules, React `^19.2.6`, Vite `^8.0.12` | HQ/Admin browser application and production web bundle. |
| Web navigation/UI | React Router DOM `^7.16.0`, CSS, Font Awesome, Lucide | Client-side navigation, styling, and icons. |
| Web data/state | Axios `^1.16.1`, Redux Toolkit `^2.13.0`, React Redux `^9.3.0`, TanStack Table `^8.21.3` | API calls, shared client state, and data tables. |
| Web maps/charts/reports | Leaflet `^1.9.4`, React Leaflet `^5.0.0`, Chart.js `^4.5.1`, `@react-pdf/renderer` `^4.9.0` | Web maps, charts, and browser-generated PDF documents. |
| Mobile language/runtime | TypeScript `~5.9.2`, React `19.1.0`, React Native `0.81.5` | Shared Android/iOS-oriented mobile application code. |
| Mobile framework/navigation | Expo `~54.0.37`, Expo Router `~6.0.23`, Hermes JavaScript engine | App packaging, native capabilities, and file-based navigation. |
| Mobile maps/location | MapLibre React Native `^11.5.0`, React Native Maps `1.20.1`, Expo Location `~19.0.8` | Native map rendering and device location. Exact provider/tile availability is configuration-dependent. |
| Mobile storage/offline support | Expo SecureStore `~15.0.8`, Expo SQLite `~16.0.10`, Expo File System `~19.0.24`, Expo Network `~8.0.8` | Secure token storage and selected local/offline data workflows. Do not claim every workflow is fully offline. |
| Mobile device features | Expo Audio, Image Picker, Battery, Notifications, Task Manager; React Native SVG and QR packages | Audio/PTT-related workflows, images, device status, notifications, background tasks, diagrams/icons, and QR display as used by the app. |
| Push notifications | OneSignal Expo plugin `^2.7.0`, React Native OneSignal `^5.5.3`, Android push services | Push delivery when app/provider configuration, device permissions, network, and subscriptions are in place. |
| Testing/quality | PHPUnit `^12.5`; web ESLint and Vite; mobile Expo lint and TypeScript `tsc --noEmit` | Backend tests, web lint/build, and mobile static/type checks. |

## Data flow and integrations

1. Web and mobile users authenticate through Laravel; the API validates requests and enforces backend role/access rules.
2. Laravel reads and writes operational data through the active database connection. The configured connection can differ between environments.
3. Selected events use Laravel jobs/queues, scheduler, storage, and realtime services for background processing and client updates.
4. External integrations documented in the project include SafeTrack household/shared records, EvaTrack request intake, TrackingAid validated-request handoff, OneSignal push, Open-Meteo weather snapshots, PAGASA advisories/references, and configured map/routing and SMS providers.
5. These integrations are not all unconditional: credentials, access approvals, network reachability, service availability, and deployment settings may be required. A documented provider is not by itself proof that the integration is live in the defense environment.

## Security and operations boundaries

- Keep database credentials, provider secrets, and signing material in backend environment configuration; do not put server secrets in a client app.
- Clients call the API and must not connect directly to MySQL.
- Authentication does not grant every role permission; backend authorization and request validation control protected operations.
- Protect household location, contact, and member data. Use approved/synthetic demo data or mask personal data during defense.
- Database schema proposals require review before application to a shared database.
- Verify the exact app build, package versions, environment, providers, and database target used for the defense; this table summarizes project declarations, not a deployment certification.

## Primary evidence

- Current backend dependency declarations: [`composer.json`](../../../../resqperation-system/backend-laravel/composer.json)
- Current web dependency declarations: [`package.json`](../../../../resqperation-system/frontend-web/package.json)
- Current mobile dependency declarations: [`package.json`](../../../../resqperation-system/frontend-mobile/package.json)
- Mobile platform/app configuration: [`app.json`](../../../../resqperation-system/frontend-mobile/app.json)
- Database connection definitions: [`database.php`](../../../../resqperation-system/backend-laravel/config/database.php)
- Organized architecture and ownership reference: [RESQPERATION_SYSTEM_ARCHITECTURE_FILE_STACK.md](../../../03_SYSTEM_DESIGN/Requirements_and_Architecture/RESQPERATION_SYSTEM_ARCHITECTURE_FILE_STACK.md)
- Organized stack/resources reference: [RESQPERATION_SYSTEM_STACK_RESOURCES_AND_REFERENCES.md](RESQPERATION_SYSTEM_STACK_RESOURCES_AND_REFERENCES.md)

The organized stack/resources reference has an older scan date. For version numbers, prefer the current manifests linked above and recheck them against the exact lockfiles/build used for submission.
