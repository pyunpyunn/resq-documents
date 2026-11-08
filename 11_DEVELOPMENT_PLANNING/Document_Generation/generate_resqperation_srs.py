from __future__ import annotations

import subprocess
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parent.parent
PROJECT = ROOT / "resqperation-system"
OUTPUT = Path(__file__).resolve().parent / "RESQPERATION_SRS_v1.0_FINAL.docx"
AS_OF = "October 6, 2026"


def field(paragraph, instruction: str, placeholder: str = "Update this field in Word") -> None:
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    code = OxmlElement("w:instrText")
    code.set(qn("xml:space"), "preserve")
    code.text = instruction
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = placeholder
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.extend([begin, code, separate, text, end])


def table(doc, headers, rows, widths=None):
    result = doc.add_table(rows=1, cols=len(headers))
    result.style = "Table Grid"
    result.alignment = WD_TABLE_ALIGNMENT.CENTER
    result.autofit = False
    header_props = result.rows[0]._tr.get_or_add_trPr()
    header_repeat = OxmlElement("w:tblHeader")
    header_repeat.set(qn("w:val"), "true")
    header_props.append(header_repeat)
    all_rows = [headers] + rows
    for row_number, values in enumerate(all_rows):
        cells = result.rows[0].cells if row_number == 0 else result.add_row().cells
        for index, value in enumerate(values):
            cell = cells[index]
            cell.text = ""
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(str(value))
            r.font.name = "Calibri"
            r.font.size = Pt(8.2)
            if row_number == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            props = cell._tc.get_or_add_tcPr()
            shade = OxmlElement("w:shd")
            shade.set(qn("w:fill"), "17365D" if row_number == 0 else ("F2F6FA" if row_number % 2 == 0 else "FFFFFF"))
            props.append(shade)
            if widths:
                cell.width = Inches(widths[index])
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return result


def bullets(doc, items):
    for text in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(2)
        p.add_run(text)


def numbered(doc, items):
    for text in items:
        p = doc.add_paragraph(style="List Number")
        p.paragraph_format.space_after = Pt(3)
        p.add_run(text)


def requirements(doc, heading, items):
    doc.add_heading(heading, level=3)
    table(doc, ["Req. ID", "Requirement Description", "Priority", "Current Status"], items, [0.82, 4.0, 0.72, 1.25])


def revisions():
    result = subprocess.run(
        ["git", "-C", str(PROJECT), "log", "main", "--since=2026-09-29 00:00:00", "--date=short", "--format=%h%x09%ad%x09%s"],
        check=True, capture_output=True, text=True,
    )
    rows = []
    for line in result.stdout.splitlines():
        parts = line.split("\t", 2)
        if len(parts) == 3:
            rows.append([parts[0], parts[1], parts[2], ""])
    if not rows:
        raise RuntimeError("No main-branch commits found for revision history")
    return rows


