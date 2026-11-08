# SRS and Attachment Package

This folder is a companion packet for the SRS. It contains copies of source documents and attachments; it does not silently alter or replace the existing SRS DOCX.

## Contents

- `01_SRS_Documents` — copies of the SRS DOCX versions and editable Markdown source.
- `02_Use_Cases_and_Narratives` — the canonical system use-case catalog and role-specific use-case diagrams.
- `03_System_Architecture` — architecture, system-context, and roles/auth diagram sources.
- `04_ERD` — logical scope ERD and data-model diagram sources.
- `05_UI_Screenshots` — the one existing rescuer navigation capture, with a note about its limits.
- `06_Other_Diagram_Attachments` — supplementary workflow, data-flow, security, radio, and reporting diagrams.

## Completion status

The SRS Markdown source contains use-case narratives and Mermaid diagram source, and the screenshot figures are placeholders. The final SRS DOCX was checked and contains no embedded image/media files. The available project screenshot is not a full set of current screens and shows the navigation screen with no active dispatch assigned.

The supplied DOCX files and Markdown source are also different revisions: `RESQPERATION_SRS_v1.0_FINAL.docx` identifies itself as Version 1.0 dated October 6, 2026, while the Markdown source identifies itself as Version 1.2 dated October 23, 2026. They should not be combined or submitted as if they were the same revision. The team/adviser should select and reconcile one approved SRS baseline before final submission.

Before submitting the SRS, the team should:

1. Capture current screenshots from the actual defense build for web login/dashboard/maps and household/rescuer workflows.
2. Mask personal or operationally sensitive data and label each screenshot with client and build/version.
3. Export the approved use-case, architecture, and ERD diagrams to readable image/PDF formats.
4. Insert approved images into the submission SRS at the existing placeholders, retain editable sources in this packet, and check pagination/captions.
5. Confirm the ERD against the approved schema and confirm that all narratives match the demonstrated build.

The Mermaid `.md` files are editable diagram sources; they are attachments for review, not proof that images have already been embedded in the DOCX.
