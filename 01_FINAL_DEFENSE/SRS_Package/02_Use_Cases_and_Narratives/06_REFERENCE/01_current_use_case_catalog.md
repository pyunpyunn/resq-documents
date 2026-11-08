# Current use-case catalog and route evidence

Generated from the current route/policy contract and inspected workflow sources on October 31, 2026. Existing UC-01 through UC-36 IDs are retained where applicable; letter suffixes separate actors/actions previously bundled together. UC-37 through UC-39 add explicit push/SMS/browser-notification coverage. This does not silently rewrite the older SRS baseline.

## UC-01: Sign in, resume access and sign out

Primary actors: Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation, Household resident, Rescuer team leader, Rescuer team member.

Supporting actors: none.

Goal/result: An authenticated, role-scoped session or a clear rejection.

Conditions and limits: Household owner selection and mobile device binding can restrict the session before operational actions.

Route evidence:
- `POST /auth/login`
- `GET /auth/me`
- `POST /auth/logout`

## UC-02: Maintain own profile and password

Primary actors: Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation, Household resident, Rescuer team leader, Rescuer team member.

Supporting actors: none.

Goal/result: Permitted personal fields or credentials updated.

Conditions and limits: These are role-specific entry points, not permission for every actor to call every listed route.

Route evidence:
- `PATCH /profile/password`
- `PATCH /profile`
- `PATCH /rescuer/profile`
- `PATCH /household/members/{memberId}`

## UC-03: Recover account access

Primary actors: Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation, Household resident, Rescuer team leader, Rescuer team member.

Supporting actors: Configured SMS gateway.

Goal/result: Verified recovery resets credentials.

Conditions and limits: Security-question recovery and household SMS recovery are different branches; configured contact data, expiry and throttles apply.

Route evidence:
- `POST /auth/password-recovery/verify`
- `POST /auth/password-recovery/reset`
- `POST /auth/password-recovery/household/send-code`
- `POST /auth/password-recovery/household/reset`

## UC-04: Manage rescuer accounts and teams

Primary actors: Operations / Admin.

Supporting actors: none.

Goal/result: Validated account/team changes with audit evidence.

Conditions and limits: Personnel access is currently Operations/Admin; a team leader is not automatically a personnel administrator.

Route evidence:
- `GET /rescuers`
- `POST /rescuers`
- `POST /rescuers/team-config`

## UC-05: Manage HQ accounts and roles

Primary actors: Operations / Admin.

Supporting actors: none.

Goal/result: Account roles and permitted capabilities configured.

Conditions and limits: Role configuration remains bounded by the server policy.

Route evidence:
- `POST /headquarters-accounts`
- `POST /rescuers/roles`

## UC-06: Maintain barangay operational profile

Primary actors: Operations / Admin.

Supporting actors: none.

Goal/result: Authorized profile data updated.

Conditions and limits: Account/module, record-scope and input validation apply as required by the listed route.

Route evidence:
- `PATCH /profile/barangay`

## UC-07A: Submit a public inquiry

Primary actors: Public visitor.

Supporting actors: none.

Goal/result: Validated inquiry stored in landing_inquiries.

Conditions and limits: Public submission does not grant staff review access.

Route evidence:
- `POST /inquiries`

## UC-07B: Review and archive inquiries

Primary actors: Operations / Admin.

Supporting actors: none.

Goal/result: Staff handling state and history recorded.

Conditions and limits: Account/module, record-scope and input validation apply as required by the listed route.

Route evidence:
- `GET /inquiries`
- `PATCH /inquiries/{inquiryId}`
- `GET /archive/inquiry-logs`

## UC-08: Select phone owner and complete household setup

Primary actors: Household resident.

Supporting actors: none.

Goal/result: Current phone is linked to an authorized household member and setup/geotag.

Conditions and limits: Pending-owner tokens cannot perform ordinary household actions. Existing registered Android/iOS platform is preserved.

