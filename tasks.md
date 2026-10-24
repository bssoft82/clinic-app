# Clinic Prescription App - Implementation Tasks

Tasks are ordered by dependency. Each task has clear acceptance criteria.

**Legend:** B = Backend, F = Frontend

---

## Task 1: Scaffold Backend Project (B)

**Dependencies:** None

**Steps:**
- Create `backend/` directory with `app/` package structure per design section 5
- Create Python virtual environment, install: `fastapi`, `uvicorn[standard]`, `sqlalchemy>=2.0`, `alembic`, `pydantic>=2`
- `config.py`: Settings with SQLite URL (`sqlite:///./clinic.db`)
- `database.py`: Engine, session factory, `get_db` dependency
- `main.py`: FastAPI app instance, CORS middleware (allow frontend origin), health check endpoint
- `run.py`: Uvicorn launcher (`uvicorn app.main:app --reload --port 8000`)
- `requirements.txt`: Pinned versions

**Acceptance:**
- `python run.py` starts server on port 8000
- `GET /api/v1/health` returns `{"status": "ok"}`

---

## Task 2: Create Database Models (B)

**Dependencies:** Task 1

**Steps:**
- Define Python enums: `MedicineType` (Fluid, Capsule, Tablet, Injection), `DoseTime` (MORNING, AFTERNOON, EVENING, NIGHT), `Prerequisite` (AFTER_FOOD, BEFORE_FOOD, EMPTY_STOMACH, NONE), `Gender` (Male, Female, Other)
- Create SQLAlchemy models per design section 2:
  - `Illness` (id, name, created_at, updated_at)
  - `Medicine` (id, name, medicine_type, default_duration_days=5, dose_times JSON, prerequisite nullable)
  - `Patient` (id, name, name_marathi, gender, age, mobile_number, residence, timestamps)
  - `LabTest` (id, name, timestamps)
  - `Symptom` (id, name unique, timestamps)
  - `ReferralDoctor` (id, name, address, phone_number, timestamps)
  - `AdviceTemplate` (id, text, timestamps)
  - `PrescriptionTemplate` (id, name, timestamps) + sub-tables: TemplateSymptom, TemplateMedicine, TemplateAdvice, TemplateLabTest
  - `Prescription` (id, patient_id FK, date, patient_type="OPD", illness_id nullable FK, blood_pressure, temperature, spo2, pulse, created_at) + sub-tables: PrescriptionSymptom, PrescriptionMedicine, PrescriptionAdvice, PrescriptionLabTest, PrescriptionReferral
- Add `created_at`/`updated_at` mixins

**Acceptance:**
- All models import without errors
- `python -c "from app.models import *"` succeeds

---

## Task 3: Create Alembic Migration + Initial Schema (B)

**Dependencies:** Task 2

**Steps:**
- Initialize Alembic: `alembic init alembic`
- Configure `alembic.ini` with SQLite URL
- Configure `alembic/env.py` to use `app.models` Base metadata
- Generate initial migration: `alembic revision --autogenerate -m "initial schema"`
- Run migration: `alembic upgrade head`

**Acceptance:**
- `clinic.db` file created
- All tables present (verify with `sqlite3` or DB browser)
- Migration is re-runnable (`alembic downgrade base` then `alembic upgrade head` works)

---

## Task 4: Create Pydantic Schemas (B)

**Dependencies:** Task 2

**Steps:**
- Create schemas per entity in `app/schemas/`:
  - Simple CRUD schemas: Illness, LabTest, Symptom, AdviceTemplate (name/text + id + timestamps)
  - Medicine schema: includes medicine_type enum, default_duration_days, dose_times list, prerequisite enum
  - Patient schema: name, name_marathi, gender, age, mobile_number, residence
  - ReferralDoctor schema: name, address, phone_number
  - PrescriptionTemplateCreate: nested symptom_ids, medicines, advice, lab_test_ids
  - PrescriptionTemplateResponse: full detail with all sub-items
  - PrescriptionCreate: nested patient (id or new), symptoms (id or new), medicines, advice, lab_tests (id or new), referrals (id or new), vital signs, illness_id, save_as_template flag, template_symptom_ids
  - PrescriptionResponse: full detail with patient, symptoms, medicines, advice, lab_tests, referrals
  - PaginatedResponse generic: items, total, skip, limit

