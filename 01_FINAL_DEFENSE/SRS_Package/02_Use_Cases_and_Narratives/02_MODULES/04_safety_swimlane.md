# Record an authorized household or member safety report

SMS enters through a separately signed gateway path, not an unrestricted alternate login. Lanes identify responsibility; arrows identify control/handoff rather than database foreign keys.

```mermaid
flowchart LR
  subgraph lane0["Household resident"]
    direction TB
    start(["Choose current household, member or trusted report"])
    send[/"Submit safety status and allowed details"/]
  end
  subgraph lane1["Mobile client"]
    direction TB
    choose["Display persisted event/status choices"]
  end
  subgraph lane2["API"]
    direction TB
    scope{"Identity, event and trusted permissions valid?"}
  end
  subgraph lane3["Client"]
    direction TB
    reject(["Show validation or access error"])
  end
  subgraph lane4["Operational data"]
    direction TB
    save[("Persist status evidence and current event state")]
  end
  subgraph lane5["HQ / Mobile clients"]
    direction TB
    show(["Refresh monitoring and status history"])
  end
  start --> choose
  choose --> send
  send --> scope
  scope -->|"No"| reject
  scope -->|"Yes"| save
  save --> show
```

## Use cases and responsibilities

| ID | Goal | Primary actor / permitted baseline role | Result / important condition |
|---|---|---|---|
| UC-10 | Report household or member safety | Household resident | Authorized status/history records updated. Use the active event and actual configured database/broadcast status choices. |
| UC-11 | Connect and assist a trusted household | Household resident | A permitted trusted connection can report scoped member status. A household ID alone is insufficient: connection state and PIN/permission checks apply. |
| UC-25A | Review household safety reports | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation | Household safety data shown within geographic scope.  |
| UC-38 | Report safety through a configured SMS gateway | Household resident | A verified sender can record supported event status. Gateway signature/timestamp, matching household contact, active event and supported keyword are required. |

[Raw Mermaid](04_safety_swimlane.mmd) | [Package index](../00_README.md) | [Current case catalog](../06_REFERENCE/01_current_use_case_catalog.md)
