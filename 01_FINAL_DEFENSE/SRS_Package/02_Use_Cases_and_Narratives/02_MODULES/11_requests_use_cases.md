# Resource request validation and handoff — use cases

Mermaid has no native UML use-case diagram. Actor boxes, oval goals and the system boundary form an explicitly UML-style view; association lines are not a process sequence. Supporting providers are external actors, not additional staff roles.

```mermaid
flowchart LR
  %% UML-style use-case view in Mermaid flowchart notation; neutral lines are associations.
  actorchair["Actor: Chairperson"]
  actoroperationsadmin["Actor: Operations / Admin"]
  actorrecoveryrehabilitation["Actor: Recovery / Rehabilitation"]
  actorresourcePartner["Actor: Authorized request partner"]
  actorresponse["Actor: Response personnel"]
  actortl["Actor: Rescuer team leader"]
  actortm["Actor: Rescuer team member"]
  actortrackingAid["Actor: TrackingAid"]
  subgraph systemBoundary["RESQPERATION system boundary"]
    caseUC21A(["UC-21A: Submit a field logistics request"])
    caseUC21B(["UC-21B: Track or cancel an eligible own request"])
    caseUC31(["UC-31: Submit an external resource request"])
    caseUC32A(["UC-32A: Review and record resource requests"])
    caseUC32B(["UC-32B: Validate, return or complete a resource request"])
    caseUC33(["UC-33: Forward a validated request and monitor fulfillment"])
  end
  actortl --- caseUC21A
  actortl --- caseUC21B
  actortm --- caseUC21B
  actorresourcePartner --- caseUC31
  actorchair --- caseUC32A
  actoroperationsadmin --- caseUC32A
  actorresponse --- caseUC32A
  actorrecoveryrehabilitation --- caseUC32A
  actorchair --- caseUC32B
  actoroperationsadmin --- caseUC32B
  actorchair --- caseUC33
  actoroperationsadmin --- caseUC33
  actortrackingAid --- caseUC33
```

## Use cases and responsibilities

| ID | Goal | Primary actor / permitted baseline role | Result / important condition |
|---|---|---|---|
| UC-21A | Submit a field logistics request | Rescuer team leader | Persisted request awaits HQ validation. Submission is team-leader-only. Base rescuer identity alone does not grant this POST action. |
| UC-21B | Track or cancel an eligible own request | Rescuer team leader, Rescuer team member | Own request state shown or an allowed cancellation recorded. Ownership and current state limit cancellation. |
| UC-31 | Submit an external resource request | Authorized request partner | Authenticated partner request enters the persisted workflow. Partner authentication/contract validation is separate from human sign-in. |
| UC-32A | Review and record resource requests | Chairperson, Operations / Admin, Response personnel, Recovery / Rehabilitation | Authorized workspace or request record returned.  |
| UC-32B | Validate, return or complete a resource request | Chairperson, Operations / Admin | Validation decision/history/status saved. Module visibility does not confer approval. Status labels come from actual lookup records. |
| UC-33 | Forward a validated request and monitor fulfillment | Chairperson, Operations / Admin | Partner handoff/reference and actual fulfillment evidence recorded. Partner connectivity/acknowledgment is conditional. Forwarded does not mean delivered. |

[Raw Mermaid](11_requests_use_cases.mmd) | [Package index](../00_README.md) | [Current case catalog](../06_REFERENCE/01_current_use_case_catalog.md)
