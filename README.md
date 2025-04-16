# Final Project Plan: Encounter Mapping and Code Grouping

## Input

We will use three input datasets:

- **Database A**: Contains two columns – `patientid` and `date of birth` (already in date format)
- **Database B**: Contains `patientid`, `encounterid`, `encounterdate`, and `localcode`
- **Mapping Table**: Contains `localcode` and its corresponding `groupcode` (one-to-one mapping)

---

## Functionality

### 1. Load Data into Python Classes (or optionally SQLite)

Read the two datasets (A and B) and store the information in appropriate Python class instances.  
SQLite may optionally be used for intermediate storage or demonstration, but the primary implementation will use plain Python and class-based data structures.

### 2. Identify a Cohort of Patients Aged 10–17 at Encounter Time

For each encounter, compute the patient’s age at the time of the encounter using their date of birth.  
Then filter out only those encounters where the patient was between 10 and 17 years old (inclusive).  
The filtered results (including `patientid`, `encounterid`, `encounterdate`, and `localcode`) will be stored in a separate class instance (e.g., `FilteredEncounterData`).

### 3. Map Local Codes to Group Codes

Read the mapping table and apply it to the filtered data, converting each `localcode` into its corresponding `groupcode`.  
The mapped group codes will be appended to the filtered data structure.

### 4. Generate Monthly Co-occurrence Counts

For each `patientid` and each calendar month (based on the `encounterdate`), count how many times each `groupcode` appears.  
The output will be a table or CSV file with the following structure:

- `month` (in `YYYY-MM` format)  
- `patientid`  
- `groupcode`  
- `count` (number of occurrences in that month for that patient)

## Purpose

The primary goal of the project is to process raw EHR data, extract a cohort within a specific age range, and generate a group code co-occurrence table. This table can be used for downstream modeling and evaluation.