**Acceptance:**
- Schemas validate sample JSON correctly
- PrescriptionCreate with `id: null` items parses without error

---

## Task 5: Implement Backend CRUD + API Routers (B)

**Dependencies:** Tasks 3, 4

**Steps:**
- `app/crud/base.py`: Generic CRUD class (get_all with search/pagination, get_by_id, create, update, delete)
- Master data routers (all in `app/routers/`):
  - `illnesses.py`, `medicines.py`, `patients.py` (search by English name), `lab_tests.py`, `symptoms.py`, `referral_doctors.py`, `advice_templates.py`
  - Each: GET list (with `q`, `skip`, `limit`), GET by id, POST, PUT, DELETE
- `prescription_templates.py`:
  - CRUD + `GET /recommend?symptom_ids=1,2,3` (returns templates whose symptom tags overlap)
- `prescriptions.py`:
  - `GET /prescriptions` (filters: `patient_id`, `date`, `q` for patient name search)
  - `GET /prescriptions/{id}` (full detail with all nested items)
  - `POST /prescriptions` — **auto-create pattern**: for items with `id: null`, create master record first, then link. All in one DB transaction.
  - If `save_as_template: true`, also create a PrescriptionTemplate from the current prescription
  - `DELETE /prescriptions/{id}` → return 405 (immutable)
- Register all routers in `main.py`

**Acceptance:**
- API docs at `http://localhost:8000/docs` show all endpoints
- POST prescription with new patient + new symptoms → creates master records + prescription
- GET prescription detail returns full nested data
- Template recommend returns matching templates by symptom overlap

---

## Task 6: Scaffold Frontend Project (F)

**Dependencies:** None (can run in parallel with backend tasks)

**Steps:**
- `npm create vite@latest frontend -- --template react-ts`
- Install: `tailwindcss`, `postcss`, `autoprefixer`, `react-router-dom`, `axios`
- Configure Tailwind (`tailwind.config.js`, `postcss.config.js`, import in `index.css`)
- Load Noto Sans Devanagari via Google Fonts in `index.html`
- Configure Vite proxy: `/api` → `http://localhost:8000`
- Set up `tsconfig.json` path aliases

**Acceptance:**
- `npm run dev` starts on port 5173
- Tailwind styles apply (test with a `bg-teal-500` div)
- Devanagari font loads (Marathi text renders correctly)

---

## Task 7: Build Layout + Routing (F)

**Dependencies:** Task 6

**Steps:**
- `Layout.tsx`: Sidebar navigation + top bar + content area
  - Sidebar items: Dashboard, New Prescription, History, then Master Data section (Illnesses, Medicines, Patients, Lab Tests, Symptoms, Referral Doctors, Advice Templates, Rx Templates)
  - Active route highlighting
- `App.tsx`: React Router setup
  - `/` → New Prescription (default landing)
  - `/dashboard` → Dashboard
  - `/prescriptions` → History
  - `/prescriptions/:id` → Detail/Print
  - `/illnesses`, `/medicines`, `/patients`, `/lab-tests`, `/symptoms`, `/referral-doctors`, `/advice-templates`, `/prescription-templates`
- `api/client.ts`: Axios instance with baseURL `/api/v1`, typed API functions for all endpoints

**Acceptance:**
- Sidebar navigation works, routes resolve correctly
- Default landing is New Prescription page (even if empty placeholder)
- API client functions are typed and callable

---

## Task 8: Build Reusable Components (F)

**Dependencies:** Task 7

**Steps:**
- `CrudTable.tsx`: Generic table component
  - Props: columns config, fetch function, create/update/delete functions, search input
  - Add/Edit modal with form fields (configurable per entity)
  - Delete confirmation dialog
- `Typeahead.tsx`: Async search input
  - Props: search function, display field, free-text entry flag, onSelect callback
  - Dropdown with results, free-text creates new item
  - Patient typeahead shows both English + Marathi name in dropdown
