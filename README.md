# Final Project: Encounter Mapping and Code Grouping

## Installation

### Prerequisites
- Python 3.10 or later
- `pip` installed

### Installation Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/yy447/teen-encounter-sqlite.git
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

---

## Expected Input File Formats

### 1. Patient Data (`patients.tsv`)
| PatientID | PatientDateOfBirth   |
|-----------|----------------------|
| P001      | 2010-05-01 00:00:00  |
| P002      | 2008-12-15 00:00:00  |
| P003      | 2006-07-20 00:00:00  |

**Fields**  
- `PatientID`: Unique identifier (string)  
- `PatientGender`: `M` (Male) / `F` (Female)  
- `PatientDateOfBirth`: Birth datetime in `YYYY-MM-DD HH:MM:SS` format  

---

### 2. Encounter Data (`encounters.tsv`)
| PatientID | EncounterID | EncounterDateTime    | LocalCode |
|-----------|-------------|----------------------|-----------|
| P001      | E001        | 2023-06-01 08:30:00  | L100      |
| P001      | E002        | 2021-04-15 14:15:00  | L200      |
| P002      | E003        | 2022-08-10 09:45:00  | L300      |
| P003      | E004        | 2023-01-25 10:00:00  | L400      |
| P003      | E005        | 2020-02-02 16:20:00  | L500      |

**Fields**  
- `EncounterID`: Unique encounter identifier (string)  
- `EncounterDateTime`: Encounter datetime in `YYYY-MM-DD HH:MM:SS` format  
- `LocalCode`: Facility-specific medical code (string)  

---

### 3. Code Mapping Table (`mapping.tsv`)
| LocalCode | GroupCode |
|-----------|-----------|
| L100      | G1        |
| L200      | G2        |
| L300      | G3        |
| L400      | G4        |
| L500      | G5        |

**Fields**  
- `LocalCode`: Matches codes from encounters (string)  
- `GroupCode`: Standardized grouping code (string)  

## Functionality

### 1. Load Data into Python Classes

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

## Example Usage

```python
from src.ehr_processor import (
    load_patients,
    load_encounters,
    filter_adolescents,
    MapTable,
    generate_cooccurrence_table
)
```
# 1. Load patient data (with strict format validation)
```python
patients = load_patients("data/raw/patients.tsv")  
```

# 2. Load encounter records (auto-validate patient IDs and date formats)
```python
encounters = load_encounters("data/raw/encounters.tsv")
```
# 3. Filter adolescent encounters (ages 10-17, auto-skip invalid dates)
```python
filtered = filter_adolescents(encounters, patients)
print(f"Filtered Encounters (Age 10-17): {len(filtered)} records")
```
# 4. Load medical code mapping table
```python
mapper = MapTable.from_csv("data/mapping.csv")
```
# 5. Convert local codes to standardized group codes
```python
mapped = mapper.map_encounters(filtered)
for enc, code in mapped[:3]: 
    print(f"  {enc.localcode} → {code} | Patient: {enc.patientid} | Date: {enc.encounterdate}")
```
# 6. Generate monthly co-occurrence statistics
```python
result_df = generate_cooccurrence_table(mapped)
print("\nFinal Output Preview:")
print(result_df.head().to_string(index=False))
```
## Expected Output

```text
Patient Data Preview:
  Patient P001 | DOB: 2010-05-01
  Patient P002 | DOB: 2008-12-15  
  Patient P003 | DOB: 2006-07-20

Encounter Data Preview:
  Encounter E001 | Date: 2023-06-01 | Code: L100
  Encounter E002 | Date: 2021-04-15 | Code: L200
  Encounter E003 | Date: 2022-08-10 | Code: L300

Filtered Encounters (Age 10-17): 5 records

Mapped Encounters Preview:
  L100 → G1 | Patient: P001 | Date: 2023-06-01  
  L200 → G2 | Patient: P001 | Date: 2021-04-15
  L300 → G3 | Patient: P002 | Date: 2022-08-10

Final Output Preview:
     month patientid groupcode  count
  2023-06     P001        G1      1
  2021-04     P001        G2      1
  2022-08     P002        G3      1
  2023-01     P003        G4      1
  2020-02     P003        G5      1
```


## Local Testing Instructions for Contributors

To ensure the correctness and maintainability of the project, contributors should run tests before making changes.

### Running Unit Tests
The test cases:
- **Checking function load_patients** (`test_final_project.py`)
- **Checking function load_encounters** (`test_final_project.py`)
- **Checking function filter_adolescents** (`test_filter_adolescents.py`)
- **Checking function from_csv**(`test_map.py`)
- **Checking function map_encounters**(`test_map.py`)
- **Checking function generate_cooccurrence_table**(`test_map.py`)

To run the tests, execute:

    ```sh
    pytest tests/
    ```
