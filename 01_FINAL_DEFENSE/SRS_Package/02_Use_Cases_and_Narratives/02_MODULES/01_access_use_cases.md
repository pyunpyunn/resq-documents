# Access, recovery and notification registration — use cases

Mermaid has no native UML use-case diagram. Actor boxes, oval goals and the system boundary form an explicitly UML-style view; association lines are not a process sequence. Supporting providers are external actors, not additional staff roles.

```mermaid
flowchart LR
  %% UML-style use-case view in Mermaid flowchart notation; neutral lines are associations.
  actorbrowserPush["Actor: Browser Push service"]
  actorchair["Actor: Chairperson"]
  actorhouseholdresident["Actor: Household resident"]
  actormitigationprevention["Actor: Mitigation / Prevention"]
  actoroneSignal["Actor: OneSignal mobile push"]
  actoroperationsadmin["Actor: Operations / Admin"]
  actorpreparedness["Actor: Preparedness"]
  actorrecoveryrehabilitation["Actor: Recovery / Rehabilitation"]
  actorresponse["Actor: Response personnel"]
  actorsmsGateway["Actor: Configured SMS gateway"]
  actortl["Actor: Rescuer team leader"]
  actortm["Actor: Rescuer team member"]
  subgraph systemBoundary["RESQPERATION system boundary"]
    caseUC01(["UC-01: Sign in, resume access and sign out"])
    caseUC02(["UC-02: Maintain own profile and password"])
    caseUC03(["UC-03: Recover account access"])
    caseUC37(["UC-37: Register a permitted mobile push subscription"])
    caseUC39(["UC-39: Review notifications and enable browser push"])
  end
  actorchair --- caseUC01
  actoroperationsadmin --- caseUC01
  actormitigationprevention --- caseUC01
  actorpreparedness --- caseUC01
  actorresponse --- caseUC01
  actorrecoveryrehabilitation --- caseUC01
  actorhouseholdresident --- caseUC01
  actortl --- caseUC01
  actortm --- caseUC01
  actorchair --- caseUC02
  actoroperationsadmin --- caseUC02
  actormitigationprevention --- caseUC02
  actorpreparedness --- caseUC02
  actorresponse --- caseUC02
  actorrecoveryrehabilitation --- caseUC02
  actorhouseholdresident --- caseUC02
  actortl --- caseUC02
  actortm --- caseUC02
  actorchair --- caseUC03
  actoroperationsadmin --- caseUC03
  actormitigationprevention --- caseUC03
  actorpreparedness --- caseUC03
  actorresponse --- caseUC03
  actorrecoveryrehabilitation --- caseUC03
  actorhouseholdresident --- caseUC03
  actortl --- caseUC03
  actortm --- caseUC03
  actorsmsGateway --- caseUC03
  actorhouseholdresident --- caseUC37
  actortl --- caseUC37
  actortm --- caseUC37
  actoroneSignal --- caseUC37
  actorchair --- caseUC39
  actoroperationsadmin --- caseUC39
  actormitigationprevention --- caseUC39
  actorpreparedness --- caseUC39
  actorresponse --- caseUC39
  actorrecoveryrehabilitation --- caseUC39
  actorbrowserPush --- caseUC39
```

## Use cases and responsibilities

| ID | Goal | Primary actor / permitted baseline role | Result / important condition |
|---|---|---|---|
| UC-01 | Sign in, resume access and sign out | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation, Household resident, Rescuer team leader, Rescuer team member | An authenticated, role-scoped session or a clear rejection. Household owner selection and mobile device binding can restrict the session before operational actions. |
| UC-02 | Maintain own profile and password | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation, Household resident, Rescuer team leader, Rescuer team member | Permitted personal fields or credentials updated. These are role-specific entry points, not permission for every actor to call every listed route. |
| UC-03 | Recover account access | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation, Household resident, Rescuer team leader, Rescuer team member | Verified recovery resets credentials. Security-question recovery and household SMS recovery are different branches; configured contact data, expiry and throttles apply. |
| UC-37 | Register a permitted mobile push subscription | Household resident, Rescuer team leader, Rescuer team member | Real subscription/permission/identity saved on the active backend. Native SDK registration and consent required. Legacy mobile platforms are used for Android only after provider verification. |
| UC-39 | Review notifications and enable browser push | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation | Authorized web notifications or browser subscription updated. Browser push uses VAPID/service-worker configuration and HTTPS requirements; it is separate from mobile OneSignal. |

[Raw Mermaid](01_access_use_cases.mmd) | [Package index](../00_README.md) | [Current case catalog](../06_REFERENCE/01_current_use_case_catalog.md)
