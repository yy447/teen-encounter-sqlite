"""Load Data."""

import csv
from datetime import date, datetime


class Patient:
    """Represents a patient with ID and date of birth."""

    def __init__(self, patientid: str, dob: date):
        """Initialize a Patient instance with patientid and dob."""
        self.patientid = patientid
        self.dob = dob

    def __repr__(self) -> str:
        """Manage the output."""
        return (
            f"Patient(patientid='{self.patientid}', "
            f"dob={self.dob.isoformat()})"
        )

    def __eq__(self, other: object) -> bool:
        """Use for test."""
        return (
            isinstance(other, Patient)
            and self.patientid == other.patientid
            and self.dob == other.dob
        )


class Encounter:
    """Represents a medical encounter with a local code."""

    def __init__(
        self,
        patientid: str,
        encounterid: str,
        encounterdate: date,
        localcode: str,
    ):
        """Initialize a Encounter instance."""
        self.patientid = patientid
        self.encounterid = encounterid
        self.encounterdate = encounterdate
        self.localcode = localcode

    def __repr__(self) -> str:
        """Manage the output."""
        return (
            f"Encounter(patientid='{self.patientid}', "
            f"encounterid='{self.encounterid}', "
            f"encounterdate={self.encounterdate.isoformat()}, "
            f"localcode='{self.localcode}')"
        )

    def __eq__(self, other: object) -> bool:
        """Use for test."""
        return (
            isinstance(other, Encounter)
            and self.patientid == other.patientid
            and self.encounterid == other.encounterid
            and self.encounterdate == other.encounterdate
            and self.localcode == other.localcode
        )


def load_patients(path: str) -> list[Patient]:
    """Load patients from a CSV file."""
    patients = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        if not rows:
            raise ValueError(
                "Input file is empty or contains no patient records."
            )

        for row in rows:
            if "patientid" not in row:
                raise KeyError("Missing required column: 'patientid'")

            pid = row["patientid"]

            # Empty patientid
            if not pid.strip():
                raise ValueError("Empty patientid found in data row")

            # Lack of dob
            try:
                dob_str = row["dob"]
            except KeyError as e:
                raise KeyError(
                    f"Missing required column: 'dob' for patient {pid}"
                ) from e

            # Invalid Date Format
            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError as e:
                raise ValueError(
                    f"Invalid date format for patient {pid}: '{dob_str}' "
                ) from e
            patient = Patient(patientid=pid, dob=dob)
            patients.append(patient)
    return patients


def load_encounters(path: str) -> list[Encounter]:
    """Load encounter data from a CSV file."""
    encounters = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        if not rows:
            raise ValueError(
                "Input file is empty or contains no encounter records."
            )

        for row in rows:
            # Check required columns
            for col in [
                "patientid",
                "encounterid",
                "encounterdate",
                "localcode",
            ]:
                if col not in row:
                    raise KeyError(f"Missing required column: '{col}'")

            pid = row["patientid"]
            eid = row["encounterid"]
            edate_str = row["encounterdate"]
            code = row["localcode"]

            # Check for empty fields
            if not pid.strip():
                raise ValueError("Empty patientid found in data row.")
            if not eid.strip():
                raise ValueError(f"Empty encounterid found for patient {pid}.")
            if not edate_str.strip():
                raise ValueError(
                    f"Empty encounterdate for patient {pid}, encounter {eid}."
                )
            if not code.strip():
                raise ValueError(
                    f"Empty localcode for patient {pid}, encounter {eid}."
                )

            # Parse date
            try:
                edate = datetime.strptime(edate_str, "%Y-%m-%d").date()
            except ValueError as e:
                raise ValueError(
                    f"Invalid date format for patient {pid}, encounter {eid}: "
                    f"'{edate_str}' (expected YYYY-MM-DD)"
                ) from e

            encounter = Encounter(
                patientid=pid,
                encounterid=eid,
                encounterdate=edate,
                localcode=code,
            )
            encounters.append(encounter)
    return encounters


if __name__ == "__main__":
    pass
