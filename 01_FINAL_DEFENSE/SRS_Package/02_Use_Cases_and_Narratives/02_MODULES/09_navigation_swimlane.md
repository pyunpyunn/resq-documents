# Navigate with online or supported saved data

Offline support is limited to implemented native navigation storage/event types and available assets; physical-device validation remains separate. Lanes identify responsibility; arrows identify control/handoff rather than database foreign keys.

```mermaid
flowchart LR
  subgraph lane0["Assigned rescuer"]
    direction TB
    start(["Open own assignment navigation"])
    follow["Follow valid route and record supported trip events"]
  end
  subgraph lane1["API / Mobile client"]
    direction TB
    gate{"Authorized route data available?"}
  end
  subgraph lane2["Mobile client"]
    direction TB
    none(["Show route unavailable; do not fabricate a route"])
    network{"Connected?"}
    cached{"Compatible saved route/pack available?"}
    ack(["Apply acknowledgments; retain failed/pending events"])
  end
  subgraph lane3["Map / routing provider"]
    direction TB
    route["Return an available route"]
  end
  subgraph lane4["Native local storage"]
    direction TB
    queue[("Retain pending navigation events until acknowledged")]
  end
  subgraph lane5["API"]
    direction TB
    sync["On reconnect, validate identity and event replay"]
  end
  start --> gate
  gate -->|"No"| none
  gate -->|"Yes"| network
  network -->|"Yes"| route
  network -->|"No"| cached
  cached -->|"No"| none
  cached -->|"Yes"| follow
  route -->|"Route available"| follow
  route -->|"Provider unavailable"| none
  follow --> queue
  queue -->|"When online"| sync
  sync --> ack
```

## Use cases and responsibilities

| ID | Goal | Primary actor / permitted baseline role | Result / important condition |
|---|---|---|---|
| UC-16 | Navigate and update assigned mission progress | Rescuer team leader, Rescuer team member | Permitted route, progress and foreground location updates recorded. Active-event, assignment ownership, household queue and valid transition rules apply. Mobile completion is not equivalent to the HQ approval endpoint. |
| UC-17 | Use saved navigation and synchronize trip events | Rescuer team leader, Rescuer team member | Supported local trip events receive server acknowledgments after reconnect. Conditional on native storage, valid cached route/pack and device binding. Never generalize this outbox to every mobile write. |

[Raw Mermaid](09_navigation_swimlane.mmd) | [Package index](../00_README.md) | [Current case catalog](../06_REFERENCE/01_current_use_case_catalog.md)
