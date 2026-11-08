# RESQPERATION Mock Defense Questions — Draft

Use the current SRS, use-case catalog, architecture reference, must-haves audit, and the defense-build test evidence when answering. The response prompts below are not claims of approval or successful verification.

## System purpose and scope

1. **What problem does RESQPERATION address?**  
   Explain coordination and traceability needs for household safety reports, responder assignments, field updates, resource requests, and situation reports. Cite the SRS scope and show the corresponding demonstrated workflow.

2. **Who are the system's users?**  
   Describe household residents and rescuers using mobile workflows, and authorized HQ/Admin users using the web client. Explain role boundaries using the use-case model.

3. **Does RESQPERATION issue official disaster warnings or replace emergency responders?**  
   No. Describe it as an information and coordination tool; distinguish official authority and external warning sources.

## Design and implementation

4. **Why use a web client and a mobile app?**  
   Relate the clients to HQ monitoring/administration and field/household workflows. Show the architecture diagram and do not imply every feature exists on every client.

5. **How do the clients access data securely?**  
   Explain the API boundary, authentication tokens, backend validation, and backend role authorization. Do not claim a security certification.

6. **What does the ERD represent?**  
   Explain that the submitted ERD is a logical system-scope model. External systems are integration boundaries, not tables owned by RESQPERATION; verify the diagram against the approved schema before claiming physical-schema accuracy.

7. **What technologies and external services are used?**  
   Refer to the stack matrix and identify which integrations are configured, conditional, planned, or merely referenced in the defense build.

## Evidence and research

8. **How were requirements and workflows identified?**  
   Answer using actual approved project records. The copied docs include desk research and requirements notes, but no formal interview/survey artifacts were found in the reviewed set. Do not invent respondents or methods.

9. **What related studies support the project?**  
   Cite only studies actually reviewed and approved for the manuscript. The project resource list and government/legal references are not substitutes for a related-studies chapter.

10. **How do you know the system works?**  
    Show dated tests and verification evidence for the exact build. Separate automated tests from live-device, external-service, and stakeholder acceptance tests.

## Limitations and operations

11. **What happens when connectivity is unavailable?**  
    State the behavior demonstrated for the specific client. The use-case catalog marks persistent household offline reporting and end-to-end offline rescuer navigation as incomplete or partially verified.

12. **What is still incomplete or conditional?**  
    Use the latest audit and current build to explain partial items honestly, including relevant deployment gates and external integrations. Do not rely on an old audit without checking updates.

13. **How is personal data protected?**  
    Describe access controls, data minimization, privacy notices, and masking in the demo as supported by actual implementation/evidence. Do not claim legal compliance solely because a law is cited.

14. **What would you improve next?**  
    Prioritize open acceptance checks, full screenshot/document completion, partner integration verification, offline behavior, and usability feedback based on current evidence.

## Before rehearsal

- Update answers to match the exact defense build and approved SRS.
- Prepare a traceable source/test reference for every factual claim.
- Practice a concise answer, then offer a diagram or evidence file when useful.
- If an answer is unknown, say so and identify how it will be verified.
