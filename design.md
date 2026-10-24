# Clinic Prescription App - Design Document

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (React)                 │
│  Vite + TypeScript + Tailwind CSS                   │
│  Port: 5173                                         │
└──────────────────────┬──────────────────────────────┘
                       │ REST API (JSON)
┌──────────────────────▼──────────────────────────────┐
│                  Backend (FastAPI)                  │
│  Python 3.11+ + SQLAlchemy 2.0 + Pydantic v2        │
│  Port: 8000                                         │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│              Database (SQLite)                      │
│  File-based, serverless, zero-config                │
└─────────────────────────────────────────────────────┘
```

### Tech Stack

| Layer       | Technology                        | Rationale                                    |
|-------------|-----------------------------------|--------------------------------------------- |
| Backend     | Python 3.11+, FastAPI             | User preference; async, auto-docs, fast     |
| ORM         | SQLAlchemy 2.0                    | Mature, well-documented, SQLite support      |
| Database    | SQLite                            | Free, lightweight, file-based, zero-config   |
| Migrations  | Alembic                           | Standard for SQLAlchemy, schema evolution    |
| Validation  | Pydantic v2                       | Bundled with FastAPI, request/response models|
| Server      | Uvicorn                           | ASGI server for FastAPI                      |
| Frontend    | React 18 + TypeScript             | Rich ecosystem, future Android portability   |
| Build       | Vite                              | Fast dev server and builds                    |
| Styling     | Tailwind CSS                      | Utility-first, no CSS file sprawl, print-ready|
| Routing     | React Router v6                   | Standard SPA routing                          |
| Font        | Noto Sans Devanagari (Google)     | Devanagari rendering for Marathi fields       |
| HTTP Client | Axios                             | Simple, interceptors, widespread use          |

### Non-Functional Considerations

- **No authentication** — single-doctor private app, non-login access as specified
- **Language** — UI in English. Marathi for specific data fields: patient name (MR), illness name, referral doctor name, advice text, dose times, prerequisites. Devanagari font loaded for Marathi rendering
- **Performance** — 100-150 patients/day means ~150 prescriptions max/day. SQLite handles this with ease
- **Print** — browser print with CSS `@media print` rules; top/bottom margins configured to avoid pre-printed letterhead areas
- **Future Android** — API-first design ensures the backend is reusable for a future mobile client

---

## 2. Data Models

### Entity Relationship Overview

```
Illness (optionally linked to prescriptions as diagnosis)

Medicine ────────────────────────┐
Symptom ─────────────────────┐   │
LabTest ──────────────────┐   │   │
ReferralDoctor ─────────┐ │   │   │
AdviceTemplate ──────┐   │ │   │   │
                     │   │ │   │   │
Patient ─┐           │   │ │   │   │
         │           │   │ │   │   │
         ▼           ▼   ▼ ▼   ▼   ▼
      Prescription ───────────────────────
         │
         ├──> Illness (optional FK, diagnosis)
         ├──> PrescriptionSymptom (M:N → Symptom)
         ├──> PrescriptionMedicine  (M:N → Medicine, with per-Rx overrides)
         ├──> PrescriptionAdvice    (free text, optionally sourced from AdviceTemplate)
         ├──> PrescriptionLabTest   (M:N → LabTest)
         └──> PrescriptionReferral   (M:N → ReferralDoctor)

PrescriptionTemplate ─┐
         │
         ├──> PrescriptionTemplateSymptom (tags for recommendation matching)
         ├──> PrescriptionTemplateMedicine (with per-template overrides)
         ├──> PrescriptionTemplateAdvice  (free text)
         └──> PrescriptionTemplateLabTest  (M:N → LabTest)