- `MultiSelectTag.tsx`: Multi-value typeahead
  - Chip display for selected items, × to remove, type to add new
  - Props: search function, selected items, onChange
- `PrescriptionTabs.tsx`: Tab bar for multiple prescriptions
  - Tab per in-progress prescription (title = patient English name or "New Patient")
  - "+" button to open new tab, "×" to close (warn if unsaved)
  - Active tab switching, state preserved per tab in React state
  - Optional: persist tab state to localStorage

**Acceptance:**
- CrudTable renders with mock data, add/edit/delete modal works
- Typeahead shows dropdown results, free-text entry creates new item
- MultiSelectTag adds/removes chips
- PrescriptionTabs opens/closes/switches tabs with unsaved-changes warning

---

## Task 9: Implement Master Data Pages (F)

**Dependencies:** Tasks 5, 8

**Steps:**
- Create page components using CrudTable for each master data entity:
  - `Illnesses.tsx` — columns: name (Marathi input)
  - `Medicines.tsx` — columns: name (English), type (dropdown), default_duration, dose_times (Marathi checkbox labels), prerequisite (dropdown with English + Marathi)
  - `Patients.tsx` — columns: name (English), name_marathi (Marathi input), gender, age, mobile, residence
  - `LabTests.tsx` — columns: name (English)
  - `Symptoms.tsx` — columns: name (English)
  - `ReferralDoctors.tsx` — columns: name (Marathi), address, phone
  - `AdviceTemplates.tsx` — columns: text (Marathi)
  - `PrescriptionTemplates.tsx` — card-based layout: name (English), symptom tags (English chips), medicines (English), advice (Marathi), lab tests (English)
- Connect each page to backend API via `api/client.ts`

**Acceptance:**
- All 8 pages render with data from backend
- CRUD operations (add, edit, delete) work for all entities
- Language mapping correct: Marathi inputs for patient name_mr, illness, referral, advice; English for symptoms, medicines, lab tests

---

## Task 10: Build New Prescription — Patient + Symptoms + Templates (F)

**Dependencies:** Tasks 5, 8

**Steps:**
- Integrate PrescriptionTabs at top of page
- Patient Details section:
  - English name typeahead (searches backend by English name, dropdown shows "English (Marathi) · age · gender · mobile")
  - Selecting existing patient auto-fills: name_marathi, age, gender, mobile, residence
  - Marathi name input field (separate, editable)
  - Age, gender (dropdown), date, mobile, residence fields
  - Vital signs row: blood_pressure, temperature, spo2, pulse (optional fields)
- Symptoms section:
  - MultiSelectTag with English symptom names
  - Free-text entry creates new symptom (saved on prescription save)
- Template Recommendations:
  - When symptoms selected, call `GET /prescription-templates/recommend?symptom_ids=...`
  - Display matching templates as cards (template name + brief content)
  - Click "Apply" loads template's medicines, advice, lab tests into the form

**Acceptance:**
- Patient search by English name works, auto-fills all fields including Marathi name
- New patient can be typed (no existing match)
- Symptoms add/remove as chips with English names
- Template recommendations appear after symptoms selected
- Applying a template populates medicines, advice, and lab tests

---

## Task 11: Build New Prescription — Medicines + Advice + Labs + Referrals + Save (F)

**Dependencies:** Task 10

**Steps:**
- Medicines section:
  - List of medicine rows, each with: medicine name typeahead (English), type (auto-filled), duration (days, default from medicine), dose time checkboxes (Marathi labels: सकाळी/दुपारी/संध्याकाळी/रात्री), prerequisite dropdown (English + Marathi: "After Food / जेवणानंतर" etc.)
  - Add/remove medicine rows
  - Free-text medicine name creates new Medicine record on save
- Advice section:
  - Free text textarea (Marathi), with typeahead chips from advice templates to insert
  - Add/remove advice entries
- Lab Tests section:
  - MultiSelectTag with English names, free-text creates new on save
- Referrals section:
  - MultiSelectTag with Marathi doctor names, free-text creates new on save
