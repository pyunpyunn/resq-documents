# RESQPERATION Defense Presentation Script — Draft

**Draft for team review.** Confirm presenter names, assigned sections, duration, current build/version, and every demonstrated feature before rehearsal. Do not describe a conditional or partial feature as fully verified.

## Opening and project

**Presenter 1:** Good day, respected panel members and guests. We are presenting RESQPERATION, a geo-tagged household monitoring and barangay disaster risk reduction and management rescue coordination system. Our project focuses on helping authorized household users, rescuers, and headquarters personnel coordinate disaster-related information through connected mobile and web workflows.

## Problem and purpose

**Presenter 1:** During a disaster, household safety reports, rescue assignments, field updates, resource requests, and situation reports need to be reviewed and coordinated. RESQPERATION provides a shared operational workspace for those activities. It supports authorized decision-makers; it does not replace official warning issuers, emergency services, or the authority of disaster-management offices.

**Presenter 2:** The system is designed around three client roles: HQ/Admin users on the web dashboard, and household residents and rescuers on the mobile application. Each client communicates with the Laravel API. The system also documents integrations with external data and service providers, whose availability depends on configuration.

## Technology and architecture

**Presenter 2:** The documented stack includes a Laravel JSON API, a React and Vite web client, and an Expo/React Native mobile client. The clients call the API rather than connecting directly to the database. Authentication, validation, and role authorization are enforced at the backend boundary. Please refer to the architecture diagram and the verified package versions in our stack reference.

## Demonstration

**Presenter 3:** We will demonstrate the workflows available in the defense build: [insert only tested workflows, such as sign-in, household status reporting, incident monitoring, dispatch, or reporting]. For each step, we will identify the role, the information submitted, and the resulting system response.

**Presenter 3:** This demonstration uses [state build/version and test-data environment]. The records shown are [identify as synthetic/demo or approved live data]. We will not expose personal household information or credentials.

## Testing and limitations

**Presenter 4:** Our test cases and verification records document the flows that have been checked. We distinguish source implementation from end-to-end verification. Some areas have deployment or external-service dependencies; the current use-case catalog and must-haves audit identify partial workflows and remaining acceptance checks. We will not claim offline completion, partner availability, or push delivery unless verified in the build being demonstrated.

## Closing

**Presenter 4:** In summary, RESQPERATION brings household reporting, field response, and headquarters coordination into a role-based system with a documented API and data boundary. We appreciate your time and welcome your questions.

## Rehearsal checklist

- Replace bracketed text with actual, verified build and data details.
- Assign names and speaking parts; fit the approved time limit.
- Rehearse a working demo and a safe fallback recording/screenshots.
- Verify network, accounts, provider services, and test records on the defense device.
- Avoid exposing personal data, credentials, internal hostnames, or tokens.
