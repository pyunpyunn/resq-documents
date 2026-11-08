# Dispatch a scoped rescue assignment

HQ approval and mobile household-queue completion are different endpoints with different guards. Lanes identify responsibility; arrows identify control/handoff rather than database foreign keys.

```mermaid
flowchart LR
  subgraph lane0["Authorized HQ dispatcher"]
    direction TB
    start(["Review actual household needs and team availability"])
    select[/"Select incident, targets and responders"/]
  end
  subgraph lane1["API"]
    direction TB
    gate{"Role, active event and assignment scope valid?"}
  end
  subgraph lane2["Web client"]
    direction TB
    error(["Show validation or availability conflict"])
  end
  subgraph lane3["Operational data"]
    direction TB
    save[("Save assignment and target queue")]
    evidence[("Persist scoped progress and field evidence")]
  end
  subgraph lane4["Delivery services"]
    direction TB
    deliver["Publish updates and attempt eligible push"]
  end
  subgraph lane5["Assigned rescuer"]
    direction TB
    rescuer["Read own assignment and update allowed progress"]
  end
  subgraph lane6["Authorized HQ user"]
    direction TB
    review(["Review results; complete only with permitted action"])
  end
  start --> select
  select --> gate
  gate -->|"No"| error
  gate -->|"Yes"| save
  save --> deliver
  deliver --> rescuer
  rescuer --> evidence
  evidence --> review
```

## Use cases and responsibilities

| ID | Goal | Primary actor / permitted baseline role | Result / important condition |
|---|---|---|---|
| UC-15 | View own assigned incidents and households | Rescuer team leader, Rescuer team member | Only the authorized rescuer assignment/household scope is returned.  |
| UC-16 | Navigate and update assigned mission progress | Rescuer team leader, Rescuer team member | Permitted route, progress and foreground location updates recorded. Active-event, assignment ownership, household queue and valid transition rules apply. Mobile completion is not equivalent to the HQ approval endpoint. |
| UC-25B | Confirm a household status report | Chairperson, Operations / Admin, Response personnel | Authorized operational confirmation recorded.  |
| UC-26A | Inspect rescue priorities and historical criteria | Chairperson, Operations / Admin, Response personnel | Database-backed priorities and versioned evidence displayed.  |
| UC-26B | Dispatch a rescue team | Chairperson, Operations / Admin, Response personnel | Validated assignment targets and team/responder scope saved.  |
| UC-26C | Complete a dispatch through HQ approval | Chairperson, Operations / Admin | Permitted HQ completion recorded. HQ completion is an approve action, distinct from rescuer household-queue progress. |
| UC-27 | Monitor field reports and team progress | Chairperson, Operations / Admin, Response personnel | HQ operational progress/evidence displayed.  |

[Raw Mermaid](07_dispatch_swimlane.mmd) | [Package index](../00_README.md) | [Current case catalog](../06_REFERENCE/01_current_use_case_catalog.md)
