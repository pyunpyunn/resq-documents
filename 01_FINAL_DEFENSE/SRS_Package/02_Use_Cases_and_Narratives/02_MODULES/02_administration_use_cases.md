# Personnel administration and public inquiries — use cases

Mermaid has no native UML use-case diagram. Actor boxes, oval goals and the system boundary form an explicitly UML-style view; association lines are not a process sequence. Supporting providers are external actors, not additional staff roles.

```mermaid
flowchart LR
  %% UML-style use-case view in Mermaid flowchart notation; neutral lines are associations.
  actoroperationsadmin["Actor: Operations / Admin"]
  actorpublic["Actor: Public visitor"]
  subgraph systemBoundary["RESQPERATION system boundary"]
    caseUC04(["UC-04: Manage rescuer accounts and teams"])
    caseUC05(["UC-05: Manage HQ accounts and roles"])
    caseUC06(["UC-06: Maintain barangay operational profile"])
    caseUC07A(["UC-07A: Submit a public inquiry"])
    caseUC07B(["UC-07B: Review and archive inquiries"])
  end
  actoroperationsadmin --- caseUC04
  actoroperationsadmin --- caseUC05
  actoroperationsadmin --- caseUC06
  actorpublic --- caseUC07A
  actoroperationsadmin --- caseUC07B
```

## Use cases and responsibilities

| ID | Goal | Primary actor / permitted baseline role | Result / important condition |
|---|---|---|---|
| UC-04 | Manage rescuer accounts and teams | Operations / Admin | Validated account/team changes with audit evidence. Personnel access is currently Operations/Admin; a team leader is not automatically a personnel administrator. |
| UC-05 | Manage HQ accounts and roles | Operations / Admin | Account roles and permitted capabilities configured. Role configuration remains bounded by the server policy. |
| UC-06 | Maintain barangay operational profile | Operations / Admin | Authorized profile data updated.  |
| UC-07A | Submit a public inquiry | Public visitor | Validated inquiry stored in landing_inquiries. Public submission does not grant staff review access. |
| UC-07B | Review and archive inquiries | Operations / Admin | Staff handling state and history recorded.  |

[Raw Mermaid](02_administration_use_cases.mmd) | [Package index](../00_README.md) | [Current case catalog](../06_REFERENCE/01_current_use_case_catalog.md)
