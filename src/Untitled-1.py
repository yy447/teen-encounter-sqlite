"""Load Data."""

import csv
from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Patient:
    """Class representing a patient."""

    patientid: str
    dob: date

    @staticmethod
    def from_row(row: dict) -> "Patient":
        """Create a Patient instance from a CSV row."""
        dob_str = row["dob"]
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        return Patient(patientid=row["patientid"], dob=dob)


@dataclass
class Encounter:
    """Class representing an encounter."""

    patientid: str
    encounterid: str
    encounterdate: date
    localcode: str

    @staticmethod
    def from_row(row: dict) -> "Encounter":
        """Create an Encounter instance from a CSV row."""
        encounterdate_str = row["encounterdate"]
        encounterdate = datetime.strptime(encounterdate_str, "%Y-%m-%d").date()
        return Encounter(
            patientid=row["patientid"],
            encounterid=row["encounterid"],
            encounterdate=encounterdate,
            localcode=row["localcode"],
        )


class DataLoader:
    """Class for loading patient and encounter data from CSV files."""

    def __init__(self, path_a: str, path_b: str):
        self.path_a = path_a  # CSV for Patient
        self.path_b = path_b  # CSV for Encounter

    def load_patients(self) -> List[Patient]:
        """Load patient data from file and return a list of Patient objects."""
        patients = []
        with open(self.path_a, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                patients.append(Patient.from_row(row))
        return patients

    def load_encounters(self) -> List[Encounter]:
        """Load encounter data from file and return a list of Encounter objects."""
        encounters = []
        with open(self.path_b, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                encounters.append(Encounter.from_row(row))
        return encounters
