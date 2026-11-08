# Baseline role/capability matrix

These are policy maxima from unpersisted role models. Configured web_modules may narrow access; inactive/deleted accounts, household owner selection, assignment ownership and device binding add further restrictions. TL/TM use base rescuer capability plus assigned-role checks; generic legacy rescuer actions do not imply team-leader request-submission rights.

| Role | Baseline web modules | Request approval | Publish alert | Create dispatch | HQ complete dispatch | Personnel |
|---|---|---|---|---|---|---|
| Operations / Admin | dashboard, geospatial_analytics, response_operations, resources_requests, reports_documentation, personnel_access, profile, notifications, inquiries | Yes | Yes | Yes | Yes | Yes |
| Chairperson | dashboard, geospatial_analytics, response_operations, resources_requests, reports_documentation, profile, notifications | Yes | Yes | Yes | Yes | No |
| Mitigation / Prevention | dashboard, geospatial_analytics, reports_documentation, profile, notifications | No | No | No | No | No |
| Preparedness | dashboard, geospatial_analytics, reports_documentation, profile, notifications | No | No | No | No | No |
| Response personnel | dashboard, geospatial_analytics, response_operations, resources_requests, reports_documentation, profile, notifications | No | No | Yes | No | No |
| Recovery / Rehabilitation | dashboard, geospatial_analytics, resources_requests, reports_documentation, profile, notifications | No | No | No | No | No |
| Household resident | Mobile roles; no HQ modules | No | No | No | No | No |
| Rescuer team leader | Mobile roles; no HQ modules | No | No | No | No | No |
| Rescuer team member | Mobile roles; no HQ modules | No | No | No | No | No |

Report-release review follows reports_documentation module access and its record/contract checks; it is not automatically the same permission as resource-request approval. Public inquiry submission does not expose inquiry review. Evacuation verifier support is an API path, not a new account role.
