# Users
Doctors

# Purpose
* Illness Lists
* Medicines List
* Patient List
* Lab Test List
* Symptoms List
* Refer Other Doctors list
* Prescribing medicines to patients
* Patient Prescription Record maintenance
* Advice section in prescription
* Print Prescription
* Templated prescriptions
* Templated Advice

# Additional Notes
* Expect around 100-150 to patients daily
* Town and Village levels patients. Rare Urban patients possibility
* Language mapping (per doctor review of mockups):
  - App interface (UI labels, navigation, buttons, field labels): English
  - Patient name: English (for search) + Marathi (displayed alongside English)
  - Symptom name: English
  - Illness name: Marathi
  - Referral doctor name: Marathi
  - Advice text (prescriptions and advice templates): Marathi
  - Dose Time labels: Marathi (सकाळी / दुपारी / संध्याकाळी / रात्री)
  - Prerequisite: English + Marathi (After Food / जेवणानंतर, Before Food / जेवणापूर्वी, Empty Stomach / रिकाम्या पोटी, None / काहीही नाही)
  - Medicine names: English (e.g., Paracetamol, Azithromycin)
  - Medicine type (Tablet, Capsule, Fluid, Injection): English
  - Lab test names: English
  - Gender, Age, Mobile Number, Residence, Date: English
  - Prescription template names: English
  - Hindi support deferred to future
* Default landing page: New Prescription (not Dashboard)
* Multiple prescriptions: In-app tabs for simultaneous prescriptions for different patients
* Patient types - starting with OPD only, Admit fields to be added in future

# Key Workflows
## Illness List Maintenance
* Add / Update / Delete Records
* Illness Records contains - Illness Name
* Illness is included in prescriptions
## Medicines List
* Add / Update / Delete Records
* Medicine List contains - Medicine Name, Type (Fluid / Capsule / Tablet / Injection), Duration (default duration 5 days), Dose Times (Morning, Afternoon, Evening, Night), Pre-requisite (Empty Stomach, After food, Before Food)
## Patient List
* Add / Update / Delete Records
* Patient List contains - Name (English), Name (Marathi), Gender, Age, Mobile Number, Residence
* Search by English name; display shows both English and Marathi names
## Lab Test List
* Add / Update / Delete Records
* Lab Test List Contains - Lab Test Name
## Symptoms List
* Add / Update / Delete Records
* Symptoms list contains - Symptom name
## Refer Other Doctors List
* Add / Update / Delete Records
* Each record contains - Doctor Name, Doctor Address and Doctor Phone Number
## Prescribing Medicines to Patients
* Doctor Enters Patient Details - Name, Age, Gender, Date, Mobile Number, Residence
    - If existing patient, list shall auto suggest name and other details
* Doctor notes symptoms from symptoms list
* App recommends Prescription from the Templated prescriptions based on doctor's manual tags
* Doctor can also search and select prescription template manually
* Illness is optionally part of the prescription
* Doctor can modify the prescription - add, modify or delete particular medicine in the prescription
* If Templated prescription do not match, doctor creates custom prescription
* Doctor recommends advice from Templated Advice
* Advice can be modified by doctor
* Doctor recommends lab tests
* Doctor can modify list of lab tests
* Print the prescription
* Any new patient, symtoms, medicines, advice, lab test etc. shall get added to respective list
* Doctor shall be able to save the current prescription as template
* Prescription shall have field to note - blood pressure and temperature and SPO2 and pulse

## Patient Prescription Record maintenance
* View patient prescription history (read-only)
* Past records cannot be edited or deleted
* Patients do not have access to the application

## Advice section in prescription
* Free text advice sourced from templated advice
* Doctor can modify advice text

## Print Prescription
* Letterhead with pre-printed headers and footers will be used (provided externally)
* App shall focus on per-patient prescription details only (not the letterhead)
## Templated prescriptions
* Doctor manually tags templates (associates templates with symptoms or names)
* App recommends templates based on these manual tags
## Templated Advice
* Doctor manually tags advice templates for reuse

# Platform
* Start with Web app
* Extend to Android in future

# Backend Preferences
* Python, Fast API
* Database - any free and light weight database

# Integrations
* No external Integrations required right now
* Create Local Databases
* These shall be extensible in future

# Compliance
* No compliance needed at this stage
* App is in private mode and used only by one doctor

# Auth Model
* Not Required
* Enable non login based access



