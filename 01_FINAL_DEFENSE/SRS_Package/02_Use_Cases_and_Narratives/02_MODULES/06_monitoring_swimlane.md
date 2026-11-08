# Read database-backed operational monitoring

Weather/map providers and underlying data must be available. No prototype data should appear as real records. Lanes identify responsibility; arrows identify control/handoff rather than database foreign keys.

```mermaid
flowchart LR
  subgraph lane0["Authorized HQ user"]
    direction TB
    start(["Open permitted monitoring module"])
  end
  subgraph lane1["API"]
    direction TB
    gate{"Module access allowed?"}
    derive["Calculate summaries and versioned history"]
    ready{"Data/provider available?"}
  end
  subgraph lane2["Web client"]
    direction TB
    deny(["Show access denied"])
    none(["Show empty, unavailable or error state"])
    view(["Display real labels, maps and charts"])
  end
  subgraph lane3["Operational data"]
    direction TB
    read[("Read scoped events, statuses and report evidence")]
  end
  start --> gate
  gate -->|"No"| deny
  gate -->|"Yes"| read
  read --> derive
  derive --> ready
  ready -->|"No"| none
  ready -->|"Yes"| view
```

## Use cases and responsibilities

| ID | Goal | Primary actor / permitted baseline role | Result / important condition |
|---|---|---|---|
| UC-22A | Monitor dashboard and operational summaries | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation | Charts/KPIs derive from selected operational database records.  |
| UC-22B | Review maps, directory and weather | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation | Authorized geography/safety/weather data displayed.  |
| UC-24 | Review severity and hazard overlays | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation | Stored severity/hazard evidence displayed. This use case does not claim an implemented arbitrary area-drawing or hazard-edit UI. |
| UC-25A | Review household safety reports | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation | Household safety data shown within geographic scope.  |
| UC-26A | Inspect rescue priorities and historical criteria | Chairperson, Operations / Admin, Response personnel | Database-backed priorities and versioned evidence displayed.  |

[Raw Mermaid](06_monitoring_swimlane.mmd) | [Package index](../00_README.md) | [Current case catalog](../06_REFERENCE/01_current_use_case_catalog.md)
