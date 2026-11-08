# Validate and persist field assessment evidence

QR/check-in API support does not establish a separate scanner role or a fully deployed scanning UI. Lanes identify responsibility; arrows identify control/handoff rather than database foreign keys.

```mermaid
flowchart LR
  subgraph lane0["Assigned rescuer / verifier"]
    direction TB
    start(["Open assigned household or verification task"])
  end
  subgraph lane1["Mobile client"]
    direction TB
    entry[/"Capture check-in, member status and catalog damage"/]
    reject(["Correct stale scope, missing data or invalid choice"])
  end
  subgraph lane2["API"]
    direction TB
    gate{"Identity, event, queue and fields valid?"}
  end
  subgraph lane3["Operational data"]
    direction TB
    save[("Persist report and permitted status/verification links")]
  end
  subgraph lane4["Authorized HQ user"]
    direction TB
    review(["Read field findings and current safety evidence"])
  end
  start --> entry
  entry --> gate
  gate -->|"No"| reject
  gate -->|"Yes"| save
  save --> review
```

## Use cases and responsibilities

| ID | Goal | Primary actor / permitted baseline role | Result / important condition |
|---|---|---|---|
| UC-13B | Verify evacuation arrival | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation, Rescuer team leader, Rescuer team member | Authorized verification/check-in updates shared evacuation evidence. Backend verifier access is supported; a dedicated scanner account role or complete staff scanning UI is not established by these routes. |
| UC-18 | Record check-in and member assessment | Rescuer team leader, Rescuer team member | Scoped field/check-in evidence recorded.  |
| UC-19 | Submit field findings and damage assessment | Rescuer team leader, Rescuer team member | Validated report header, member assessment and catalog damage choice stored. Actual database keys/labels, assignment/event scope and retry protections are used. |
| UC-27 | Monitor field reports and team progress | Chairperson, Operations / Admin, Response personnel | HQ operational progress/evidence displayed.  |

[Raw Mermaid](04_field_assessment_evidence.mmd) | [Package index](../00_README.md) | [Current case catalog](../06_REFERENCE/01_current_use_case_catalog.md)