Route evidence:
- `GET /household/device-owner/options`
- `POST /household/device-owner/select`
- `POST /household/setup`
- `PUT /household/geotag`

## UC-09: Receive and review disaster alerts

Primary actors: Household resident, Rescuer team leader, Rescuer team member.

Supporting actors: OneSignal mobile push.

Goal/result: App reads stored alerts; eligible devices can receive provider pushes.

Conditions and limits: Notification permission, native build, subscription and network availability are required for push delivery.

Route evidence:
- `GET /household/overview`
- `GET /rescuer/overview`

## UC-10: Report household or member safety

Primary actors: Household resident.

Supporting actors: none.

Goal/result: Authorized status/history records updated.

Conditions and limits: Use the active event and actual configured database/broadcast status choices.

Route evidence:
- `POST /household/status`
- `POST /household/members/{memberId}/status`
- `GET /household/status-history`

## UC-11: Connect and assist a trusted household

Primary actors: Household resident.

Supporting actors: none.

Goal/result: A permitted trusted connection can report scoped member status.

Conditions and limits: A household ID alone is insufficient: connection state and PIN/permission checks apply.

Route evidence:
- `POST /household/trusted-households`
- `PATCH /household/trusted-households/{connectionId}`
- `POST /household/trusted-pin/verify`
- `POST /household/trusted-households/{connectionId}/members/{memberId}/status`

## UC-12: View evacuation information and available directions

Primary actors: Household resident.

Supporting actors: Map / routing provider.

Goal/result: Available site/map information is displayed.

Conditions and limits: Availability of directions depends on the implemented client, location/provider data and connectivity; do not infer a dedicated household route API.

Route evidence:
- `GET /household/overview`

## UC-13A: Display household verification QR

Primary actors: Household resident.

Supporting actors: none.

Goal/result: Household verification information displayed.

Conditions and limits: Account/module, record-scope and input validation apply as required by the listed route.

Route evidence:
- `GET /household/qr`

## UC-13B: Verify evacuation arrival

Primary actors: Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation, Rescuer team leader, Rescuer team member.

Supporting actors: none.

Goal/result: Authorized verification/check-in updates shared evacuation evidence.

Conditions and limits: Backend verifier access is supported; a dedicated scanner account role or complete staff scanning UI is not established by these routes.

Route evidence:
- `POST /evacuation/verify-qr`
- `POST /evacuation/check-in`

## UC-14: View saved household information offline

Primary actors: Household resident.

Supporting actors: none.

Goal/result: An available account-scoped cached overview can be shown.

Conditions and limits: Current useMobileOverview/mobileSnapshot supports cached reading. This does not establish durable offline household status submission.

Route evidence:
- `GET /household/overview`

## UC-15: View own assigned incidents and households

Primary actors: Rescuer team leader, Rescuer team member.

Supporting actors: none.

Goal/result: Only the authorized rescuer assignment/household scope is returned.

Conditions and limits: Account/module, record-scope and input validation apply as required by the listed route.

Route evidence:
- `GET /rescuer/assignments`
- `GET /rescuer/assignments/{assignmentId}/household`

## UC-16: Navigate and update assigned mission progress

Primary actors: Rescuer team leader, Rescuer team member.

Supporting actors: Map / routing provider.

Goal/result: Permitted route, progress and foreground location updates recorded.

Conditions and limits: Active-event, assignment ownership, household queue and valid transition rules apply. Mobile completion is not equivalent to the HQ approval endpoint.

Route evidence:
- `POST /rescuer/assignments/{assignmentId}/route`
- `PATCH /rescuer/assignments/{assignmentId}/status`
- `POST /rescuer/assignments/{assignmentId}/location`

## UC-17: Use saved navigation and synchronize trip events

Primary actors: Rescuer team leader, Rescuer team member.

Supporting actors: none.

Goal/result: Supported local trip events receive server acknowledgments after reconnect.

Conditions and limits: Conditional on native storage, valid cached route/pack and device binding. Never generalize this outbox to every mobile write.

