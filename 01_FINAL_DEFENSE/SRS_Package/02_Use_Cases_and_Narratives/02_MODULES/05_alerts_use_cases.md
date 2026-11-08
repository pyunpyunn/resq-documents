# Disaster lifecycle and broadcast delivery — use cases

Mermaid has no native UML use-case diagram. Actor boxes, oval goals and the system boundary form an explicitly UML-style view; association lines are not a process sequence. Supporting providers are external actors, not additional staff roles.

```mermaid
flowchart LR
  %% UML-style use-case view in Mermaid flowchart notation; neutral lines are associations.
  actorchair["Actor: Chairperson"]
  actorhouseholdresident["Actor: Household resident"]
  actoroneSignal["Actor: OneSignal mobile push"]
  actoroperationsadmin["Actor: Operations / Admin"]
  actorresponse["Actor: Response personnel"]
  actorsmsGateway["Actor: Configured SMS gateway"]
  actortl["Actor: Rescuer team leader"]
  actortm["Actor: Rescuer team member"]
  subgraph systemBoundary["RESQPERATION system boundary"]
    caseUC09(["UC-09: Receive and review disaster alerts"])
    caseUC23A(["UC-23A: Declare a disaster and publish alert instructions"])
    caseUC23B(["UC-23B: Review, update and close an active event"])
  end
  actorhouseholdresident --- caseUC09
  actortl --- caseUC09
  actortm --- caseUC09
  actoroneSignal --- caseUC09
  actorchair --- caseUC23A
  actoroperationsadmin --- caseUC23A
  actoroneSignal --- caseUC23A
  actorsmsGateway --- caseUC23A
  actorchair --- caseUC23B
  actoroperationsadmin --- caseUC23B
  actorresponse --- caseUC23B
```

## Use cases and responsibilities

| ID | Goal | Primary actor / permitted baseline role | Result / important condition |
|---|---|---|---|
| UC-09 | Receive and review disaster alerts | Household resident, Rescuer team leader, Rescuer team member | App reads stored alerts; eligible devices can receive provider pushes. Notification permission, native build, subscription and network availability are required for push delivery. |
| UC-23A | Declare a disaster and publish alert instructions | Chairperson, Operations / Admin | Event/alert saved; actual provider delivery state recorded. Publishing is Chairperson/Operations-Admin under current policy. A saved alert can still have no recipients or provider failure; only accepted messages have provider IDs. |
| UC-23B | Review, update and close an active event | Chairperson, Operations / Admin, Response personnel | Permitted event lifecycle change recorded. Close/review/update follow their actual route actions; do not assume all publication permissions are identical. |

[Raw Mermaid](05_alerts_use_cases.mmd) | [Package index](../00_README.md) | [Current case catalog](../06_REFERENCE/01_current_use_case_catalog.md)
