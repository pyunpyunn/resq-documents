# RESQPERATION · Diagram Design System

One style for all seven diagram templates: **light mode, white canvas, dark-blue structure, clean rounded shapes.**
Templates contain only the main data and correct labels. Everything else (legend, shape meaning, connector meaning, styling) lives here.

Files:

| # | File | Diagram |
|---|------|---------|
| 01 | `01_ERD_Template.svg` | Entity Relationship Diagram |
| 02 | `02_Use_Case_Template.svg` | Use Case Diagram |
| 03 | `03_Flow_Chart_Template.svg` | Flow Chart |
| 04 | `04_Swim_Lane_Template.svg` | Swim Lane Diagram |
| 05 | `05_Data_Flow_Diagram_Template.svg` | Data Flow Diagram (Level 1) |
| 06 | `06_System_Architecture_Template.svg` | System Architecture |
| 07 | `07_Tech_Stack_Template.svg` | Tech Stack |

---

## 1. Design principles

1. **Light mode only.** Canvas is white. Dark blue is used for structure (headers, primary nodes, lines), never for the whole background.
2. **Blue family only.** No warm colors. The old strawberry / terracotta / rose / brown / cream theme is retired.
3. **Minimal text in the diagram.** Title + node labels + connector labels only. No paragraphs, legends, notes or "how to use" panels on the canvas.
4. **Same tokens everywhere.** Radius, border width, line weight, font and spacing never change between diagrams.
5. **Color means the same thing in every diagram** (see section 2.2).

---

## 2. Color

### 2.1 Tokens

| Token | Hex | Use |
|-------|-----|-----|
| `ink` | `#0F1E3D` | All body text on light surfaces |
| `navy` | `#12306B` | Darkest color. Titles, HQ Web, primary lines, ERD relationship lines, terminators |
| `blue` | `#2563EB` | Household Mobile, accents, title underline, DB read/write arrows |
| `cyan` | `#0E7490` | Rescuer Mobile, operations tables, I/O shapes |
| `slate` | `#475569` | Shared services, external systems, secondary lines, integration connectors |
| `navy-tint` | `#E6ECF8` | Light fill for navy items (data stores, MySQL, database shapes) |
| `blue-tint` | `#DBE8FE` | Light fill for blue items (decisions, Household use cases) |
| `cyan-tint` | `#D5F0F6` | Light fill for cyan items (Rescuer use cases, input/output) |
| `slate-tint` | `#E8EDF3` | Light fill for slate items |
| `mist` | `#F5F8FD` | Alternate rows, lane backgrounds, panel backgrounds |
| `white` | `#FFFFFF` | Canvas, card fill, text on dark fills |
| `border` | `#CBD5E1` | Default neutral border, label-chip border |
| `border-strong` | `#94A3B8` | Emphasis neutral border (use sparingly) |
| `muted` | `#64748B` | Secondary text (data types, sub-labels, column headings) |

Contrast rules: white text on `navy`, `blue`, `cyan`, `slate`. `ink` text on white, `mist` and all `-tint` fills.

### 2.2 System color mapping (fixed)

| System / role | Color | Light fill |
|---------------|-------|------------|
| HQ Web (Operations Web App, HQ / Admin staff) | `navy` | `navy-tint` |
| Household Mobile (Household Resident) | `blue` | `blue-tint` |
| Rescuer Mobile (Rescuer) | `cyan` | `cyan-tint` |
| Shared services, external services, integrations | `slate` | `slate-tint` |
| Mobile App / Mobile API client (serves both mobile roles) | split `blue` / `cyan` (left / right half) | n/a |
| Database | `navy` outline on `navy-tint` | n/a |

### 2.3 Not allowed

Terracotta, rose, brown, cream, beige, red, orange, green, purple. No gradients, shadows or glows. No dark-mode canvas.

---

## 3. Typography

Font: **Inter** (fallback: Segoe UI, Arial). Install Inter before importing the SVGs, or Figma will substitute a default font.

| Role | Size | Weight | Color |
|------|------|--------|-------|
| Diagram title | 30 | SemiBold (600) | `navy` |
| Container / group label | 11 | SemiBold, UPPERCASE | system color |
| Table / header name | 14 | SemiBold | white (on header) |
| Node label | 13 | SemiBold | `ink` (or white on dark fill) |
| Node sub-label | 10 | Regular | same as node text |
| ERD field name | 12 | Regular (PK: SemiBold) | `ink` |
| ERD data type | 11 | Regular | `muted` |
| Connector label chip | 10-11 | SemiBold | `slate` |
| Column heading | 11 | SemiBold, UPPERCASE | `muted` |