Route evidence:
- `GET /mobile/bootstrap`
- `GET /mobile/packs/{version}`
- `POST /mobile/sync`

## UC-18: Record check-in and member assessment

Primary actors: Rescuer team leader, Rescuer team member.

Supporting actors: none.

Goal/result: Scoped field/check-in evidence recorded.

Conditions and limits: Account/module, record-scope and input validation apply as required by the listed route.

Route evidence:
- `POST /rescuer/check-ins`
- `GET /rescuer/assignments/{assignmentId}/household`

## UC-19: Submit field findings and damage assessment

Primary actors: Rescuer team leader, Rescuer team member.

Supporting actors: none.

Goal/result: Validated report header, member assessment and catalog damage choice stored.

Conditions and limits: Actual database keys/labels, assignment/event scope and retry protections are used.

Route evidence:
- `POST /rescuer/field-reports`

## UC-20A: Communicate using internet PTT and clips

Primary actors: Rescuer team leader, Rescuer team member.

Supporting actors: none.

Goal/result: Internet radio activity and playable clip references recorded.

Conditions and limits: Requires connectivity and microphone access. It is not offline hardware radio; audio files are outside MySQL.

Route evidence:
- `POST /rescuer/radio/start`
- `POST /rescuer/radio/heartbeat`
- `POST /rescuer/radio/clip`
- `POST /rescuer/radio/stop`

## UC-20B: Monitor rescue communications

Primary actors: Chairperson, Operations / Admin, Response personnel.

Supporting actors: none.

Goal/result: Authorized HQ can review operational communication metadata.

Conditions and limits: Account/module, record-scope and input validation apply as required by the listed route.

Route evidence:
- `GET /dispatches/communications`

## UC-21A: Submit a field logistics request

Primary actors: Rescuer team leader.

Supporting actors: none.

Goal/result: Persisted request awaits HQ validation.

Conditions and limits: Submission is team-leader-only. Base rescuer identity alone does not grant this POST action.

Route evidence:
- `POST /rescuer/resource-requests`

## UC-21B: Track or cancel an eligible own request

Primary actors: Rescuer team leader, Rescuer team member.

Supporting actors: none.

Goal/result: Own request state shown or an allowed cancellation recorded.

Conditions and limits: Ownership and current state limit cancellation.

Route evidence:
- `GET /rescuer/resource-requests`
- `PATCH /rescuer/resource-requests/{requestId}/cancel`

## UC-22A: Monitor dashboard and operational summaries

Primary actors: Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation.

Supporting actors: none.

Goal/result: Charts/KPIs derive from selected operational database records.

Conditions and limits: Account/module, record-scope and input validation apply as required by the listed route.

Route evidence:
- `GET /dashboard/summary`
- `GET /dashboard/impact-history`

## UC-22B: Review maps, directory and weather

Primary actors: Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation.

Supporting actors: Weather / advisory provider.

Goal/result: Authorized geography/safety/weather data displayed.

Conditions and limits: Account/module, record-scope and input validation apply as required by the listed route.

Route evidence:
- `GET /map/overview`
- `GET /households/directory`
- `GET /weather`

## UC-23A: Declare a disaster and publish alert instructions

Primary actors: Chairperson, Operations / Admin.

Supporting actors: OneSignal mobile push, Configured SMS gateway.

Goal/result: Event/alert saved; actual provider delivery state recorded.

Conditions and limits: Publishing is Chairperson/Operations-Admin under current policy. A saved alert can still have no recipients or provider failure; only accepted messages have provider IDs.

Route evidence:
- `POST /disaster-events`
- `POST /disaster-events/{eventId}/broadcasts`

## UC-23B: Review, update and close an active event

Primary actors: Chairperson, Operations / Admin, Response personnel.

Supporting actors: none.

Goal/result: Permitted event lifecycle change recorded.

Conditions and limits: Close/review/update follow their actual route actions; do not assume all publication permissions are identical.

