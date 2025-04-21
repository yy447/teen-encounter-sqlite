"""Final Project Functions Testing."""

import os
import tempfile
from datetime import date

import pytest

from src.load_data import Encounter, Patient, load_encounters, load_patients


def test_load_patients_tempfile() -> None:
    """Test load_encounters() function using mock TSV input files."""
    csv_content = "patientid,dob\nP001,2010-05-01\nP002,2008-12-15\n"

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp_file:
        tmp_file.write(csv_content)
        tmp_path = tmp_file.name

    try:
        patients = load_patients(tmp_path)
        assert patients == [
            Patient("P001", date(2010, 5, 1)),
            Patient("P002", date(2008, 12, 15)),
        ]
    finally:
        os.remove(tmp_path)


# 空文件
def test_load_patients_empty_file() -> None:
    """Test that an empty file raises a ValueError."""
    csv_content = "patientid,dob\n"

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp_file:
        tmp_file.write(csv_content)
        tmp_path = tmp_file.name

    try:
        with pytest.raises(ValueError, match="Input file is empty"):
            load_patients(tmp_path)
    finally:
        os.remove(tmp_path)


def test_load_patients_missing_patientid_column() -> None:
    """Test that missing 'patientid' column raises KeyError."""
    csv_content = "dob\n2010-05-01\n"

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp_file:
        tmp_file.write(csv_content)
        tmp_path = tmp_file.name

    try:
        with pytest.raises(
            KeyError, match="Missing required column: 'patientid'"
        ):
            load_patients(tmp_path)
    finally:
        os.remove(tmp_path)


def test_load_patients_empty_patientid() -> None:
    """Test that an empty patientid raises ValueError."""
    csv_content = "patientid,dob\n,2010-05-01\n"

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp_file:
        tmp_file.write(csv_content)
        tmp_path = tmp_file.name

    try:
        with pytest.raises(ValueError, match="Empty patientid found"):
            load_patients(tmp_path)
    finally:
        os.remove(tmp_path)


def test_load_patients_missing_dob_column() -> None:
    """Test that missing 'dob' column raises KeyError with patient info."""
    csv_content = "patientid\nP001\n"

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp_file:
        tmp_file.write(csv_content)
        tmp_path = tmp_file.name

    try:
        with pytest.raises(
            KeyError, match="Missing required column: 'dob' for patient P001"
        ):
            load_patients(tmp_path)
    finally:
        os.remove(tmp_path)


def test_load_patients_invalid_date_format() -> None:
    """Test that invalid date format raises ValueError with patient info."""
    csv_content = "patientid,dob\nP001,2022/01/01\n"

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp_file:
        tmp_file.write(csv_content)
        tmp_path = tmp_file.name

    try:
        with pytest.raises(
            ValueError,
            match="Invalid date format for patient P001: '2022/01/01'",
        ):
            load_patients(tmp_path)
    finally:
        os.remove(tmp_path)


def test_load_encounters_valid() -> None:
    """Test loading encounters from valid input."""
    csv_content = (
        "patientid,encounterid,encounterdate,localcode\n"
        "P001,E001,2023-06-01,L100\n"
        "P002,E002,2022-08-10,L200\n"
    )

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name

    try:
        encounters = load_encounters(tmp_path)
        assert encounters == [
            Encounter("P001", "E001", date(2023, 6, 1), "L100"),
            Encounter("P002", "E002", date(2022, 8, 10), "L200"),
        ]
    finally:
        os.remove(tmp_path)


def test_load_encounters_empty_file() -> None:
    """Test that an empty encounter file raises ValueError."""
    csv_content = "patientid,encounterid,encounterdate,localcode\n"

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name

    try:
        with pytest.raises(ValueError, match="Input file is empty"):
            load_encounters(tmp_path)
    finally:
        os.remove(tmp_path)


def test_load_encounters_missing_patientid_column() -> None:
    """Missing 'patientid' column raises KeyError."""
    csv_content = "encounterid,encounterdate,localcode\nE001,2023-06-01,L100\n"
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name
    try:
        with pytest.raises(
            KeyError, match="Missing required column: 'patientid'"
        ):
            load_encounters(tmp_path)
    finally:
        os.remove(tmp_path)


def test_load_encounters_missing_encounterid_column() -> None:
    """Missing 'encounterid' column raises KeyError."""
    csv_content = "patientid,encounterdate,localcode\nP001,2023-06-01,L100\n"
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name
    try:
        with pytest.raises(
            KeyError, match="Missing required column: 'encounterid'"
        ):
            load_encounters(tmp_path)
    finally:
        os.remove(tmp_path)


def test_load_encounters_missing_encounterdate_column() -> None:
    """Missing 'encounterdate' column raises KeyError."""
    csv_content = "patientid,encounterid,localcode\nP001,E001,L100\n"
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name
    try:
        with pytest.raises(
            KeyError, match="Missing required column: 'encounterdate'"
        ):
            load_encounters(tmp_path)
    finally:
        os.remove(tmp_path)


def test_load_encounters_empty_patientid() -> None:
    """Empty 'patientid' value raises ValueError."""
    csv_content = (
        "patientid,encounterid,encounterdate,localcode\n"
        ",E001,2023-06-01,L100\n"
    )

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name
    try:
        with pytest.raises(ValueError, match="Empty patientid found"):
            load_encounters(tmp_path)
    finally:
        os.remove(tmp_path)


def test_load_encounters_empty_encounterid() -> None:
    """Empty 'encounterid' value raises ValueError."""
    csv_content = (
        "patientid,encounterid,encounterdate,localcode\n"
        "P001,,2023-06-01,L100\n"
    )

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name
    try:
        with pytest.raises(
            ValueError, match="Empty encounterid found for patient P001"
        ):
            load_encounters(tmp_path)
    finally:
        os.remove(tmp_path)


def test_load_encounters_empty_encounterdate() -> None:
    """Empty 'encounterdate' value raises ValueError."""
    csv_content = (
        "patientid,encounterid,encounterdate,localcode\nP001,E001,,L100\n"
    )
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name
    try:
        with pytest.raises(
            ValueError,
            match="Empty encounterdate for patient P001, encounter E001",
        ):
            load_encounters(tmp_path)
    finally:
        os.remove(tmp_path)


def test_load_encounters_empty_localcode() -> None:
    """Empty 'localcode' value raises ValueError."""
    csv_content = (
        "patientid,encounterid,encounterdate,localcode\n"
        "P001,E001,2023-06-01,\n"
    )

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name
    try:
        with pytest.raises(
            ValueError,
            match="Empty localcode for patient P001, encounter E001",
        ):
            load_encounters(tmp_path)
    finally:
        os.remove(tmp_path)


def test_load_encounters_missing_localcode_column() -> None:
    """Missing 'localcode' column raises KeyError."""
    csv_content = "patientid,encounterid,encounterdate\nP001,E001,2023-06-01\n"
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name
    try:
        with pytest.raises(
            KeyError, match="Missing required column: 'localcode'"
        ):
            load_encounters(tmp_path)
    finally:
        os.remove(tmp_path)


def test_load_encounters_invalid_date_format() -> None:
    """Test that invalid date format raises ValueError."""
    csv_content = (
        "patientid,encounterid,encounterdate,localcode\n"
        "P001,E001,2023/06/01,L100\n"
    )

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name

    try:
        with pytest.raises(
            ValueError,
            match="Invalid date format for patient P001, encounter E001",
        ):
            load_encounters(tmp_path)
    finally:
        os.remove(tmp_path)