Naming style: nodes and processes in **Title Case**; use cases **verb-first** ("Update Household Status"); tables **snake_case plural** ("household_members"); decisions end with **?**; keep labels to 1-4 words.

---

## 4. Radius, borders, lines

### 4.1 Corner radius

| Element | Radius |
|---------|--------|
| System boundary, group container, lane frame, tech-stack row | 16 |
| ERD table card, DFD process | 12-14 |
| Process / node box, external-entity box, chip, subprocess | 8-10 |
| Label chip (connector label) | 6 |
| Terminator (Start / End) | pill (height / 2) |
| FK / PK badge | pill |

### 4.2 Border width

| Element | Width | Color |
|---------|-------|-------|
| Container / boundary / lane frame | 1.5 | system color (or `border` when neutral) |
| Node / table / card outline | 1.5 | system color |
| Emphasis (DFD process, outer swim lane frame) | 1.75 - 2 | `navy` |
| Label chip | 1 | `border` |
| Divider line | 1.5 - 2 | `border` or `navy` |

### 4.3 Connector weight

All connectors: **1.75 px**, round caps, round joins. Associations in the use case diagram: 1.25 px at 55% opacity.

---

## 5. Canvas and grid

- Canvas fill `#FFFFFF`. Outer margin 60 px. Base grid 8 px; gaps between nodes in multiples of 8.
- Title block: title text at (60, 72) plus a 64 x 5 `blue` underline (radius 2.5) at (60, 88).
- Content starts at y = 140.
- Keep connectors orthogonal (horizontal / vertical, 90-degree bends). Diagonals only for use case associations and include / extend links.

| Diagram | Canvas |
|---------|--------|
| ERD | 2260 x 1460 |
| Use Case | 2730 x 1344 |
| Flow Chart | 1500 x 1700 |
| Swim Lane | 2650 x 950 |
| DFD | 2200 x 1420 |
| System Architecture | 1780 x 1500 |
| Tech Stack | 2260 x 830 |

Duplicate a frame and extend the height or width when a diagram grows. Do not shrink the margins.

---

## 6. Connectors and arrowheads

| Connector | Line | Arrowhead | Used for |
|-----------|------|-----------|----------|
| Primary flow | `navy`, solid | Filled triangle, 10 px | Flow chart, swim lane, DFD flows, architecture calls |
| Database read / write | `blue`, solid | Filled triangle | Architecture: service group to database; DFD: process to data store (one arrow each way) |
| Integration | `slate`, dashed (7 5) | Filled triangle | Architecture: service to service, service to external |
| Include / Extend | `slate`, dashed (5 4) | Filled triangle | Use case. Include points to the included case. Extend points back to the base case. |
| Association | system color, solid, 55% opacity | none | Use case: actor to use case |
| ERD relationship | `navy`, solid | Crow's foot / one bar (see 7.1) | ERD |
| Branch point | `navy` dot, r = 4 | none | Where one client line splits into several |

Label rules: connector labels sit in a **label chip** (white fill, 1 px `border`, radius 6, 10-11 px SemiBold `slate`) centered on the line. Flow chart branches use **Yes / No**. DFD flows are **nouns** ("status update", not "updates status"). Architecture labels are one word ("push", "SMS", "R / W", "REST / JSON").

Routing: leave the source from the side that faces the target, bend once or twice, enter the target on the opposite face. When several lines share a gap, offset each vertical segment by 24-30 px so they do not overlap. Crossings are allowed at 90 degrees only.

---

## 7. Shape library and per-diagram spec

### 7.1 ERD

Shapes: **Table card** (300 wide, header 44, row 28, radius 12, 1.5 outline in domain color) with a filled header, white body and alternating `mist` rows. **PK / FK badge** (28 x 16 pill). Relationship line with cardinality symbols.

Domain color (header fill):

| Domain | Color |
|--------|-------|
| Identity / accounts | `navy` |
| Household and geography | `blue` |
| Operations / rescue | `cyan` |
| Comms and reports | `slate` |

