# Identify, review, export or delete archive evidence

Saved-group snapshots, source records and recording files have different lifecycles. File playback is available only when the actual retained recording exists; the diagram does not assert that every deletion removes every related file. Lanes identify responsibility; arrows identify control/handoff rather than database foreign keys.

```mermaid
flowchart LR
  subgraph lane0["Authorized archive user"]
    direction TB
    start(["Choose archive category and event scope"])
    action{"Choose archive action"}
  end
  subgraph lane1["API / archive service"]
    direction TB
    read["Load actual source IDs and snapshot metadata"]
    validate{"Authorization and source IDs still valid?"}
  end
  subgraph lane2["Web client"]
    direction TB
    view["Show identities, status and recording availability"]
    confirm{"Confirm explicit selected identities for deletion"}
    keep(["Keep original records unchanged"])
    error(["Show stale selection or access error"])
    result(["Refresh actual archive results"])
  end
  subgraph lane3["Archive / report service"]
    direction TB
    export["Export selected records or save validated group"]
  end
  subgraph lane4["Archive service"]
    direction TB
    delete["Apply the implemented scoped deletion"]
  end
  start --> read
  read --> view
  view --> action
  action -->|"Export / save group"| export
  export --> result
  action -->|"Delete"| confirm
  confirm -->|"No"| keep
  confirm -->|"Yes"| validate
  validate -->|"No"| error
  validate -->|"Yes"| delete
  delete --> result
```

## Use cases and responsibilities

| ID | Goal | Primary actor / permitted baseline role | Result / important condition |
|---|---|---|---|
| UC-20B | Monitor rescue communications | Chairperson, Operations / Admin, Response personnel | Authorized HQ can review operational communication metadata.  |
| UC-30 | Browse, export and manage scoped archive evidence | Chairperson, Operations / Admin, Mitigation / Prevention, Preparedness, Response personnel, Recovery / Rehabilitation | Authorized archive evidence reviewed or managed. Use record IDs, source validation and recording availability. Destructive actions still require their own validation/confirmation. |

[Raw Mermaid](09_archive_identification_and_actions.mmd) | [Package index](../00_README.md) | [Current case catalog](../06_REFERENCE/01_current_use_case_catalog.md)
