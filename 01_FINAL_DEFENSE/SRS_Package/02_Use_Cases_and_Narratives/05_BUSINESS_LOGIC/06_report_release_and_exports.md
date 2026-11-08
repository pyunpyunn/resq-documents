# Prepare or release a scoped report

Internal exports and external release are related but distinct branches. Manual escalation is not an automatic district handoff. Lanes identify responsibility; arrows identify control/handoff rather than database foreign keys.

```mermaid
flowchart LR
  subgraph lane0["HQ reviewer / authorized partner"]
    direction TB
    start(["Select report or request permitted sections"])
  end
  subgraph lane1["API"]
    direction TB
    gate{"Access, contract and source data valid?"}
    external{"External release request?"}
  end
  subgraph lane2["Client / Partner"]
    direction TB
    error(["Show validation or provider error"])
    deliver(["Retrieve permitted file before link expiry"])
  end
  subgraph lane3["Operational data"]
    direction TB
    pending[("Record pending external report request")]
    reject(["Record rejection reason"])
  end
  subgraph lane4["Authorized HQ reviewer"]
    direction TB
    review["Choose event, scope, inputs and release decision"]
    accept{"External release accepted?"}
  end
  subgraph lane5["API / Operational data"]
    direction TB
    snapshot["Generate recorded summary or accepted snapshot"]
  end
  subgraph lane6["Report file storage"]
    direction TB
    file[("Create requested export and signed access when applicable")]
  end
  start --> gate
  gate -->|"No"| error
  gate -->|"Yes"| external
  external -->|"Yes"| pending
  external -->|"No: internal export"| snapshot
  pending --> review
  review --> accept
  accept -->|"No"| reject
  accept -->|"Yes"| snapshot
  snapshot --> file
  file --> deliver
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

[Raw Mermaid](06_report_release_and_exports.mmd) | [Package index](../00_README.md) | [Current case catalog](../06_REFERENCE/01_current_use_case_catalog.md)