Row content: `[badge] field_name ........ type` or `→ referenced_table` for FKs.
Badges: PK = filled domain color, white text; FK = `blue-tint` fill, `navy` text.
Cardinality at line ends: **one** = single perpendicular bar; **many** = crow's foot (3 prongs, 14 px). Parent end = one, child end = many. Lines leave from the PK / FK row or the card edge.
Layout: 5 columns x 4 rows. Column pitch 440, row pitch 340. Relationship lines run in the gutters between cards.
Required: every table has a PK; every FK shows `→ table`.

### 7.2 Use Case

Shapes: **System boundary** (rounded rect, white fill, 1.5 outline, 48 px colored header with system name), **Actor** (stick figure, system color, label below), **Use case** (ellipse 250 x 52, `-tint` fill, 1.5 outline; sub use case = white fill), **Include / Extend arrow** with `«include»` / `«extend»` chip.
One boundary per system: Household Mobile (`blue`), Rescuer Mobile (`cyan`), HQ Web (`navy`). Actors stay outside the boundary on the left. Primary use cases in the left column; sub use cases in the right column on the same row as their parent.
Required: actor-to-use-case associations; include / extend arrows for every sub use case; each use case starts with a verb.

### 7.3 Flow Chart

| Shape | Size | Fill / outline | Meaning |
|-------|------|----------------|---------|
| Terminator | 180 x 52, pill | `navy` fill, white text | Start / End |
| Process | 250 x 60, radius 8 | white, `navy` outline | An action or step |
| Decision | 270 x 130 diamond | `blue-tint`, `blue` outline | Yes / No question |
| Input / Output | 270 x 64 parallelogram | `cyan-tint`, `cyan` outline | Data entered or produced |
| Subprocess | 270 x 60, double side bars | white, `navy` outline | A predefined routine |
| Database | 230 x 80 cylinder | `navy-tint`, `navy` outline | Stored data |

Flow top to bottom on a center axis; decisions branch left (No / exit) or right (retry loop). Every decision has two labeled exits. Exactly one Start; at least one End. Loops return with an arrow into the earlier step.

### 7.4 Swim Lane

Shapes: **Lane** (150 tall; header block 150 wide in system color, body white / `mist` alternating, outer frame 2 px `navy`, radius 12), plus the flow chart shapes (terminator 110 x 44, process 130 x 60, decision 140 x 92).
Lane order and color: Household Mobile (`blue`), Rescuer Mobile (`cyan`), HQ Web (`navy`), Laravel API (`slate`), External (white header, `slate` text). Node outline takes the lane color.
Time runs left to right in columns of 170 px; one step per column. Connectors cross lanes as elbow lines in the gap between columns. Decision "No" paths return through a free channel at the bottom of a lane.
Required: every step sits in exactly one lane; lane names are system names, not people.

### 7.5 Data Flow Diagram (Gane-Sarson)

| Shape | Size | Style | Meaning |
|-------|------|-------|---------|
| External entity | 200 x 90, radius 8 | Solid system color, white text | Person or outside system |
| Process | 320 x 120, radius 14 | White, `navy` 1.75 outline, `navy-tint` header band with ID `1.0`, `2.0` ... | Transforms data |
| Data store | 280 x 56 | Open right end, ID box `D1`, `D2` ... on the left | Stored data |
| Data flow | 1.75 px arrow with noun label chip | `navy` | Data moving |
| Store access | `blue` arrow pair | one arrow in, one arrow out | Write / read |

Left column: people (Household `blue`, Rescuer `cyan`, HQ Staff `navy`). Center: processes. Right: one data store aligned to each process. Far right: outside systems (`slate`). Rules: no entity-to-entity flows; no entity-to-store flows; every process has at least one input and one output; every flow has a label.

### 7.6 System Architecture

Columns, left to right: **Users, Apps, API Clients, Laravel API, Data and External.**

| Shape | Style | Meaning |
|-------|-------|---------|
| Node | 240 x 56, radius 10, solid system color, white text | A component |
| Split node | half `blue`, half `cyan` | Mobile App / Mobile API Client (serves both roles) |
| Group container | 16 radius, 1.5 outline in group color, light tint fill, UPPERCASE label | HQ Operations / Mobile Field Work / Shared Services |
| Database | 300 wide, `navy-tint` fill, `navy` outline | MySQL |
| External | white fill, `slate` outline | Outside service |

