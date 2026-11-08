# Situation reports, archives and partner exchange — use cases

Mermaid has no native UML use-case diagram. Actor boxes, oval goals and the system boundary form an explicitly UML-style view; association lines are not a process sequence. Supporting providers are external actors, not additional staff roles.

```mermaid
flowchart LR
  %% UML-style use-case view in Mermaid flowchart notation; neutral lines are associations.
  actorchair["Actor: Chairperson"]
  actorevaTrack["Actor: EvaTrack report service"]
  actormitigationprevention["Actor: Mitigation / Prevention"]
  actoroperationsadmin["Actor: Operations / Admin"]
  actorpreparedness["Actor: Preparedness"]
  actorrecoveryrehabilitation["Actor: Recovery / Rehabilitation"]
  actorresponse["Actor: Response personnel"]
  actorsafeTrack["Actor: SafeTrack report service"]
  actortrackingAid["Actor: TrackingAid"]
  subgraph systemBoundary["RESQPERATION system boundary"]
    caseUC28(["UC-28: Prepare, save and export a situation report"])
    caseUC29(["UC-29: Export findings for manual escalation"])
    caseUC30(["UC-30: Browse, export and manage scoped archive evidence"])
    caseUC34A(["UC-34A: Request a Resqperation report"])
    caseUC34B(["UC-34B: Decide report release and generate a signed file"])
    caseUC35(["UC-35: Request and review a partner report"])
    caseUC36(["UC-36: Export selected situation findings"])
  end
  actorchair --- caseUC28
  actoroperationsadmin --- caseUC28
  actormitigationprevention --- caseUC28
  actorpreparedness --- caseUC28
  actorresponse --- caseUC28
  actorrecoveryrehabilitation --- caseUC28
  actorchair --- caseUC29
  actoroperationsadmin --- caseUC29
  actormitigationprevention --- caseUC29
  actorpreparedness --- caseUC29
  actorresponse --- caseUC29
  actorrecoveryrehabilitation --- caseUC29
  actorchair --- caseUC30
  actoroperationsadmin --- caseUC30
  actormitigationprevention --- caseUC30
  actorpreparedness --- caseUC30
  actorresponse --- caseUC30
  actorrecoveryrehabilitation --- caseUC30
  actorsafeTrack --- caseUC34A
  actorevaTrack --- caseUC34A
  actortrackingAid --- caseUC34A
  actorchair --- caseUC34B
  actoroperationsadmin --- caseUC34B
  actormitigationprevention --- caseUC34B
  actorpreparedness --- caseUC34B
  actorresponse --- caseUC34B
  actorrecoveryrehabilitation --- caseUC34B
  actorsafeTrack --- caseUC34B
  actorevaTrack --- caseUC34B
  actortrackingAid --- caseUC34B
  actorchair --- caseUC35
  actoroperationsadmin --- caseUC35
  actormitigationprevention --- caseUC35
  actorpreparedness --- caseUC35
  actorresponse --- caseUC35
  actorrecoveryrehabilitation --- caseUC35
  actorsafeTrack --- caseUC35
  actorevaTrack --- caseUC35
  actortrackingAid --- caseUC35
  actorchair --- caseUC36
  actoroperationsadmin --- caseUC36
  actormitigationprevention --- caseUC36
  actorpreparedness --- caseUC36
  actorresponse --- caseUC36
  actorrecoveryrehabilitation --- caseUC36
```

## Use cases and responsibilities

| ID | Goal | Primary actor / permitted baseline role | Result / important condition |
|---|---|---|---|
| UC-28 | Prepare, save and export a situation report | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation | Report created/exported from recorded data and operator inputs.  |
| UC-29 | Export findings for manual escalation | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation | Exported document available for manual handoff. File export does not establish automatic transmission to every higher-level authority. |
| UC-30 | Browse, export and manage scoped archive evidence | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation | Authorized archive evidence reviewed or managed. Use record IDs, source validation and recording availability. Destructive actions still require their own validation/confirmation. |
| UC-34A | Request a Resqperation report | SafeTrack report service, EvaTrack report service, TrackingAid | Valid partner contract creates a pending report request. Current ReportExchangeController requires contract v4.0 with permitted event, sitio, sections and format. |
| UC-34B | Decide report release and generate a signed file | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation | Accepted snapshot/file or rejection reason persisted. This is governed by the reports module, not automatically the resource-request approve permission. |
| UC-35 | Request and review a partner report | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation | Available partner report returned or explicit provider error.  |
| UC-36 | Export selected situation findings | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation | Permitted sections exported in the implemented format.  |

[Raw Mermaid](12_reports_use_cases.mmd) | [Package index](../00_README.md) | [Current case catalog](../06_REFERENCE/01_current_use_case_catalog.md)