- Actions:
  - "Save & Print" → POST to `/prescriptions` (with auto-create for new items) → open print view in new tab (`/prescriptions/{id}`)
  - "Save as Template" → dialog to name template + select symptom tags → POST to `/prescription-templates`
  - Unsaved-changes warning when closing tab

**Acceptance:**
- Medicine rows add/remove, dose times show Marathi checkboxes, prerequisites show English + Marathi
- Advice text is Marathi, template insertion works
- Lab tests and referrals add/remove as chips
- Save & Print creates prescription (new items auto-created), opens print view
- Save as Template creates template with symptom tags
- Closing a tab with unsaved data shows warning

---

## Task 12: Build Prescription History + Print View (F)

**Dependencies:** Task 5, 8

**Steps:**
- `PrescriptionHistory.tsx`:
  - Searchable table: patient name (English, with Marathi in smaller text), date, age, gender, symptoms (English), medicine count, type
  - Search by patient English name, filter by date
  - Paginated (50 per page)
  - Read-only — no edit/delete buttons
  - "View" action → navigates to `/prescriptions/:id`
- `PrintView.tsx`:
  - Fetch prescription detail by id
  - Layout: prescription number, date, patient info (English name + Marathi in parentheses), vital signs row, symptoms (English), medicines table (English names, Marathi dose times, dual-language prerequisites), lab tests (English), advice (Marathi), referrals (Marathi name + English address)
  - CSS `@media print`: margin-top 3cm, margin-bottom 2cm (for pre-printed letterhead)
  - `window.print()` triggered on load
  - Print button visible on screen, hidden when printing
  - Dashed-line markers showing letterhead areas (screen only)

**Acceptance:**
- History page lists prescriptions with dual patient names, searchable, paginated
- Print view renders all fields with correct language mapping
- Browser print dialog opens, output has correct margins for letterhead
- Print button hidden in print output

---

## Task 13: Seed Data + End-to-End Verification (B+F)

**Dependencies:** All previous tasks

**Steps:**
- Create `backend/seed.py` script:
  - Sample medicines: Paracetamol (Tablet, 5 days, Morning+Night, After Food), Azithromycin (Tablet, 3 days, Morning, Empty Stomach), Omeprazole (Capsule, 7 days, Morning, Empty Stomach), Cetirizine (Tablet, 5 days, Night, None), Ibuprofen (Tablet, 5 days, Morning+Evening, After Food), ORS Powder (Fluid, 3 days, Morning+Afternoon+Night, After Food)
  - Sample symptoms: Fever, Cough, Cold, Headache, Sore Throat, Stomach Pain, Body Pain, Joint Pain, Vomiting, Diarrhea
  - Sample illnesses (Marathi): साधा ताप, श्वसनमार्ग संक्रमण, पोटाचा त्रास
  - Sample referral doctors (Marathi): डॉ. शर्मा (Pune, 9123456789)
  - Sample advice templates (Marathi): भरपूर पाणी प्या, विश्रांती घ्या, गरम पाणी प्या, ओले पदार्थ टाळा
  - Sample prescription templates: Simple Fever Template (tags: Fever, Body Pain), Respiratory Template (tags: Cough, Cold, Sore Throat), Stomach Pain Template (tags: Stomach Pain, Vomiting), Joint Pain Template (tags: Joint Pain)
- Full workflow test:
  1. Open app → lands on New Prescription with one tab
  2. Search patient "Ramesh" → typeahead shows matches → select → fields auto-fill
  3. Add symptoms: Fever, Cough → template recommendations appear
  4. Apply "Respiratory Template" → medicines, advice, lab tests load
  5. Modify: add another medicine, edit advice text
  6. Enter vital signs: BP 120/80, Temp 98.6, SpO2 98, Pulse 72
  7. Click "Save & Print" → prescription saved, print view opens
  8. Verify print view shows all details with correct languages
  9. Open second tab "+" → start new prescription for different patient
  10. Go to History → verify both prescriptions listed with dual patient names

**Acceptance:**
- Seed script populates all master data
- Complete prescribing workflow works end-to-end
- Multiple tabs work simultaneously
- History shows saved prescriptions
- Print view renders correctly with pre-printed margins
- New items (patient, symptom, medicine, lab test, referral) auto-created in master data