def build():
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Inches(.7)
    sec.bottom_margin = Inches(.7)
    sec.left_margin = Inches(.8)
    sec.right_margin = Inches(.8)
    sec.header_distance = Inches(.3)
    sec.footer_distance = Inches(.3)
    styles = doc.styles
    styles["Normal"].font.name = "Calibri"
    styles["Normal"].font.size = Pt(10.5)
    styles["Normal"].paragraph_format.space_after = Pt(6)
    for name, size in (("Title", 26), ("Heading 1", 17), ("Heading 2", 13), ("Heading 3", 11)):
        st = styles[name]
        st.font.name = "Calibri"
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = RGBColor(23, 54, 93)
        st.paragraph_format.keep_with_next = True
    h = sec.header.paragraphs[0]
    h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    h.add_run("RESQPERATION | SOFTWARE REQUIREMENTS SPECIFICATION").font.size = Pt(8)
    f = sec.footer.paragraphs[0]
    f.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    f.add_run("Page ")
    field(f, "PAGE")

    # Cover page follows the supplied university SRS cover-page pattern; personal names remain blank.
    for text in ("UNIVERSITY OF SAN JOSE-RECOLETOS", "School of Computer Studies", "Cebu City, Philippines"):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(13 if text.startswith("UNIVERSITY") else 11)
    doc.add_paragraph()
    p = doc.add_paragraph(style="Title")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("RESQPERATION")
    for text, size in (
        ("A Geo-Tagged Household Monitoring and BDRRM Rescue Coordination System", 15),
        ("Software Requirements Specification", 18),
        ("Version 1.0 | " + AS_OF, 11),
    ):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(text)
        r.bold = size > 12
        r.font.size = Pt(size)
    doc.add_paragraph()
    for text in (
        "A Capstone Project Presented to the Faculty of the",
        "School of Computer Studies",
        "University of San Jose-Recoletos",
        "In Partial Fulfillment of the Requirements for",
        "Associate in Computer Technology, Major in Software Development",
    ):
        p = doc.add_paragraph(text)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
    doc.add_paragraph()
    p = doc.add_paragraph("Presented by:")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.runs[0].bold = True
    for _ in range(4):
        p = doc.add_paragraph("________________________________________")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(1)
    p = doc.add_paragraph("Capstone Adviser:")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.runs[0].bold = True
    p = doc.add_paragraph("________________________________________")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()

    doc.add_heading("Revision History", level=1)
    doc.add_paragraph(
        "The table records commits on the public main branch from September 29, 2026 through the latest main commit available on October 6, 2026. Commit IDs and messages are read from Git history; author names are intentionally blank. Earlier history remains available at the repository URL."
    )
    history = revisions()
    table(doc, ["Commit", "Date", "Revision / Change", "Author(s)"], history, [.72, .85, 4.45, .75])
    p = doc.add_paragraph()
    p.add_run("Repository: ").bold = True
    p.add_run("https://github.com/pyunpyunn/G10-CAPSTONE.git")
    doc.add_heading("Document Control", level=1)
    table(doc, ["Control Field", "Value"], [
        ["System", "RESQPERATION: A Geo-Tagged Household Monitoring and BDRRM Rescue Coordination System"],
        ["Document", "Software Requirements Specification, Version 1.0"],
        ["Status", "Requirements baseline for review; implementation gaps are identified in Appendix B."],
        ["Prepared by", "________________________________________"],
        ["Reviewed by", "________________________________________"],
        ["Approved by", "________________________________________"],
        ["Date", AS_OF],
    ], [1.5, 5.1])
    doc.add_heading("Table of Contents", level=1)
    field(doc.add_paragraph(), 'TOC \\o "1-3" \\h \\z \\u')
    doc.add_paragraph("Update the table field in Microsoft Word to refresh page numbers and heading links.")
    doc.add_page_break()

    # 1. Introduction
    doc.add_heading("1. Introduction", level=1)
    doc.add_heading("1.1 Purpose", level=2)
    doc.add_paragraph(
        "This Software Requirements Specification defines the functional, interface, data, security, operational, and quality requirements for RESQPERATION. The system is a barangay disaster-response coordination platform for Headquarters (HQ)/Dispatcher personnel, household residents, and on-site rescuers. It combines an HQ/Admin web application and role-specific mobile workflows with a central Laravel API and configurable MySQL data connections."
    )
    doc.add_paragraph(
        "This document follows the supplied SRS structure and is based on project documentation in docs/ and FOR DEV/, the active source tree in resqperation-system/, and the public main-branch history checked on October 6, 2026. Requirements describe the intended system; Appendix B separately distinguishes source implementation from independently verified operation."
    )
    doc.add_heading("1.2 Scope", level=2)
    doc.add_paragraph(
        "RESQPERATION supports barangay disaster monitoring and response coordination. HQ/Admin personnel manage disaster events and broadcasts, monitor household and field reports, view maps and weather, dispatch responders, validate resource requests, generate situation reports, and archive operational records. Household residents use mobile functions to set household geotags, view household/member information, report safety status, access evacuation QR information, and manage trusted-household connections. Rescuers use mobile functions to view and update assignments, navigate to target areas, submit field reports and check-ins, request resources, and exchange team voice clips."
    )
    doc.add_paragraph(
        "The system does not replace PAGASA as the official warning source, BDRRM leadership, emergency radio infrastructure, or TrackingAid's inventory and physical fulfillment responsibility. SafeTrack is a source of shared household/account data; EvaTrack may submit requests; TrackingAid receives validated handoffs."
    )
    doc.add_heading("1.3 Definitions, Acronyms, and Abbreviations", level=2)
    table(doc, ["Term", "Definition"], [
        ["BDRRM / BDRRMC", "Barangay Disaster Risk Reduction and Management / Committee."],
        ["HQ / Dispatcher", "Authorized headquarters personnel coordinating incidents, alerts, resources, and responders."],
        ["Household resident", "Authenticated user associated with a household and using the mobile application."],
        ["Rescuer / responder", "Authenticated field-response user associated with a rescue team and operational tasks."],
        ["Disaster event", "Active or historical event associated with alerts, household reports, assignments, and SitReps."],
        ["Geotag", "Latitude/longitude and location metadata attached to a household, device, report, responder, or route."],
        ["SitRep", "Situation Report: structured operational summary for a selected disaster event and reporting period."],
        ["PTT", "Push-to-talk interaction; the current app records and uploads voice clips, not continuous live audio."],
        ["Sanctum", "Laravel token authentication used by API clients."],
        ["OneSignal", "Third-party provider for mobile subscription registration and push delivery."],
        ["SafeTrack", "Shared-system source for household identity/account data."],
        ["EvaTrack", "External system that can submit evacuation, personnel, or resource requests."],
        ["TrackingAid", "External system/database receiving validated request handoffs and supplying inventory data when available."],
        ["Open-Meteo / PAGASA", "Open-Meteo provides structured weather snapshots; PAGASA remains the official warning source."],
    ], [1.45, 5.15])
    doc.add_heading("1.4 References", level=2)
    bullets(doc, [
        "resqperation-system/README.md and the active backend-laravel, frontend-web, and frontend-mobile source trees.",
        "docs/RESQPERATION_SYSTEM_CLEANUP_AND_CURRENT_STATE.md and docs/RESQPERATION_G10_STEP_BY_STEP_CHECKLIST.md.",
        "docs/RESQPERATION_FINAL_DEFENSE_STUDY_GUIDE_AND_DIAGRAMS.md and docs/diagrams/01 through 21.",
        "docs/RESQPERATION_REQUIREMENTS_BREAKDOWN.md, RESQPERATION_TRACKINGAID_REQUEST_INTEGRATION_GUIDE.md, and RESQPERATION_RESCUER_RADIO_COMMUNICATION.md.",
        "FOR DEV/API_REFERENCE.md, FOR DEV/GEOTAGGING_DISPATCH_ROUTING.md, and FOR DEV/PUSH_NOTIFICATIONS.md as supplementary design references.",
        "GitHub main branch: https://github.com/pyunpyunn/G10-CAPSTONE.git (history checked October 6, 2026).",
        "Republic Act No. 10121, Philippine Disaster Risk Reduction and Management Act of 2010.",
        "Republic Act No. 10173, Data Privacy Act of 2012, and its Implementing Rules and Regulations.",
        "Official Laravel, React, Expo, MySQL, OpenStreetMap, OSRM, Open-Meteo, PAGASA, and OneSignal documentation as applicable.",
    ])
    doc.add_heading("1.5 Overview", level=2)
    doc.add_paragraph(
        "Section 2 describes the product, users, operating environment, constraints, assumptions, and priorities. Section 3 defines interfaces, functional and non-functional requirements, end-to-end flows, and database requirements. Appendix A summarizes system flow, Appendix B records status and verification limits, Appendix C lists acceptance criteria, and Appendix D lists source evidence."
    )

    # 2. Overall Description
    doc.add_heading("2. Overall Description", level=1)
    doc.add_heading("2.1 Product Perspective", level=2)
    doc.add_paragraph(
        "The system has a presentation layer, application layer, and data/integration layer. The React + Vite web client serves HQ/Admin workflows. One Expo React Native app provides household and rescuer role-specific mobile screens. Both clients use the same versioned Laravel JSON API; neither connects directly to MySQL. Laravel performs authentication, authorization, validation, operational workflows, data access, queued work, file handling, and integration handoffs."
    )
    doc.add_paragraph(
        "The primary application database is selected through backend environment configuration and may target local or shared MySQL. SQLite in-memory is used by automated tests. TrackingAid is configured as a separate database connection. The application reuses the approved shared schema and must not assume a destructive clean-database reset."
    )
    table(doc, ["Layer", "Components and Responsibility"], [
        ["Presentation", "React/Vite HQ/Admin web app; Expo React Native household and rescuer mobile app."],
        ["Application/API", "Laravel 13 JSON API under /api/v1; routes, Sanctum, role middleware, validation, controllers, workflows/services, queries, presenters, and resources."],
        ["Data/storage", "Configured MySQL application database; separate TrackingAid connection; Laravel cache/queue/jobs, scheduled tasks, file/audio storage, and logs."],
        ["External services", "SafeTrack, EvaTrack, TrackingAid, OneSignal, Open-Meteo, PAGASA, map tiles, and OSRM routing."],
    ], [1.35, 5.25])
    doc.add_heading("2.2 Product Functions", level=2)
    doc.add_paragraph("At a summary level, RESQPERATION shall provide the following functions:")
    numbered(doc, [
        "Authenticate users and enforce role access for super administrators, HQ/Admin personnel, household residents, and rescuers.",
        "Present HQ/Admin dashboard summaries for events, households, dispatches, requests, weather, mapping, and recent activity.",
        "Create and manage disaster events and broadcasts, define recipient scope, retain broadcast records, and deliver configured mobile alerts.",
        "Collect and display household profiles, member/device data, geotags, household status reports/history, and evacuation verification.",
        "Display household, evacuation-site, responder, assignment, and route information on web/mobile maps with supported routing.",
        "Create rescue assignments, select teams/responders, record progress and locations, and monitor field operations.",
        "Support rescuer profile workflows, household check-ins, field reports, team radio voice clips, and resource requests.",
        "Receive requests from internal/external sources, validate at HQ, prevent duplicate external references, forward approved requests to TrackingAid, and retain status/handoff history.",
        "Fetch/store weather snapshots, display PAGASA references, generate SitReps, and retrieve/export archived records.",
        "Register mobile devices and deliver configured OneSignal push notifications; provide HQ notifications, profiles, and enabled inquiry workflows.",
    ])
    doc.add_heading("2.3 User Classes and Characteristics", level=2)
    table(doc, ["User Class", "Primary Responsibilities", "Client / Access"], [
        ["HQ / Dispatcher (admin)", "Monitor events/status, broadcast alerts, dispatch teams, validate/forward requests, review maps/weather, generate SitReps, archive records.", "React/Vite web; admin API role."],
        ["Super Admin", "System-wide administration and enabled inquiry/administrative workflows.", "React/Vite web; super_admin API role."],
        ["Household Resident", "Complete setup/geotagging, view family data, submit household/member status, view history/QR, manage trusted connections.", "Expo mobile; household_resident API role."],
        ["Rescuer", "View/update assignments, share location, navigate, submit reports/check-ins, request resources, use team voice clips, manage profile.", "Expo mobile; rescuer API role."],
        ["Evacuation Personnel", "Verify household QR through an authorized evacuation workflow; represented by an authorized rescuer/HQ account in current roles.", "Authorized workflow; no separate public role is defined."],
        ["External system", "Submit authenticated requests or exchange data through defined integration boundaries.", "Server-to-server API/database integration."],
    ], [1.35, 3.65, 1.6])
    doc.add_heading("2.4 Operating Environment", level=2)
    bullets(doc, [
        "Backend: Laravel 13 and PHP 8.3 or versions supported by installed dependencies.",
        "Web: React + Vite in a current desktop browser; Leaflet/React Leaflet for mapping.",
        "Mobile: Expo React Native on Android/iOS; GPS, QR/camera, microphone/audio, and push features depend on device permissions/build support. Expo Go is for UI/API testing and does not provide the full native push capability.",
        "Database: MySQL for application/shared data, SQLite in-memory for automated tests, and a separate configurable MySQL connection for TrackingAid.",
        "Network: clients use HTTP(S) to Laravel. A physical phone must use a reachable LAN address during local testing; phone localhost is not the development computer.",
        "Mapping and routing use configured map tiles and route services; provider availability and usage limits apply.",
        "Weather snapshots use Open-Meteo; official warning confirmation uses PAGASA. Direct PAGASA API access is optional and credential/approval dependent.",
    ])
    doc.add_heading("2.5 Design and Implementation Constraints", level=2)
    bullets(doc, [
        "Clients access operational data only through Laravel APIs and do not connect directly to the database.",
        "API routes use /api/v1; protected endpoints use Sanctum tokens and role middleware.",
        "Database endpoints, secrets, and external credentials reside in protected environment configuration, not public client code.",
        "The application reuses the approved active database schema. Do not run migrate:fresh, db:wipe, or unapproved schema changes on shared databases.",
        "Shared database changes and SQL proposals require DB-owner/team review; changes should be additive/reversible where applicable.",
        "Cross-database TrackingAid delivery is not atomic with the main database transaction; queued/outbox processing is eventually consistent.",
        "Open-Meteo data is operational context, not an official warning. HQ confirms warnings through PAGASA before broadcasting.",
        "Current radio communication is voice-clip based, not continuous WebRTC or hardware-radio integration.",
        "Operational pages do not replace missing live data with fabricated sample records.",
    ])
    doc.add_heading("2.6 Assumptions and Dependencies", level=2)
    bullets(doc, [
        "The barangay/BDRRMC supplies accurate household, responder, team, evacuation-center, and operational reference data with authority to use it.",
        "SafeTrack/shared records are available and correctly linked for household identity and account lookup.",
        "HQ/Admin accounts are provisioned by authorized administrators; there is no unrestricted public registration for operational accounts.",
        "Users grant GPS, camera/QR, microphone, and notification permissions when using the corresponding device feature.",
        "Push notification acceptance depends on OneSignal configuration, native build, device subscription, permission, and network access.",
        "TrackingAid supplies valid credentials, database grants, handoff schema, and status/fulfillment information; delivery may be delayed by external outages.",
        "Weather, map-tile, and routing providers may be rate-limited or unavailable; unavailable results must not be presented as confirmed data.",
        "The operator configures the correct local/shared database values for each environment.",
    ])
    doc.add_heading("2.7 Apportioning of Requirements", level=2)
    doc.add_paragraph(
        "Must requirements define minimum scope: role-protected access, disaster/event and household status workflows, mapping/geotags, rescue dispatch and field updates, request validation/handoff, and reporting/archive access. Should requirements include external-device push acceptance, complete cross-system fulfillment feedback, and continuously refreshed operations. Could enhancements include live WebRTC radio, predictive analytics, direct PAGASA API integration, and extended offline synchronization. Deferral of a Must requirement requires explicit adviser/project-owner approval; a source route alone is not acceptance evidence."
    )

    # 3. Specific Requirements
    doc.add_heading("3. Specific Requirements", level=1)
    doc.add_paragraph(
        "Requirements use unique identifiers and verifiable shall statements. Priority uses Must, Should, or Could. The status column reflects source evidence as of October 6, 2026 and is not a substitute for field testing or user acceptance."
    )
    doc.add_heading("3.1 External Interface Requirements", level=2)
    doc.add_heading("3.1.1 User Interfaces", level=3)
    bullets(doc, [
        "The web interface shall provide authenticated HQ/Admin and enabled Super Admin workspaces, operational pages, forms, filters, detail views, and loading/error/empty states.",
        "The mobile interface shall provide household and rescuer workflows in one Expo app and route users according to API role metadata.",
        "The interface shall distinguish reported, verified, pending, stale, and unavailable data where those states apply.",
        "Forms shall show API validation errors and action results in understandable language; consequential actions shall require confirmation where applicable.",
        "HQ review shall preserve the source attribution of household/responder reports and shall not imply that HQ personally observed a field condition.",
    ])
    doc.add_heading("3.1.2 Hardware Interfaces", level=3)
    doc.add_paragraph(
        "No dedicated rescue hardware is required. Mobile workflows may use phone GPS/location services, camera for QR scanning, microphone/audio recording for radio clips, and operating-system notification services. Availability depends on device capability, granted permission, application build, and network connectivity."
    )
    doc.add_heading("3.1.3 Software Interfaces", level=3)
    table(doc, ["Interface", "Purpose", "Protocol / Boundary"], [
        ["Laravel API", "Shared business operations for web/mobile.", "JSON REST under /api/v1; Sanctum bearer tokens for protected routes."],
        ["Primary MySQL", "Users, roles, households, events, reports, responder operations, requests, and notifications.", "Laravel configured connection; credentials from backend environment."],
        ["TrackingAid DB", "Receive forwarded requests and expose inventory when available.", "Separate configurable DB connection; queued/outbox handoff."],
        ["SafeTrack records", "Source shared household/account identity data.", "Shared DB/data contract; upstream identity remains externally owned."],
        ["EvaTrack", "Submit evacuation/personnel/resource requests.", "POST /api/v1/external/resource-requests with integration-key auth and validation."],
        ["OneSignal", "Register devices and deliver mobile push.", "Native/mobile SDK registration and Laravel REST delivery."],
        ["Open-Meteo / PAGASA", "Weather snapshots and official warning references.", "Backend HTTPS fetch for Open-Meteo; official advisory links for PAGASA."],
        ["Map tiles / OSRM", "Map rendering and route geometry.", "Configured external tile and routing integrations."],
        ["Laravel file storage", "Radio clips and generated file access.", "Configured filesystem/public storage paths."],
    ], [1.45, 2.45, 2.7])
    doc.add_heading("3.1.4 Communications Interfaces", level=3)
    bullets(doc, [
        "Clients shall exchange JSON application data with Laravel over HTTP or HTTPS. Production transfer of credentials or personal/location data shall use HTTPS with valid TLS.",
        "External request intake shall authenticate the sending system, validate its payload, and record request source/reference before operational use.",
        "A physical phone testing a local API shall use a LAN-reachable server address; Laravel must listen on an address reachable from the phone.",
        "Long-running/external work may be asynchronous. Responses shall distinguish accepted/pending work from completed delivery when defined by the endpoint contract.",
        "Polling or refresh-based views shall not be described as guaranteed instantaneous websocket or live-stream delivery.",
    ])

    doc.add_heading("3.2 Functional Requirements", level=2)
    requirements(doc, "3.2.1 Authentication and User Management (AUTH)", [
        ["FR-AUTH-01", "Authenticate a user with a supported unique account identifier and password before protected access.", "Must", "Implemented"],
        ["FR-AUTH-02", "Enforce server-side role access for super_admin, admin, household_resident, and rescuer roles.", "Must", "Implemented"],
        ["FR-AUTH-03", "Issue/revoke API tokens and return user identity and role metadata after successful authentication.", "Must", "Implemented"],
        ["FR-AUTH-04", "Route web/mobile users to the appropriate workspace and deny role-incompatible operations.", "Must", "Implemented"],
        ["FR-AUTH-05", "Allow authorized HQ/Admin to create, update, validate, deactivate, and review responder accounts and team assignments while retaining history.", "Must", "Implemented"],
        ["FR-AUTH-06", "Provide supported account recovery/password reset workflows with validation and protected password changes.", "Should", "Implemented; end-to-end QA pending"],
        ["FR-AUTH-07", "Prevent unrestricted public creation of operational or privileged accounts.", "Must", "Implemented"],
    ])
    requirements(doc, "3.2.2 Household Residents and Monitoring (HH)", [
        ["FR-HH-01", "Allow a household user to complete first-time setup by selecting the exact household map location and saving available address, member, device, and geotag metadata.", "Must", "Implemented"],
        ["FR-HH-02", "Request location permission and capture/update device location when granted and when the workflow is active.", "Must", "Implemented; device QA pending"],
        ["FR-HH-03", "Allow household users to view their household profile, linked members, available device/location information, and overview.", "Must", "Implemented"],
        ["FR-HH-04", "Allow status submission during an active disaster and persist event, source, timestamp, and available coordinates.", "Must", "Implemented"],
        ["FR-HH-05", "Provide the required four choices: Safe, Need Help, Need to Evacuate, and Evacuated.", "Must", "Partial: current options are Safe, Evacuated, Unsafe, Needs help; exact evacuation-intent option differs"],
        ["FR-HH-06", "Allow a resident to edit a saved status while preserving prior report history.", "Must", "Implemented"],
        ["FR-HH-07", "Show household status history with saved/submitted time.", "Must", "Implemented"],
        ["FR-HH-08", "Support individual family-member status reporting where event/member data permits.", "Must", "Implemented"],
        ["FR-HH-09", "Queue unsent reports offline and synchronize on reconnect without duplicate records.", "Must", "Not implemented in source"],
        ["FR-HH-10", "Provide a cached household overview for offline viewing and indicate freshness/offline state.", "Must", "Not implemented in source"],
        ["FR-HH-11", "Support trusted-household requests, accept/reject decisions, and configured PIN-gated member/status access.", "Should", "Implemented; acceptance QA pending"],
        ["FR-HH-12", "Generate/present a household evacuation QR credential for an authorized verification workflow.", "Must", "Implemented; field QA pending"],
        ["FR-HH-13", "On valid QR verification, record the household check-in and associated site/event/time where supplied.", "Must", "Implemented"],
        ["FR-HH-14", "Show nearby evacuation centers on a map and support route display where coordinates/providers are available.", "Must", "Implemented; device/provider QA pending"],
    ])
    requirements(doc, "3.2.3 Disaster Events, Alerts, and Notifications (DIS)", [
        ["FR-DIS-01", "Allow HQ/Admin to create, view, update, and close disaster events with type, affected scope, priority/severity metadata, and lifecycle time.", "Must", "Implemented"],
        ["FR-DIS-02", "Allow HQ/Admin to create event-linked broadcasts, define recipient/area scope, and retain broadcast history.", "Must", "Implemented"],
        ["FR-DIS-03", "Deliver configured disaster messages to registered household/responder devices through OneSignal.", "Must", "Implemented in code; native delivery QA pending"],
        ["FR-DIS-04", "Record device registration and notification state and provide supported notification feeds/read actions.", "Should", "Implemented"],
        ["FR-DIS-05", "Show active disaster information to mobile users and a clear standby state when no event is active.", "Must", "Implemented"],
    ])
    requirements(doc, "3.2.4 Shared Rescue-Team and On-Site Responder Functions (RESP)", [
        ["FR-RESP-01", "Allow HQ/Admin to create responder accounts with personal/contact information and rescue team/cluster affiliation.", "Must", "Implemented via HQ; no public registration"],
        ["FR-RESP-02", "Capture and verify official identification before marking a responder operationally validated.", "Must", "Partial: account/team validation exists; distinct official-ID process not evidenced"],
        ["FR-RESP-03", "Maintain team names/codes and validate responder account/team identifier consistency.", "Must", "Implemented"],
        ["FR-RESP-04", "Allow a responder to view/update permitted profile data under role protection.", "Must", "Implemented"],
        ["FR-RESP-05", "Show assigned incidents in a list and details with target, team, priority, and status.", "Must", "Implemented"],
        ["FR-RESP-06", "Show assignments and evacuation context on a map and support navigation when coordinates/providers exist.", "Must", "Implemented; field QA pending"],
        ["FR-RESP-07", "Allow permitted assignment progress transitions and attribute each update to responder and time.", "Must", "Implemented"],
        ["FR-RESP-08", "Record responder location updates and expose appropriate current location/route to authorized HQ users.", "Must", "Implemented; update cadence QA pending"],
        ["FR-RESP-09", "Allow post-rescue household check-ins with status tracking for household members.", "Must", "Implemented"],
        ["FR-RESP-10", "Accept field reports with status/location/notes, injuries, deaths, property damage, and member condition data.", "Must", "Implemented"],
        ["FR-RESP-11", "Automatically timestamp assignment, location, report, check-in, and radio updates.", "Must", "Implemented"],
        ["FR-RESP-12", "Allow responders to create and track equipment/supply/resource/personnel requests and cancel eligible requests.", "Must", "Implemented"],
        ["FR-RESP-13", "Allow same-team users to record, upload, retrieve, and play radio voice clips with activity logs.", "Must", "Implemented as clips, not continuous live PTT"],
        ["FR-RESP-14", "Expose authorized field updates to HQ for operational monitoring.", "Must", "Implemented; refresh-based, not continuous streaming"],
    ])
    requirements(doc, "3.2.5 Headquarters / Dispatcher Operations (HQ)", [
        ["FR-HQ-01", "Show dashboard summaries for event, household reporting/status, dispatch, requests, weather, map, and recent activity from active data.", "Must", "Implemented"],
        ["FR-HQ-02", "Allow HQ to review household status, geotag, profile, device signals where recorded, and history using operational filters.", "Must", "Implemented"],
        ["FR-HQ-03", "Allow HQ to review/confirm affected-area information while preserving original report attribution.", "Must", "Implemented as review; no manual HQ status overwrite"],
        ["FR-HQ-04", "Allow HQ to create dispatches, identify target/area, select available responders/teams, set priority, and add route/dispatch notes.", "Must", "Implemented"],
        ["FR-HQ-05", "Use unsafe/need-help household counts, location, availability, or configured criteria to support geographic triage.", "Must", "Implemented; operational effectiveness QA pending"],
        ["FR-HQ-06", "Route teams to affected households/areas using coordinates and available route data.", "Must", "Implemented; provider dependent"],
        ["FR-HQ-07", "Support area severity categories Low, Medium, High, and Critical.", "Must", "Partial: dispatch values are Critical, High, Watch, Monitor"],
        ["FR-HQ-08", "Show incoming incident reports and field updates with source, event, and time.", "Must", "Partial: read/refresh exists; continuous realtime not demonstrated"],
        ["FR-HQ-09", "Notify assigned responders through registered push channels where configured and available.", "Must", "Implemented in code; native delivery QA pending"],
        ["FR-HQ-10", "Allow event closure and retain related records for SitRep and archive review.", "Must", "Implemented"],
    ])
    requirements(doc, "3.2.6 Spatial and Mapping Functions (MAP)", [
        ["FR-MAP-01", "Provide household geotags, evacuation sites, responders/teams, assignments, and stored route geometry where available.", "Must", "Implemented"],
        ["FR-MAP-02", "Distinguish status layers and use only locations from the active configured data source.", "Must", "Implemented; bad source joins may limit attribution"],
        ["FR-MAP-03", "Support coordinate-based routes or external navigation for households, assignments, and evacuation centers.", "Must", "Implemented; provider dependent"],
        ["FR-MAP-04", "Show clear empty/unavailable state when coordinates, boundaries, or map/routing providers are absent.", "Should", "Implemented"],
    ])
    requirements(doc, "3.2.7 Resource Request Intake, Validation, and Tracking (REQ)", [
        ["FR-REQ-01", "Receive internal/mobile and authenticated external requests and record source/reference, requester, category, item/type, quantity, urgency, area, and description when supplied.", "Must", "Implemented"],
        ["FR-REQ-02", "Support personnel, equipment/resource, goods/supply, and vehicle request categories as applicable.", "Must", "Implemented; goods/supplies use resource category"],
        ["FR-REQ-03", "Persist each request in the RESQPERATION queue before HQ review and retain validation decisions/notes.", "Must", "Implemented"],
        ["FR-REQ-04", "Allow HQ to verify/approve, return for missing data, reject/cancel where permitted, or forward requests.", "Must", "Implemented"],
        ["FR-REQ-05", "Prevent duplicate external active requests using source system plus source reference.", "Must", "Implemented"],
        ["FR-REQ-06", "Forward verified requests to TrackingAid with tracking reference, source reference, payload, validator/forwarder details, and time.", "Must", "Queued/outbox implemented; external QA pending"],
        ["FR-REQ-07", "Retain request status/audit history through fulfillment or recorded return/cancellation.", "Must", "Implemented; final fulfillment is TrackingAid-owned"],
        ["FR-REQ-08", "Represent Pending, Approved, In Progress, and Completed or provide an explicit approved mapping to internal states.", "Must", "Partial: internal keys need explicit mapping"],
        ["FR-REQ-09", "Show TrackingAid inventory before forwarding when its connection and schema are available.", "Should", "Implemented where available; external dependency"],
        ["FR-REQ-10", "Expose failed/pending cross-database delivery for retry/review and do not claim acceptance before successful handoff.", "Must", "Outbox design present; deployed worker QA pending"],
    ])
    requirements(doc, "3.2.8 Weather and Barangay Context (WX)", [
        ["FR-WX-01", "Allow HQ to view saved weather snapshots and request a Laravel-managed refresh.", "Must", "Implemented"],
        ["FR-WX-02", "Store snapshots for event monitoring, SitRep, and archive context where schema permits.", "Must", "Implemented"],
        ["FR-WX-03", "Identify PAGASA as official warning confirmation; Open-Meteo values alone shall not be represented as official warnings.", "Must", "Implemented"],
        ["FR-WX-04", "Provide configurable barangay/map focus and coordinates without source-code edits for environment changes.", "Should", "Configuration implemented; profile-table limitation documented"],
    ])
    requirements(doc, "3.2.9 Situation Reporting and Incident Archive (REP)", [
        ["FR-REP-01", "Allow HQ to review event-linked household, casualty, evacuation, dispatch, weather, and request summary data.", "Must", "Implemented"],
        ["FR-REP-02", "Generate and save a SitRep snapshot with event and reporting metadata.", "Must", "Implemented"],
        ["FR-REP-03", "Provide authorized printable/downloadable SitRep PDF when renderer and data are available.", "Should", "Route/source present; end-to-end PDF QA pending"],
        ["FR-REP-04", "Provide authorized retrieval of event, household status, dispatch, radio, request, and SitRep archive categories.", "Must", "Implemented"],
        ["FR-REP-05", "Support archive search/filter/pagination and CSV export for supported categories with role protection and row limits.", "Must", "Implemented; large-data QA pending"],
        ["FR-REP-06", "Support manual report generation/export for city-level escalation without implying automatic city-system delivery.", "Must", "Partial: no dedicated city escalation workflow evidenced"],
        ["FR-REP-07", "Retain event records after closure for authorized documentation and review.", "Must", "Implemented"],
    ])
    requirements(doc, "3.2.10 Notifications, Profile, and Administration (ADM)", [
        ["FR-ADM-01", "Allow HQ users to view supported notification feeds and update read/saved states.", "Should", "Implemented"],
        ["FR-ADM-02", "Allow authenticated users to view/update permitted profile data and change password through protected workflows.", "Should", "Implemented"],
        ["FR-ADM-03", "Allow Super Admin to review incoming inquiries where the feature/route is enabled.", "Should", "Implemented"],
        ["FR-ADM-04", "Record audit information for consequential operational, account, and request changes where schema permits.", "Must", "Implemented; full audit coverage QA pending"],
        ["FR-ADM-05", "Provide liveness/readiness diagnostics without exposing secrets or sensitive records.", "Should", "Implemented"],
    ])

    doc.add_heading("3.3 Non-Functional Requirements", level=2)
    for heading, rows in [
        ("3.3.1 Performance", [
            ["NFR-PER-01", "Dashboard/list endpoints shall use bounded or aggregate reads and avoid unbounded operational payloads.", "Must", "Partial; audits identify remaining work"],
            ["NFR-PER-02", "Paginated endpoints shall validate and cap requested page size.", "Must", "Implemented for audited inputs; wider coverage pending"],
            ["NFR-PER-03", "Long-running/external tasks shall use asynchronous work where configured and expose pending/failure status.", "Must", "Implemented; worker/scheduler deployment QA pending"],
            ["NFR-PER-04", "Performance claims shall use representative data and repeatable measurements; no production latency target is claimed without evidence.", "Must", "Representative deployment test not done"],
        ]),
        ("3.3.2 Security", [
            ["NFR-SEC-01", "Passwords shall be one-way hashed and excluded from responses and logs.", "Must", "Authentication code implements; operational review pending"],
            ["NFR-SEC-02", "Protected operations shall enforce authentication and authorization on the server.", "Must", "Sanctum and role middleware implemented"],
            ["NFR-SEC-03", "Write endpoints shall validate values, ownership, transitions, and allowed enumerations before persistence.", "Must", "Many workflows implement; full route matrix QA pending"],
            ["NFR-SEC-04", "Use parameter binding/ORM/query-builder APIs; do not concatenate untrusted SQL.", "Must", "Project rule; full security audit not claimed"],
            ["NFR-SEC-05", "Keep DB/integration secrets in protected environment configuration, not public client bundles.", "Must", "Pattern present; repository-history secret review remains"],
            ["NFR-SEC-06", "Disclose household identity, GPS, contact, and responder data only to roles with an operational need.", "Must", "Role boundaries present; privacy review pending"],
            ["NFR-SEC-07", "Production transfer of credentials or personal/location data shall use HTTPS/TLS.", "Must", "Production TLS not verified"],
        ]),
        ("3.3.3 Reliability and Availability", [
            ["NFR-REL-01", "Return structured JSON for validation/auth/database/integration failures and hide stack traces in production.", "Must", "Partly implemented; production config review needed"],
            ["NFR-REL-02", "Related writes on one database connection shall roll back together on failure.", "Must", "Several workflows tested; full write audit pending"],
            ["NFR-REL-03", "External/cross-DB delivery shall be retryable or expose pending/failure and shall not be claimed atomic with primary DB.", "Must", "Outbox pattern present; deployment QA pending"],
            ["NFR-REL-04", "Deployment shall define backup, retention, restoration, workers, scheduler, and recovery procedures.", "Must", "Restore/operations exercise not verified"],
            ["NFR-REL-05", "Show unavailable/stale data and do not substitute fabricated records for live operational data.", "Must", "Rule implemented; client failure QA pending"],
        ]),
        ("3.3.4 Usability", [
            ["NFR-USA-01", "Use role-appropriate labels, concise errors, clear loading/empty states, and confirmation for consequential actions.", "Must", "Source present; user acceptance pending"],
            ["NFR-USA-02", "Mobile workflows shall provide save/failure/pending feedback on supported screens and phone sizes.", "Must", "Device usability QA pending"],
            ["NFR-USA-03", "Map/status meaning shall include text or legend and not rely on color alone.", "Should", "Implemented in key screens; accessibility audit pending"],
        ]),
        ("3.3.5 Maintainability and Testability", [
            ["NFR-MNT-01", "Separate route/controller, validation, workflow, query, and response responsibilities enough to test each boundary.", "Must", "Partial; current architecture audit records gaps"],
            ["NFR-MNT-02", "Review and test shared schema changes against the intended active DB; use reversible/additive changes where possible.", "Must", "Policy documented; approval required"],
            ["NFR-MNT-03", "Automated tests shall cover auth/roles, household status, dispatch, requests, evacuation, reports, and integration failure contracts.", "Must", "Partial; current suite has 1 failing test"],
            ["NFR-MNT-04", "Run backend tests, web build/lint, and mobile lint/type checks for release and record unavailable checks.", "Must", "Current evidence in Appendix B"],
        ]),
        ("3.3.6 Portability", [
            ["NFR-POR-01", "DB/API/barangay/provider values shall be environment-configurable, not hardcoded for one deployment.", "Must", "Configuration patterns present; deployment review pending"],
            ["NFR-POR-02", "Physical mobile testing shall use a LAN-reachable API host, not phone localhost.", "Must", "Documented and supported"],
            ["NFR-POR-03", "Document backend, frontend, queue, scheduler, storage, DB, and native-build prerequisites for deployment.", "Should", "Partial; production runbook remains"],
        ]),
        ("3.3.7 Data Privacy and Compliance", [
            ["NFR-PRV-01", "Collect/expose only data necessary for disaster coordination, safety reporting, response, and defined integrations.", "Must", "Formal privacy impact assessment pending"],
            ["NFR-PRV-02", "Define purpose and role access for GPS, device, family-member, contact, and responder information.", "Must", "Role controls present; consent/PIA review pending"],
            ["NFR-PRV-03", "Protect authorized exports and preserve appropriate audit attribution for personal data.", "Must", "Authorization present; export audit QA pending"],
            ["NFR-PRV-04", "Review retention, correction, access, breach response, and data-subject handling under RA 10173 before production.", "Must", "Governance procedure not evidenced complete"],
        ]),
    ]:
        doc.add_heading(heading, level=3)
        table(doc, ["Req. ID", "Requirement Description", "Priority", "Current Status"], rows, [.82, 4.0, .72, 1.25])

    doc.add_heading("3.4 Database Requirements", level=2)
    doc.add_paragraph(
        "Primary application data uses Laravel's configured MySQL connection and the existing approved schema. A separate TrackingAid connection handles external handoff and inventory reads. Automated tests may use isolated SQLite in-memory. The logical entities below describe data responsibilities; they do not authorize destructive schema replacement or imply RESQPERATION exclusively owns every shared table."
    )
    table(doc, ["Logical Entity / Store", "Description and Relationships"], [
        ["users, roles, personal_access_tokens", "Identity, role, account state, API tokens; users may link to household or responder profiles."],
        ["households, household addresses, household_members", "Household identity/profile, address/barangay/purok, members, and account links."],
        ["geotagged_locations, device_tokens, device_tracking_logs", "Household/device coordinates, platform, push registration, location, permission, and last-seen data where present."],
        ["disaster_events, disaster types, disaster_broadcasts", "Event lifecycle, scope, alert records, recipient metadata, and links to status/dispatch/weather/reports."],
        ["household_statuses, household_disasters, household_status_logs", "Status lookup, latest household/event state, and attributed report history with time, source, notes, coordinates."],
        ["member_statuses, member_disaster_statuses", "Per-member disaster status, previous/current status, location, and rescue indicators where supported."],
        ["rescue_teams, responders", "Team/cluster definitions and responder profile, account relation, availability, validation, and contact details."],
        ["responder_assignments, responder_routes, route_coordinates, responder_location_logs", "Dispatch target, status lifecycle, team assignment, route geometry, and responder location history."],
        ["responder_field_reports, evacuation check-ins", "Field observations, injuries/deaths/damage, notes/member conditions, QR verification and center check-in."],
        ["evacuation_centers", "Evacuation-site identity, location/reference information, routes, and check-ins."],
        ["resource_requests, request_validations, resource_request_status", "Source/reference/category, quantity/urgency, request lifecycle, HQ decisions, duplicate notes, fulfillment/handoff."],
        ["TrackingAid handoff/outbox", "Queued/retryable external delivery and forwarded request details in the separate integration DB."],
        ["weather_logs", "Time-stamped weather snapshots and optional event links for workspace, SitRep, and archive."],
        ["situation_reports, incident_archives", "Generated report snapshots and archived operational records."],
        ["responder_communication_logs", "Team transmission/voice-clip metadata, file references, and timestamps."],
        ["notifications, notification_recipients, notification_logs", "Device/user notification state, recipients, delivery metadata, and read/feed actions where present."],
        ["trusted-household connection/PIN data", "Connection requests, accept/reject decisions, and PIN-gated access support."],
        ["audit_logs, inquiries", "Operational/account change audit records and enabled inquiry records."],
    ], [2.15, 4.45])
    bullets(doc, [
        "Foreign keys, unique IDs, indexes, soft deletion, and column names shall follow the approved active schema; shared schemas may contain legacy names or additive compatibility fields.",
        "Related writes on one connection shall use transactions where required. Cross-database delivery shall use an outbox/queue or equivalent retryable handoff.",
        "Status history shall preserve report source and submitter; HQ review shall not erase provenance.",
        "Unavailable required schema shall produce an explicit empty/error response and shall not silently generate records.",
        "The deployment owner shall define DB backup, restore, retention, and least-privilege access; shared DB changes require approval.",
    ])

    doc.add_heading("3.5 System Flow", level=2)
    doc.add_heading("3.5.1 Authentication and Role Routing", level=3)
    doc.add_paragraph(
        "A user submits the supported identifier and password to POST /api/v1/auth/login. Laravel validates the request, resolves the account from active user/responder/household-linked records, checks the password hash and account state, determines the role, and issues a Sanctum token. Clients store the token in platform-appropriate protected storage and send it on later API calls. Administrative roles enter HQ/Admin web; household_resident and rescuer roles enter their mobile workflows. Authentication, authorization, validation, and DB errors return structured JSON."
    )
    doc.add_heading("3.5.2 HQ Disaster-to-Response Flow", level=3)
    doc.add_paragraph(
        "HQ/Admin loads dashboard summaries from the active application database. With no active event, the system shows standby monitoring. An authorized user creates/updates an event and broadcast. Laravel persists event/broadcast data and queues or submits configured push delivery. Household residents and rescuers submit attributed, timestamped status/location/report updates. HQ reviews status, maps, weather, field reports, and requests; creates assignments for affected areas; selects teams/responders; and monitors progress through authenticated operational views."
    )
    doc.add_heading("3.5.3 Household Mobile Flow", level=3)
    doc.add_paragraph(
        "The resident logs in and loads the household overview. On first use, the app requests location permission, lets the user pin the household on a map, captures available address/member/device details, and posts setup data to Laravel. During an active event, the resident selects and saves a status, can edit it, and reviews status history. Member-level status, evacuation QR, route/map, and trusted-household/PIN features are available where configured. Current status synchronization requires reachable API access; offline queue and cached overview are not implemented."
    )
    doc.add_heading("3.5.4 Responder Field Flow", level=3)
    doc.add_paragraph(
        "The rescuer logs in, loads profile/assignments, opens an incident, accepts or updates progress, views its route/map, and submits available location updates. At the scene, the rescuer conducts household/member check-ins and submits structured reports containing status, notes, injuries, deaths, property damage, and member condition. The rescuer may submit/cancel a resource request and use team radio clips. HQ reads field updates through protected endpoints and dashboard/map workflows. Radio is a record-stop-upload clip/feed, not continuous live radio."
    )
    doc.add_heading("3.5.5 Evacuation Verification Flow", level=3)
    doc.add_paragraph(
        "The household app presents an evacuation QR credential. Authorized personnel verify it against household/event information and record a check-in for the selected evacuation center. The result is persisted for monitoring/reporting. Invalid, expired, mismatched, or unavailable credentials shall not be marked verified."
    )
    doc.add_heading("3.5.6 Resource Request Flow", level=3)
    doc.add_paragraph(
        "A request may originate from EvaTrack, a rescuer, HQ, or another configured source. External intake authenticates the integration key, validates the payload, and uses source plus source reference to prevent duplicates. RESQPERATION stores it for HQ validation. HQ verifies, returns, cancels/rejects where allowed, or forwards it with decision notes. Forwarding creates a tracked outbox/handoff item for TrackingAid. Retry/worker processing reports pending/failure/success. TrackingAid owns physical inventory release and fulfillment; RESQPERATION does not claim delivery itself."
    )
    doc.add_heading("3.5.7 Weather, SitRep, and Archive Flow", level=3)
    doc.add_paragraph(
        "Laravel obtains Open-Meteo snapshots on request or schedule and stores them for dashboard, event, SitRep, and archive context. HQ confirms official warnings through PAGASA before broadcast. HQ selects an event, reviews available household, casualty, evacuation, dispatch, weather, and request summaries, and generates a stored SitRep. Authorized users retrieve historical event/status/dispatch/radio/request/report records and export supported archive data. City escalation is manual report generation/export unless a separate city integration is defined."
    )
    doc.add_heading("3.6 Verification and Acceptance", level=2)
    doc.add_paragraph(
        "Acceptance requires demonstrating the intended role workflow with representative data, correct access boundaries, validation/error behavior, and persisted result. Feature tests and client builds do not prove mobile usability, external service availability, production TLS, shared DB correctness, deployment performance, or operational readiness. Appendix C lists the end-to-end acceptance checks; unverified items remain open even when a route or screen exists."
    )

    # Appendices
    doc.add_heading("Appendix A. End-to-End System Flow Summary", level=1)
    numbered(doc, [
        "User -> React web or Expo mobile -> POST /api/v1/auth/login -> Laravel validation/account lookup -> active configured DB -> Sanctum token and role -> authorized workspace.",
        "HQ/Admin -> create event and broadcast -> Laravel stores records -> OneSignal delivery job -> registered devices -> household/responder status reports -> status/audit history.",
        "Household -> map pin/GPS and profile setup -> household/member/geotag/device records -> active-event status -> history and HQ dashboard/map.",
        "HQ -> review affected household/area and team availability -> create dispatch/route -> rescuer assignment -> progress/location/check-in/field report -> HQ monitoring and SitRep.",
        "EvaTrack/rescuer/HQ -> request intake -> duplicate check and storage -> HQ validation -> queued TrackingAid handoff -> external fulfillment/status -> request history/archive.",
        "Laravel scheduled/manual refresh -> Open-Meteo -> weather_logs -> dashboard/SitRep/archive; PAGASA confirmation remains an HQ decision.",
        "Household QR -> authorized verification -> evacuation-center check-in -> database status/history -> HQ dashboard/SitRep/archive.",
        "Event closure -> retain event, broadcast, household reports, dispatch, requests, radio, weather, and SitRep -> authorized archive and supported export.",
    ])

    doc.add_heading("Appendix B. Implementation Status and Verification", level=1)
    doc.add_paragraph(
        "Implemented means the corresponding source/routes/UI were found, not that production acceptance is complete. Partial means an explicit requirement detail, taxonomy, external dependency, deployment step, or end-to-end verification remains. Not implemented means the feature was not evidenced. External means delivery/fulfillment is owned by another system or provider."
    )
    table(doc, ["Area", "Status", "Evidence / Remaining Work"], [
        ["HQ/Admin modules", "Implemented in source", "Dashboard, broadcasts, weather, mapping, household status, dispatch, responder accounts, requests, SitRep, archive, notifications, profile, and enabled inquiries have pages/API paths."],
        ["Household mobile", "Implemented with gaps", "Setup, GPS/geotag, family views, status/edit/history, QR, evacuation map, trusted-household/PIN flows exist. Offline queue/cache absent; status taxonomy mismatch remains."],
        ["Responder mobile", "Implemented with limitations", "Assignments/status/location/map, reports/check-ins, requests, radio clips, profile, and push registration exist. Field/native QA remains; clips are not live streaming."],
        ["Official responder ID", "Partial", "HQ account/team validation exists; distinct official-ID capture and verification was not evidenced."],
        ["Severity classes", "Partial", "Current dispatch values Critical, High, Watch, Monitor differ from requested Low, Medium, High, Critical."],
        ["Real-time monitoring", "Partial", "Protected read/refresh and notification paths exist; continuous websocket/stream delivery not established."],
        ["Request state labels", "Partial", "Internal keys: needs_validation, verified, forwarded, returned, fulfilled, cancelled; explicit mapping to Pending/Approved/In Progress/Completed requires signoff."],
        ["City escalation", "Partial", "SitRep/report export exists; dedicated city escalation workflow not evidenced."],
        ["Offline operation", "Not implemented", "No mobile household status queue or persisted offline overview found in app source."],
        ["Push notifications", "Code implemented; device QA pending", "OneSignal code exists; real supported build, credentials, permission, and delivery must be verified."],
        ["TrackingAid fulfillment", "External/asynchronous", "Handoff/outbox exists; DB access, worker operation, and downstream fulfillment are external/deployment dependent."],
        ["Database", "Configurable; deployment dependent", "Primary and TrackingAid connections exist; environment selects active DB. Shared writes/migrations require approval."],
    ], [1.35, 1.4, 3.85])
    doc.add_heading("B.1 Verification Run on October 6, 2026", level=2)
    table(doc, ["Check", "Result", "Notes"], [
        ["Laravel: php artisan test --compact", "Failed: 110 passed / 111 tests; 482 assertions", "One failure: SelectDispatchRespondersTest SQLite schema lacks household_disasters."],
        ["Web: npm run build", "Passed", "Production build completed; export-helper bundle produced a chunk-size warning."],
        ["Mobile: npm run lint", "Completed with warnings", "0 errors; 3 unused-variable/import warnings in household screens."],
        ["Mobile TypeScript check", "Not run", "Project-local TypeScript compiler is not installed."],
        ["Device/external/deployment tests", "Not verified", "No physical-phone acceptance, OneSignal delivery, TrackingAid fulfillment, production TLS, load test, or restore exercise was run for this document."],
    ], [2.0, 1.55, 3.05])

    doc.add_heading("Appendix C. Acceptance Criteria", level=1)
    numbered(doc, [
        "Each role can authenticate, receive role metadata, and is denied endpoints outside its authorization boundary.",
        "Household setup persists the correct geotag/profile/member/device data; resident can view profile and status history.",
        "During an active event, residents submit/edit all approved statuses with source, event, time, and available coordinates; final four labels match the approved requirement.",
        "Offline acceptance requires queued writes and a cached overview that sync without duplicate reports and display freshness/offline state.",
        "Household QR can be verified by authorized personnel and creates the correct event/site check-in; invalid data is rejected.",
        "HQ creates an event/broadcast, supported test devices receive alerts, and event/broadcast/delivery outcomes can be audited.",
        "HQ maps show active-data household, evacuation, responder, and route layers, with clear empty/unavailable states.",
        "HQ dispatches by area/household triage; assigned rescuer updates progress/location and submits check-in/report; HQ sees source/time.",
        "Responder registration captures personal information, cluster/team, and an approved official-ID verification result before activation.",
        "Two same-team devices can record, upload, refresh, and play radio clips; live WebRTC is outside current implementation.",
        "Duplicate external request references do not duplicate active requests; HQ validates/forwards and the system shows the true TrackingAid handoff result.",
        "Request status UI explicitly maps Pending, Approved, In Progress, Completed or has approved equivalent labels.",
        "HQ generates and retrieves a SitRep and manual city-escalation report; authorized archive retrieval/export preserves role protection.",
        "Backend tests, web build/lint, and mobile lint/type checks pass or remaining failures are formally accepted; current known defects are resolved.",
        "Production setup defines HTTPS, least-privilege DB credentials, OneSignal and TrackingAid configuration, worker/scheduler, backup/restore, and privacy procedures.",
    ])

    doc.add_heading("Appendix D. Source Evidence", level=1)
    bullets(doc, [
        "System root README: resqperation-system/README.md.",
        "API roles/routes: resqperation-system/backend-laravel/routes/api.php.",
        "Backend status/audits: backend-laravel/BACKEND_REQUIREMENTS_STATUS.md and A1_A3_ARCHITECTURE_AUDIT.md.",
        "Frontend source: frontend-web/src/pages/ and frontend-mobile/app/, components/, api/, and utils/.",
        "System diagrams: docs/diagrams/01_system_context_and_external_integrations.md, 02_roles_use_cases_and_auth.md, 05_mobile_workflows_household_rescuer_radio.md, 18_system_architecture.md, and 20_data_flow_diagram.md.",
        "Current and integration docs: docs/RESQPERATION_SYSTEM_CLEANUP_AND_CURRENT_STATE.md, RESQPERATION_TRACKINGAID_REQUEST_INTEGRATION_GUIDE.md, and RESQPERATION_RESCUER_RADIO_COMMUNICATION.md.",
        "Supplementary local references: FOR DEV/API_REFERENCE.md, GEOTAGGING_DISPATCH_ROUTING.md, and PUSH_NOTIFICATIONS.md.",
    ])

    update = OxmlElement("w:updateFields")
    update.set(qn("w:val"), "true")
    doc.settings._element.append(update)
    doc.core_properties.title = "RESQPERATION Software Requirements Specification"
    doc.core_properties.subject = "A Geo-Tagged Household Monitoring and BDRRM Rescue Coordination System"
    doc.core_properties.author = ""
    doc.core_properties.keywords = "RESQPERATION, SRS, disaster response, household geotagging, BDRRM"
    doc.save(OUTPUT)
    print(f"Generated: {OUTPUT}")
    print(f"Main-branch revision rows: {len(history)}")
    print(f"Document tables: {len(doc.tables)}")


if __name__ == "__main__":
    build()