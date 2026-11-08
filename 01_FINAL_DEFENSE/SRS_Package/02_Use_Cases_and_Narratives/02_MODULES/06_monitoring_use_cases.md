# Dashboard, maps, weather and priorities — use cases

Mermaid has no native UML use-case diagram. Actor boxes, oval goals and the system boundary form an explicitly UML-style view; association lines are not a process sequence. Supporting providers are external actors, not additional staff roles.

```mermaid
flowchart LR
  %% UML-style use-case view in Mermaid flowchart notation; neutral lines are associations.
  actorchair["Actor: Chairperson"]
  actormitigationprevention["Actor: Mitigation / Prevention"]
  actoroperationsadmin["Actor: Operations / Admin"]
  actorpreparedness["Actor: Preparedness"]
  actorrecoveryrehabilitation["Actor: Recovery / Rehabilitation"]
  actorresponse["Actor: Response personnel"]
  actorweatherProvider["Actor: Weather / advisory provider"]
  subgraph systemBoundary["RESQPERATION system boundary"]
    caseUC22A(["UC-22A: Monitor dashboard and operational summaries"])
    caseUC22B(["UC-22B: Review maps, directory and weather"])
    caseUC24(["UC-24: Review severity and hazard overlays"])
    caseUC25A(["UC-25A: Review household safety reports"])
    caseUC26A(["UC-26A: Inspect rescue priorities and historical criteria"])
  end
  actorchair --- caseUC22A
  actoroperationsadmin --- caseUC22A
  actormitigationprevention --- caseUC22A
  actorpreparedness --- caseUC22A
  actorresponse --- caseUC22A
  actorrecoveryrehabilitation --- caseUC22A
  actorchair --- caseUC22B
  actoroperationsadmin --- caseUC22B
  actormitigationprevention --- caseUC22B
  actorpreparedness --- caseUC22B
  actorresponse --- caseUC22B
  actorrecoveryrehabilitation --- caseUC22B
  actorweatherProvider --- caseUC22B
  actorchair --- caseUC24
  actoroperationsadmin --- caseUC24
  actormitigationprevention --- caseUC24
  actorpreparedness --- caseUC24
  actorresponse --- caseUC24
  actorrecoveryrehabilitation --- caseUC24
  actorweatherProvider --- caseUC24
  actorchair --- caseUC25A
  actoroperationsadmin --- caseUC25A
  actormitigationprevention --- caseUC25A
  actorpreparedness --- caseUC25A
  actorresponse --- caseUC25A
  actorrecoveryrehabilitation --- caseUC25A
  actorchair --- caseUC26A
  actoroperationsadmin --- caseUC26A
  actorresponse --- caseUC26A
```

## Use cases and responsibilities

| ID | Goal | Primary actor / permitted baseline role | Result / important condition |
|---|---|---|---|
| UC-22A | Monitor dashboard and operational summaries | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation | Charts/KPIs derive from selected operational database records.  |
| UC-22B | Review maps, directory and weather | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation | Authorized geography/safety/weather data displayed.  |
| UC-24 | Review severity and hazard overlays | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation | Stored severity/hazard evidence displayed. This use case does not claim an implemented arbitrary area-drawing or hazard-edit UI. |
| UC-25A | Review household safety reports | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation | Household safety data shown within geographic scope.  |
| UC-26A | Inspect rescue priorities and historical criteria | Chairperson, Operations / Admin, Response personnel | Database-backed priorities and versioned evidence displayed.  |

[Raw Mermaid](06_monitoring_use_cases.mmd) | [Package index](../00_README.md) | [Current case catalog](../06_REFERENCE/01_current_use_case_catalog.md)