Route evidence:
- `GET /disaster-events`
- `PATCH /disaster-events/{eventId}`
- `POST /dashboard/active-event/close`

## UC-24: Review severity and hazard overlays

Primary actors: Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation.

Supporting actors: Weather / advisory provider.

Goal/result: Stored severity/hazard evidence displayed.

Conditions and limits: This use case does not claim an implemented arbitrary area-drawing or hazard-edit UI.

Route evidence:
- `GET /map/overview`
- `GET /weather/official-advisories`

## UC-25A: Review household safety reports

Primary actors: Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation.

Supporting actors: none.

Goal/result: Household safety data shown within geographic scope.

Conditions and limits: Account/module, record-scope and input validation apply as required by the listed route.

Route evidence:
- `GET /households`

## UC-25B: Confirm a household status report

Primary actors: Chairperson, Operations / Admin, Response personnel.

Supporting actors: none.

Goal/result: Authorized operational confirmation recorded.

Conditions and limits: Account/module, record-scope and input validation apply as required by the listed route.

Route evidence:
- `POST /households/{householdId}/confirm`

## UC-26A: Inspect rescue priorities and historical criteria

Primary actors: Chairperson, Operations / Admin, Response personnel.

Supporting actors: none.

Goal/result: Database-backed priorities and versioned evidence displayed.

Conditions and limits: Account/module, record-scope and input validation apply as required by the listed route.

Route evidence:
- `GET /dispatches/priorities`
- `GET /dispatches/criteria-timeline`

## UC-26B: Dispatch a rescue team

Primary actors: Chairperson, Operations / Admin, Response personnel.

Supporting actors: none.

Goal/result: Validated assignment targets and team/responder scope saved.

Conditions and limits: Account/module, record-scope and input validation apply as required by the listed route.

Route evidence:
- `POST /dispatches`

## UC-26C: Complete a dispatch through HQ approval

Primary actors: Chairperson, Operations / Admin.

Supporting actors: none.

Goal/result: Permitted HQ completion recorded.

Conditions and limits: HQ completion is an approve action, distinct from rescuer household-queue progress.

Route evidence:
- `POST /dispatches/{assignmentId}/complete`

## UC-27: Monitor field reports and team progress

Primary actors: Chairperson, Operations / Admin, Response personnel.

Supporting actors: none.

Goal/result: HQ operational progress/evidence displayed.

Conditions and limits: Account/module, record-scope and input validation apply as required by the listed route.

Route evidence:
- `GET /field-reports`
- `GET /dispatches`

## UC-28: Prepare, save and export a situation report

Primary actors: Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation.

Supporting actors: none.

Goal/result: Report created/exported from recorded data and operator inputs.

Conditions and limits: Account/module, record-scope and input validation apply as required by the listed route.

Route evidence:
- `GET /situation-reports`
- `POST /situation-reports`
- `GET /situation-reports/{sitRepId}/pdf`

## UC-29: Export findings for manual escalation

Primary actors: Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation.

Supporting actors: none.

Goal/result: Exported document available for manual handoff.

Conditions and limits: File export does not establish automatic transmission to every higher-level authority.

Route evidence:
- `GET /situation-reports/{sitRepId}/pdf`

## UC-30: Browse, export and manage scoped archive evidence

Primary actors: Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation.

Supporting actors: none.

Goal/result: Authorized archive evidence reviewed or managed.

Conditions and limits: Use record IDs, source validation and recording availability. Destructive actions still require their own validation/confirmation.

Route evidence:
- `GET /archive/radio-communication-logs`
- `GET /archive/saved-groups`
- `POST /archive/saved-groups`
- `POST /archive/delete-selected`

## UC-31: Submit an external resource request

Primary actors: Authorized request partner.

Supporting actors: none.

Goal/result: Authenticated partner request enters the persisted workflow.

Conditions and limits: Partner authentication/contract validation is separate from human sign-in.

