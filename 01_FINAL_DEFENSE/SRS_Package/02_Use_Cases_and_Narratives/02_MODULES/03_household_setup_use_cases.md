# Household owner selection, setup and location — use cases

Mermaid has no native UML use-case diagram. Actor boxes, oval goals and the system boundary form an explicitly UML-style view; association lines are not a process sequence. Supporting providers are external actors, not additional staff roles.

```mermaid
flowchart LR
  %% UML-style use-case view in Mermaid flowchart notation; neutral lines are associations.
  actorhouseholdresident["Actor: Household resident"]
  actormapProvider["Actor: Map / routing provider"]
  subgraph systemBoundary["RESQPERATION system boundary"]
    caseUC08(["UC-08: Select phone owner and complete household setup"])
    caseUC12(["UC-12: View evacuation information and available directions"])
    caseUC13A(["UC-13A: Display household verification QR"])
    caseUC14(["UC-14: View saved household information offline"])
  end
  actorhouseholdresident --- caseUC08
  actorhouseholdresident --- caseUC12
  actormapProvider --- caseUC12
  actorhouseholdresident --- caseUC13A
  actorhouseholdresident --- caseUC14
```

## Use cases and responsibilities

| ID | Goal | Primary actor / permitted baseline role | Result / important condition |
|---|---|---|---|
| UC-08 | Select phone owner and complete household setup | Household resident | Current phone is linked to an authorized household member and setup/geotag. Pending-owner tokens cannot perform ordinary household actions. Existing registered Android/iOS platform is preserved. |
| UC-12 | View evacuation information and available directions | Household resident | Available site/map information is displayed. Availability of directions depends on the implemented client, location/provider data and connectivity; do not infer a dedicated household route API. |
| UC-13A | Display household verification QR | Household resident | Household verification information displayed.  |
| UC-14 | View saved household information offline | Household resident | An available account-scoped cached overview can be shown. Current useMobileOverview/mobileSnapshot supports cached reading. This does not establish durable offline household status submission. |

[Raw Mermaid](03_household_setup_use_cases.mmd) | [Package index](../00_README.md) | [Current case catalog](../06_REFERENCE/01_current_use_case_catalog.md)