```

### Model Definitions

#### 2.1 Illness

| Field       | Type   | Notes                          |
|-------------|--------|-------------------------------|
| id          | int PK | Auto-increment                 |
| name        | str    | Unique, required              |
| created_at  | datetime | Auto                         |
| updated_at  | datetime | Auto                         |

Optionally included in prescriptions (per doctor update).

#### 2.2 Medicine

| Field                | Type     | Notes                                         |
|----------------------|----------|-----------------------------------------------|
| id                   | int PK   | Auto-increment                                |
| name                 | str      | Required                                      |
| medicine_type        | enum     | Fluid, Capsule, Tablet, Injection             |
| default_duration_days| int      | Default 5                                     |
| dose_times            | JSON arr | Subset of: Morning, Afternoon, Evening, Night |
| prerequisite         | enum     | Empty Stomach, After Food, Before Food        |
| created_at           | datetime | Auto                                          |
| updated_at           | datetime | Auto                                          |

`dose_times` stored as JSON array (e.g., `["Morning", "Night"]`).
`prerequisite` is nullable — not all medicines have food-timing constraints. Displayed as English + Marathi (e.g., "After Food / जेवणानंतर").

#### 2.3 Patient

| Field         | Type   | Notes                              |
|---------------|--------|------------------------------------|
| id            | int PK | Auto-increment                     |
| name          | str    | Required (English, used for search)|
| name_marathi  | str    | Optional (Marathi, displayed alongside)|
| gender        | enum   | Male, Female, Other                |
| age           | int    | Required, as entered (no DOB)      |
| mobile_number | str    | Optional                           |
| residence     | str    | Optional                           |
| created_at    | datetime | Auto                              |
| updated_at    | datetime | Auto                              |

Age is a simple integer field as specified. No date-of-birth calculation. Patient name has both English (for search) and Marathi (for display) fields.

#### 2.4 LabTest

| Field      | Type   | Notes              |
|------------|--------|--------------------|
| id         | int PK | Auto-increment     |
| name       | str    | Required           |
| created_at | datetime | Auto             |
| updated_at | datetime | Auto             |

#### 2.5 Symptom

| Field      | Type   | Notes              |
|------------|--------|--------------------|
| id         | int PK | Auto-increment     |
| name       | str    | Unique, required   |
| created_at | datetime | Auto             |
| updated_at | datetime | Auto             |

#### 2.6 ReferralDoctor

| Field        | Type   | Notes              |
|--------------|--------|--------------------|
| id           | int PK | Auto-increment     |
| name         | str    | Required           |
| address      | str    | Optional           |
| phone_number | str    | Optional           |
| created_at   | datetime | Auto            |
| updated_at   | datetime | Auto            |

#### 2.7 AdviceTemplate

| Field      | Type   | Notes                    |
|------------|--------|--------------------------|
| id         | int PK | Auto-increment           |
| text       | str    | Required, free text      |
| created_at | datetime | Auto                  |
| updated_at | datetime | Auto                  |

#### 2.8 PrescriptionTemplate

| Field      | Type   | Notes                          |
|------------|--------|--------------------------------|
| id         | int PK | Auto-increment                 |
| name       | str    | Required (doctor-assigned tag) |
| created_at | datetime | Auto                        |
| updated_at | datetime | Auto                        |

**PrescriptionTemplateSymptom** (association table — tags for recommendation matching)

| Field                   | Type  | Notes                        |
|-------------------------|-------|------------------------------|
| id                      | int PK| Auto-increment               |
| prescription_template_id | int FK| → PrescriptionTemplate.id    |
| symptom_id              | int FK| → Symptom.id                 |

**PrescriptionTemplateMedicine**

| Field                   | Type     | Notes                                    |
|-------------------------|----------|------------------------------------------|
| id                      | int PK   | Auto-increment                           |
| prescription_template_id | int FK   | → PrescriptionTemplate.id               |
| medicine_id             | int FK   | → Medicine.id                            |
| duration_days           | int      | Default from Medicine.default_duration   |
| dose_times              | JSON arr | Subset of: Morning, Afternoon, Evening, Night |
| prerequisite            | enum     | Nullable; from Medicine default          |

**PrescriptionTemplateAdvice**

| Field                   | Type   | Notes                    |
|-------------------------|--------|--------------------------|
| id                      | int PK | Auto-increment           |
| prescription_template_id | int FK | → PrescriptionTemplate.id|
| advice_text             | str    | Free text                |

**PrescriptionTemplateLabTest** (association table)

| Field                   | Type  | Notes                    |
|-------------------------|-------|--------------------------|
| id                      | int PK| Auto-increment           |
| prescription_template_id | int FK| → PrescriptionTemplate.id|
| lab_test_id             | int FK| → LabTest.id              |

#### 2.9 Prescription

| Field        | Type     | Notes                                      |
|--------------|----------|--------------------------------------------|
| id           | int PK   | Auto-increment                             |
| patient_id   | int FK   | → Patient.id                               |
| date         | date     | Required (prescription date)              |
| patient_type | str      | Default "OPD"; "Admit" reserved for future |
| illness_id   | int FK   | Optional (→ Illness.id, diagnosis)        |
| blood_pressure | str    | Optional (e.g., "120/80")                |
| temperature  | str      | Optional (e.g., "98.6 F")                |
| spo2         | str      | Optional (e.g., "98%")                   |
| pulse        | str      | Optional (e.g., "72 bpm")                |
| created_at   | datetime | Auto                                       |

**PrescriptionSymptom**

| Field           | Type  | Notes              |
|-----------------|-------|--------------------|
| id              | int PK| Auto-increment     |
| prescription_id  | int FK| → Prescription.id  |
| symptom_id      | int FK| → Symptom.id       |

**PrescriptionMedicine**

| Field          | Type     | Notes                                             |
|----------------|----------|---------------------------------------------------|
| id             | int PK   | Auto-increment                                    |
| prescription_id| int FK   | → Prescription.id                                  |
| medicine_id    | int FK   | → Medicine.id                                      |
| duration_days  | int      | Per-prescription override (defaults from Medicine)|
| dose_times     | JSON arr | Per-prescription override                          |
| prerequisite   | enum     | Per-prescription override; nullable               |

**PrescriptionAdvice**

| Field           | Type  | Notes                    |
|-----------------|-------|--------------------------|
| id              | int PK| Auto-increment           |
| prescription_id | int FK| → Prescription.id        |
| advice_text     | str   | Free text                |

**PrescriptionLabTest**

| Field           | Type  | Notes              |
|-----------------|-------|--------------------|
| id              | int PK| Auto-increment     |
| prescription_id | int FK| → Prescription.id  |
| lab_test_id     | int FK| → LabTest.id       |

**PrescriptionReferral**

| Field               | Type  | Notes                    |
|---------------------|-------|--------------------------|
| id                  | int PK| Auto-increment           |
| prescription_id     | int FK| → Prescription.id        |
| referral_doctor_id  | int FK| → ReferralDoctor.id      |

---

## 3. API Design

Base URL: `/api/v1`

All responses are JSON. Standard patterns:
- List: `GET /resource` (supports `q` query param for search, `skip`/`limit` for pagination)
- Create: `POST /resource`
- Update: `PUT /resource/{id}`
- Delete: `DELETE /resource/{id}`

### 3.1 Master Data Endpoints

| Resource             | Endpoint                        | Operations         |
|----------------------|---------------------------------|--------------------|
| Illnesses            | `/api/v1/illnesses`             | GET, POST, PUT, DELETE |
| Medicines            | `/api/v1/medicines`             | GET, POST, PUT, DELETE |
| Patients             | `/api/v1/patients`               | GET, POST, PUT, DELETE |
| Lab Tests            | `/api/v1/lab-tests`             | GET, POST, PUT, DELETE |
| Symptoms             | `/api/v1/symptoms`              | GET, POST, PUT, DELETE |
| Referral Doctors    | `/api/v1/referral-doctors`      | GET, POST, PUT, DELETE |
| Advice Templates     | `/api/v1/advice-templates`      | GET, POST, PUT, DELETE |

### 3.2 Prescription Templates

| Method   | Endpoint                                        | Description                          |
|----------|-------------------------------------------------|--------------------------------------|
| GET      | `/api/v1/prescription-templates`                 | List all templates                   |
| GET      | `/api/v1/prescription-templates/{id}`           | Get template detail with all sub-items|
| POST     | `/api/v1/prescription-templates`                | Create template with medicines, advice, lab tests, symptom tags |
| PUT      | `/api/v1/prescription-templates/{id}`           | Update template                      |
| DELETE   | `/api/v1/prescription-templates/{id}`           | Delete template                      |
| GET      | `/api/v1/prescription-templates/recommend`      | `?symptom_ids=1,2,3` — returns templates whose symptom tags overlap with the query |

### 3.3 Prescriptions

| Method   | Endpoint                                        | Description                          |
|----------|-------------------------------------------------|--------------------------------------|
| GET      | `/api/v1/prescriptions`                         | List with filters: `patient_id`, `date`, `q` (patient name search) |
| GET      | `/api/v1/prescriptions/{id}`                    | Full prescription detail (patient, symptoms, medicines, advice, lab tests, referrals) |
| POST     | `/api/v1/prescriptions`                          | Create prescription (all sections in one transaction) |
| DELETE   | `/api/v1/prescriptions/{id}`                    | Delete — not supported (405) per requirement: past records are immutable |

### 3.4 Auto-Create Pattern

When creating a prescription, the frontend may send new (un-saved) items inline. The backend auto-creates master records as needed:

- New patient name → create Patient record, link by ID
- New symptom name → create Symptom record, link by ID
- New medicine name → create Medicine record (with defaults), link by ID
- New advice text → optionally create AdviceTemplate if doctor chooses "save as template"
- New lab test name → create LabTest record, link by ID
- New referral doctor → create ReferralDoctor record, link by ID

**Request body for POST /api/v1/prescriptions:**

```json
{
  "patient": { "id": null, "name": "Ramesh Patil", "name_marathi": "रमेश पाटील", "gender": "Male", "age": 45, "mobile_number": "9876543210", "residence": "Shirur" },
  "date": "2026-10-24",
  "patient_type": "OPD",
  "illness_id": null,
  "blood_pressure": "120/80",
  "temperature": "98.6",
  "spo2": "98",
  "pulse": "72",
  "symptoms": [
    { "id": null, "name": "Fever" },
    { "id": 5, "name": "Cough" }
  ],
  "medicines": [
    {
      "medicine": { "id": 3, "name": "Paracetamol", "medicine_type": "Tablet" },
      "duration_days": 5,
      "dose_times": ["MORNING", "NIGHT"],
      "prerequisite": "AFTER_FOOD"
    }
  ],
  "advice": [
    { "advice_text": "भरपूर पाणी प्या आणि विश्रांती घ्या." }
  ],
  "lab_tests": [
    { "id": null, "name": "Complete Blood Count" }
  ],
  "referrals": [
    { "id": 2, "name": "डॉ. शर्मा", "address": "Pune", "phone_number": "9123456789" }
  ],
  "save_as_template": false,
  "template_symptom_ids": []
}
```

Items with `id: null` are auto-created in the master table before linking.

### 3.5 Pagination

List endpoints accept `skip` (default 0) and `limit` (default 50, max 200). Response shape:

```json
{
  "items": [...],
  "total": 150,
  "skip": 0,
  "limit": 50
}
```

---

## 4. Frontend Design

### 4.1 Page Structure

```
/                        → New Prescription (default landing, with in-app tabs)
/dashboard              → Dashboard (today's stats, quick actions)
/prescriptions          → Prescription History (searchable list)
/prescriptions/:id      → Prescription Detail / Print View

Master Data:
/illnesses              → Illness CRUD
/medicines              → Medicine CRUD
/patients               → Patient CRUD
/lab-tests              → Lab Test CRUD
/symptoms               → Symptom CRUD
/referral-doctors       → Referral Doctor CRUD
/advice-templates       → Advice Template CRUD
/prescription-templates → Prescription Template CRUD
```

### 4.2 Layout

```
┌───────────────────────────────────────────────────────┐
│  [Logo]  Clinic Prescription App               [Help] │  ← Top bar
├───────────┬───────────────────────────────────────────┤
│           │                                           │
│ Dashboard │                                           │
│ Prescribe │           Page Content                    │
│ History   │                                           │
│ ────────  │                                           │
│ Illnesses │                                           │
│ Medicines │                                           │
│ Patients │                                           │
│ Lab Tests │                                           │
│ Symptoms  │                                           │
│ Referrals │                                           │
│ Advice    │                                           │
│ Templates │                                           │
│           │                                           │
└───────────┴───────────────────────────────────────────┘
```

### 4.3 New Prescription Page (Core Workflow)

```
┌────────────────────────────────────────────────────────┐
│  New Prescription                                      │
├────────────────────────────────────────────────────────┤
│  [Ramesh Patil ×] [Sunita Deshmukh ×] [+]             │  ← In-app tabs
├────────────────────────────────────────────────────────┤
│                                                        │
│  Patient Details                                       │
│  [Name (EN): typeahead________] [Name (MR): रमेश पाटील]│
│  [Age: __] [Gender: ▼] [Date: ___]                    │
│  [Mobile: ___________] [Residence: ____]              │
│  [BP: ___] [Temp: ___] [SpO2: ___] [Pulse: ___]        │
│                                                        │
│  Symptoms (English)                                    │
│  [Fever ×] [Cough ×] [_____________ type to add]       │
│                                                        │
│  ── Recommended Templates ──                           │
│  [Seasonal Fever Template] [Respiratory Template]      │
│  (based on symptom tags)                               │
│                                                        │
│  Medicines                          [+ Add Medicine]   │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Paracetamol (Tablet)                              │  │
│  │ Duration: [5] days  Dose: [☑सकाळी] [☐दुपारी] [☐संध्याकाळी] [☑रात्री]  │
│  │ Prerequisite: [After Food ▼]          [Remove]    │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  Advice                             [+ Add Advice]      │
│  [भरपूर पाणी प्या आणि विश्रांती घ्या.___]              │
│  [typeahead to insert from templates]                   │
│                                                         │
│  Lab Tests                         [+ Add Lab Test]     │
│  [Complete Blood Count ×] [______ type to add]          │
│                                                         │
│  Refer To                          [+ Add Referral]     │
│  [डॉ. शर्मा ×] [______ type to add]                  │
│                                                       │
│  ┌──────────────────────────────────────┐            │
│  │ [Save & Print]  [Save as Template]   │            │
│  └──────────────────────────────────────┘            │
└──────────────────────────────────────────────────────┘
```

**Key interactions:**
- Patient name typeahead searches existing patients by name/mobile; selecting one auto-fills all fields
- New patient: doctor types details, patient auto-created on save
- Symptoms multi-select: typeahead from master list; typing a new name creates it on save
- Template recommendation: after symptoms selected, fetch templates matching those symptom tags; clicking a template loads its medicines, advice, lab tests into the form
- Medicines: each row is a typeahead for medicine name (from master list or new), with editable duration, dose-time checkboxes, and prerequisite dropdown. Defaults pre-filled from the master Medicine record
- Advice: free text fields with typeahead to insert from advice templates
- Lab tests and referrals: multi-select typeaheads, same auto-create pattern as symptoms
- Save & Print: saves the prescription, then opens the print view in a new tab
- Save as Template: opens a dialog to name the template and select symptom tags

### 4.4 Print View

```
┌───────────────────────────────────────────────────────┐
│  (Pre-printed letterhead area — top margin ~3cm)      │
│                                                       │
│  Date: 24/10/2026          OPD                        │
│                                                       │
│  Patient Name: Ramesh Patil (रमेश पाटील)  Age: 45     │
│  Mobile: 9876543210          Residence: Shirur        │
│  BP: 120/80  Temp: 98.6F  SpO2: 98%  Pulse: 72        │
│                                                       │
│  Symptoms: Fever, Cough                               │
│                                                       │
│  Medicines:                                           │
│  1. Paracetamol (Tablet) — 5 days                     │
│     सकाळी, रात्री — After Food / जेवणानंतर             │
│  2. Azithromycin (Tablet) — 3 days                    │
│     सकाळी — Empty Stomach / रिकाम्या पोटी               │
│                                                       │
│  Lab Tests: Complete Blood Count                      │
│                                                       │
│  Advice: भरपूर पाणी प्या आणि विश्रांती घ्या           │
│                                                       │
│  Refer to: डॉ. शर्मा, Pune — 9123456789              │
│                                                       │
│  (Pre-printed footer area — bottom margin ~2cm)       │
└───────────────────────────────────────────────────────┘
```

CSS `@media print` with `margin-top: 3cm; margin-bottom: 2cm` to avoid pre-printed letterhead. `window.print()` triggered on page load.

### 4.5 Reusable Components

| Component        | Purpose                                           |
|------------------|---------------------------------------------------|
| `Layout`         | Shell with sidebar + top bar                     |
| `CrudTable`      | Generic table with search, add/edit modal, delete |
| `Typeahead`      | Async search input with dropdown + free-text entry|
| `MultiSelectTag` | Multi-value typeahead with chip display            |
| `PrescriptionForm` | The full prescribing workflow form               |
| `PrintView`      | Print-optimized prescription layout                |
| `PrescriptionTabs` | Tab bar for multiple simultaneous prescriptions  |

### 4.6 Language Strategy

App UI is in English. No i18n framework needed (no `react-i18next`).

**Marathi fields** (doctor enters and views in Marathi script):

| Field             | Scope                                                        | Example                  |
|-------------------|--------------------------------------------------------------|--------------------------|
| Patient name (MR) | Marathi name displayed alongside English name                | रमेश पाटील                |
| Illness name      | Illness records                                              | साधा ताप                  |
| Referral doctor   | Referral doctor records                                      | डॉ. शर्मा                 |
| Advice text       | Free text in prescriptions and advice templates              | भरपूर पाणी प्या...        |
| Dose Time         | Enum values displayed in Marathi                              | सकाळी, दुपारी, संध्याकाळी, रात्री |
| Prerequisite      | Enum values displayed as English + Marathi                   | After Food / जेवणानंतर    |

Dose times stored as enum (`MORNING`, `AFTERNOON`, `EVENING`, `NIGHT`) in the database, mapped to Marathi for display:

| DB Value    | Marathi Display |
|-------------|-----------------|
| MORNING     | सकाळी           |
| AFTERNOON   | दुपारी          |
| EVENING     | संध्याकाळी      |
| NIGHT       | रात्री           |

Prerequisite enum mapping:

| DB Value      | English Display    | Marathi Display |
|---------------|---------------------|-----------------|
| AFTER_FOOD    | After Food         | जेवणानंतर        |
| BEFORE_FOOD   | Before Food        | जेवणापूर्वी       |
| EMPTY_STOMACH | Empty Stomach      | रिकाम्या पोटी     |
| NONE          | None               | काहीही नाही       |

**English fields** (everything else):

| Field                     | Example                         |
|---------------------------|---------------------------------|
| Patient name (EN)         | Ramesh Patil (used for search)  |
| Symptom name              | Fever, Cough, Headache          |
| Medicine name             | Paracetamol, Azithromycin       |
| Medicine type             | Tablet, Capsule, Fluid, Injection |
| Lab test name             | Complete Blood Count            |
| Gender                    | Male, Female, Other             |
| All UI labels             | Dashboard, New Prescription, etc. |
| Prescription template name | Seasonal Fever Template        |
| Age, Mobile, Residence    | Numbers / English text          |

Devanagari font (Noto Sans Devanagari) loaded via Google Fonts for Marathi text rendering. No `react-i18next`, no locale files needed.

### 4.7 In-App Prescription Tabs

The New Prescription page supports multiple simultaneous prescriptions via in-app tabs:

```
┌────────────────────────────────────────────────────────┐
│  New Prescription                                      │
├────────────────────────────────────────────────────────┤
│  [Ramesh Patil ×] [Sunita Deshmukh ×] [+]             │  ← Tab bar
├────────────────────────────────────────────────────────┤
│                                                        │
│  (Active tab content - full prescription form)         │
│                                                        │
└────────────────────────────────────────────────────────┘
```

- Each tab holds one in-progress prescription with full form state
- Tab title shows patient English name (or "New Patient" until selected)
- "+" button opens a new blank prescription tab
- Closing a tab warns if unsaved changes exist
- Tab state persists in React state; optionally persisted to localStorage for crash recovery
- Chosen over browser tabs for: state preservation, no page reload, simpler routing, single window

---

## 5. Project Structure

```
clinic-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                # FastAPI app, CORS, router registration
│   │   ├── config.py              # Settings (DB URL, etc.)
│   │   ├── database.py            # Engine, session factory, get_db dependency
│   │   ├── models/                # SQLAlchemy models (one file per entity)
│   │   ├── schemas/               # Pydantic request/response schemas
│   │   ├── routers/               # API route handlers
│   │   └── crud/                  # Reusable CRUD operations
│   ├── alembic/                   # Database migrations
│   ├── alembic.ini
│   ├── requirements.txt
│   └── run.py                     # Uvicorn launcher
├── frontend/
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx                # Router setup
│   │   ├── api/
│   │   │   └── client.ts          # Axios instance + typed API functions
│   │   ├── components/
│   │   ├── pages/
│   │   └── styles/
│   │       └── print.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
├── requirements.md
├── design.md
└── tasks.md
```

---

## 6. Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Database | SQLite | Free, file-based, zero-config, handles 150 Rx/day easily |
| No ORM relationships in schemas | Pydantic schemas are flat | Avoids circular serialization; manual joins in CRUD |
| Auto-create on prescription save | Backend handles inline creation | Doctor never leaves the prescribing page to create master records |
| Prescription immutability | No edit/delete on prescriptions | Per requirement; past records are read-only |
| Template recommendation | Symptom tag overlap | Doctor manually tags templates with symptoms; app recommends by matching |
| Language | English UI + Marathi data fields | Doctor-specified: names, advice, dose times in Marathi; medicines and all other fields in English |
| Print | Browser `@media print` | No PDF library needed; works with pre-printed letterhead via CSS margins |
| Frontend framework | React + Vite | Ecosystem maturity, TypeScript support, future mobile portability |