Route evidence:
- `POST /external/resource-requests/handshake`
- `POST /external/resource-requests`

## UC-32A: Review and record resource requests

Primary actors: Chairperson, Operations / Admin, Response personnel, Recovery / Rehabilitation.

Supporting actors: none.

Goal/result: Authorized workspace or request record returned.

Conditions and limits: Account/module, record-scope and input validation apply as required by the listed route.

Route evidence:
- `GET /resource-requests`
- `POST /resource-requests`

## UC-32B: Validate, return or complete a resource request

Primary actors: Chairperson, Operations / Admin.

Supporting actors: none.

Goal/result: Validation decision/history/status saved.

Conditions and limits: Module visibility does not confer approval. Status labels come from actual lookup records.

Route evidence:
- `POST /resource-requests/{requestId}/validate`
- `POST /resource-requests/{requestId}/return`
- `POST /resource-requests/{requestId}/complete`

## UC-33: Forward a validated request and monitor fulfillment

Primary actors: Chairperson, Operations / Admin.

Supporting actors: TrackingAid.

Goal/result: Partner handoff/reference and actual fulfillment evidence recorded.

Conditions and limits: Partner connectivity/acknowledgment is conditional. Forwarded does not mean delivered.

Route evidence:
- `POST /resource-requests/{requestId}/forward`

## UC-34A: Request a Resqperation report

Primary actors: SafeTrack report service, EvaTrack report service, TrackingAid.

Supporting actors: none.

Goal/result: Valid partner contract creates a pending report request.

Conditions and limits: Current ReportExchangeController requires contract v4.0 with permitted event, sitio, sections and format.

Route evidence:
- `GET /external/reports/options`
- `POST /external/report-requests`

## UC-34B: Decide report release and generate a signed file

Primary actors: Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation.

Supporting actors: SafeTrack report service, EvaTrack report service, TrackingAid.

Goal/result: Accepted snapshot/file or rejection reason persisted.

Conditions and limits: This is governed by the reports module, not automatically the resource-request approve permission.

Route evidence:
- `POST /reports/external/requests/{id}/decision`
- `POST /reports/external/requests/{id}/file`

## UC-35: Request and review a partner report

Primary actors: Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation.

Supporting actors: SafeTrack report service, EvaTrack report service, TrackingAid.

Goal/result: Available partner report returned or explicit provider error.

Conditions and limits: Account/module, record-scope and input validation apply as required by the listed route.

Route evidence:
- `POST /reports/evatrack/generate`
- `POST /reports/safetrack/generate`
- `POST /reports/trackingaid/generate`

## UC-36: Export selected situation findings

Primary actors: Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation.

Supporting actors: none.

Goal/result: Permitted sections exported in the implemented format.

Conditions and limits: Account/module, record-scope and input validation apply as required by the listed route.

Route evidence:
- `POST /reports/generate`

## UC-37: Register a permitted mobile push subscription

Primary actors: Household resident, Rescuer team leader, Rescuer team member.

Supporting actors: OneSignal mobile push.

Goal/result: Real subscription/permission/identity saved on the active backend.

Conditions and limits: Native SDK registration and consent required. Legacy mobile platforms are used for Android only after provider verification.

Route evidence:
- `POST /mobile/device-token`

## UC-38: Report safety through a configured SMS gateway

Primary actors: Household resident.

Supporting actors: Configured SMS gateway.

Goal/result: A verified sender can record supported event status.

Conditions and limits: Gateway signature/timestamp, matching household contact, active event and supported keyword are required.

Route evidence:
- `POST /sms/inbound`

## UC-39: Review notifications and enable browser push

Primary actors: Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation.

Supporting actors: Browser Push service.

Goal/result: Authorized web notifications or browser subscription updated.

Conditions and limits: Browser push uses VAPID/service-worker configuration and HTTPS requirements; it is separate from mobile OneSignal.

Route evidence:
- `GET /notifications`
- `POST /notifications/push/subscription`
