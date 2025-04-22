"""Filter a specific cohort."""

from collections.abc import Iterator
from datetime import date

from src.load_data import Encounter, Patient


class FilteredEncounterData:
    """Storing filtered Encounter objectsrepresenting patients (age 10–17)."""

    def __init__(self, encounters: list[Encounter]) -> None:
        """Initialize."""
        self.encounters = encounters

    def __len__(self) -> int:
        """Return the number of filtered encounters."""
        return len(self.encounters)

    def __getitem__(self, idx: int) -> Encounter:
        """Allow indexing to retrieve individual Encounter objects."""
        return self.encounters[idx]

    def get_unique_patients(self) -> set[str]:
        """Return a set of unique patient IDs from the filtered encounters."""
        return {e.patientid for e in self.encounters}

    def get_all_encounter_dates(self) -> list[date]:
        """Return a list of encounter dates from the filtered data."""
        return [e.encounterdate for e in self.encounters]

    def __iter__(self) -> Iterator[Encounter]:
        """Allow iteration over encounters."""
        return iter(self.encounters)


def filter_adolescents(
    encounters: list[Encounter], patients: list[Patient]
) -> FilteredEncounterData:
    """Filter encounters to include specific encounter."""

    def calculate_age(dob: date, encounter_date: date) -> int:
        """Calculate age at encounter time."""
        return (
            encounter_date.year
            - dob.year
            - (
                (encounter_date.month, encounter_date.day)
                < (dob.month, dob.day)
            )
        )

    patient_lookup = {p.patientid: p.dob for p in patients}
    filtered = []

    for e in encounters:
        dob = patient_lookup.get(e.patientid)
        if dob is None:
            raise ValueError(
                f"Encounter patientid '{e.patientid}' not found in patient list."
            )

        if e.encounterdate < dob:
            raise ValueError(
                f"Encounter date {e.encounterdate} is before birthdate {dob} "
                f"for patient {e.patientid}."
            )

        age = calculate_age(dob, e.encounterdate)
        if 10 <= age <= 17:
            filtered.append(e)

    return FilteredEncounterData(filtered)
