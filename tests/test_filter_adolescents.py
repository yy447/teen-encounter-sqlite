"""Test filter_adolescents()."""

from datetime import date

import pytest

from filter_adolescents import filter_adolescents
from load_data import Encounter, Patient


def test_patientid_not_found_error() -> None:
    """Test that a ValueError is raised when patientid is missing."""
    patients = [Patient("P001", date(2010, 5, 1))]
    encounters = [
        Encounter("P999", "E001", date(2024, 5, 1), "L100")  # Not in patients
    ]

    with pytest.raises(ValueError, match="patientid 'P999' not found"):
        filter_adolescents(encounters, patients)


def test_encounter_before_birth_error() -> None:
    """Test that a ValueError is raised when encounter is before birthdate."""
    patients = [Patient("P001", date(2010, 5, 1))]
    encounters = [
        Encounter("P001", "E001", date(2008, 1, 1), "L100")  # Before birth
    ]

    with pytest.raises(ValueError, match="is before birthdate"):
        filter_adolescents(encounters, patients)