Connectors: `navy` solid = request calls from clients to services; `blue` solid = group reads / writes the database; `slate` dashed = integration (service to service, service to external). The API groups follow the backend layers: Services/Web, Services/Mobile, Services/Shared.
Inside-API request flow for reference (not drawn): Route, Middleware (RBAC), Controller, Request, Service, Workflow / Action or Query / Repository, Model, Presenter / Resource.

### 7.7 Tech Stack

Shapes: **Layer row** (96 tall, radius 16, `mist` fill, colored label block 150 wide) and **Tech chip** (40 tall, radius 10, white fill, 1.5 outline, 14 px SemiBold).
Rows top to bottom: Web Client (`navy`) beside Mobile Client (split `blue` / `cyan`), Backend API, Database, Integrations, Tooling (all `slate`). Down arrows: clients to Backend, Backend to Database. Integrations and Tooling have no arrows.
One chip per technology, named exactly as the official product (React, Laravel Sanctum, MySQL). No versions or descriptions in the chip.

---

## 8. Legend (kept out of the templates)

**Color**

| Color | Meaning |
|-------|---------|
| `navy` | HQ Web, identity, primary lines |
| `blue` | Household Mobile, household / geo data, database access |
| `cyan` | Rescuer Mobile, operations data |
| `slate` | Shared services, external systems, integrations |
| Blue / cyan split | Mobile app serving both mobile roles |

**Line**

| Line | Meaning |
|------|---------|
| Solid `navy` + arrow | Calls / data flow / control flow |
| Solid `blue` + arrow | Database read / write |
| Dashed `slate` + arrow | Integration, include / extend |
| Thin system-color line, no arrow | Actor association |
| Crow's foot / bar | ERD many / one |

---

## 9. Figma setup

**Import:** drag the `.svg` onto a Figma page (or open the file as text, copy, paste with Ctrl / Cmd + V). Each diagram becomes one frame. Text stays editable; groups arrive with names such as `Tables`, `Connectors`, `Nodes`.

**One-time set-up**
1. Install Inter (Google Fonts) so text renders correctly.
2. Create **color styles / variables** from section 2.1 (`ink`, `navy`, `blue`, `cyan`, `slate`, the four tints, `mist`, `border`, `muted`).
3. Create **text styles** from section 3.
4. Create **radius** and **stroke** tokens from section 4.

**Tools to use**

| Task | Figma tool |
|------|-----------|
| Boxes, containers, chips | Rectangle (R) with corner radius from section 4.1 |
| Use case ovals, branch dots | Ellipse (O) |
| Decision diamond, parallelogram, cylinder | Rectangle rotated 45 degrees, Pen (P) for custom paths, Boolean ops for the cylinder |
| Connectors | Line (L) or Pen with **Arrow end** set to Triangle; stroke 1.75; or FigJam connectors set to **Elbow** |
| Labels | Text (T) with the matching text style |
| Repeated nodes (table card, use case, process, chip) | Components (Ctrl / Cmd + Alt + K); build once, instance everywhere |
| Rows inside a table, chips inside a tech row | Auto Layout (Shift + A) |
| Grouping | Frames for containers; Group (Ctrl / Cmd + G) for connectors |

**Layer naming:** one frame per diagram named `ResQ / <Diagram>`; inside use groups named `Title`, `Containers`, `Nodes`, `Connectors`, `Labels`.

**Editing workflow:** duplicate a node, rename it, drag it into place, then redraw its connector in the same color and weight. Keep new elements on the 8 px grid.

---

## 10. Content scope of the sample data

Sample content comes from the RESQPERATION repo (Laravel API, React + Vite HQ Web, Expo mobile app with Household and Rescuer roles, MySQL, OneSignal, SMS gateway, weather, routing, TrackingAid). Table names follow the model names; columns are examples; swap in the real schema.

## 11. Final check before sharing a diagram

- [ ] Only tokens from section 2.1 are used
- [ ] Every shape matches the size, radius and border in sections 4 and 7
- [ ] All connectors are 1.75 px, orthogonal, with the right arrowhead
- [ ] Every connector that needs a label has a label chip
- [ ] No legend, notes or paragraphs on the canvas
- [ ] Labels are short, Title Case (use cases verb-first, tables snake_case)
- [ ] Mobile items use the split `blue` / `cyan` treatment where both roles share a node
