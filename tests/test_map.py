"""Test Function 3 and Function 4 independently."""

import os
import tempfile
from datetime import date

import pandas as pd
import pytest

from load_data import Encounter
from map_groupcode import (
    MapTable,
    generate_cooccurrence_table,
)


def test_map_table_from_csv() -> None:
    """Test Function 3:test_map_table_from_csv."""
    mapping_csv = "localcode,groupcode\nL001,G01\nL002,G02\n"
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp:
        tmp.write(mapping_csv)
        tmp_path = tmp.name

    try:
        table = MapTable.from_csv(tmp_path)
        assert table.mapping["L001"] == "G01"
    finally:
        os.remove(tmp_path)


def test_map_table_from_csv_missing_columns() -> None:
    """Test that missing 'localcode' or 'groupcode' raise ValueError."""
    invalid_csv = "wrongcol,anothercol\nA,B\nC,D\n"
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp:
        tmp.write(invalid_csv)
        tmp_path = tmp.name

    try:
        with pytest.raises(
            ValueError,
            match="Mapping file must contain 'localcode' and 'groupcode'",
        ):
            MapTable.from_csv(tmp_path)
    finally:
        os.remove(tmp_path)


def test_map_table_from_csv_empty_file() -> None:
    """Test that empty file raises ValueError."""
    empty_csv = "localcode,groupcode\n"  # header only, no data
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp:
        tmp.write(empty_csv)
        tmp_path = tmp.name

    try:
        table = MapTable.from_csv(tmp_path)
        assert table.mapping == {}
    finally:
        os.remove(tmp_path)


def test_function3_map_encounters_independent() -> None:
    """Test Function 3: Map localcodes to groupcodes."""
    mapping_csv = "localcode,groupcode\nL100,G1\nL200,G2\n"

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp:
        tmp.write(mapping_csv)
        tmp_path = tmp.name

    try:
        encounters = [
            Encounter("P001", "E001", date(2023, 6, 1), "L100"),
            Encounter("P002", "E002", date(2023, 6, 2), "L200"),
            Encounter("P003", "E003", date(2023, 6, 3), "L999"),  # not in map
        ]

        maptable = MapTable.from_csv(tmp_path)
        mapped = maptable.map_encounters(encounters)

        assert len(mapped) == 2
        assert mapped[0][0].encounterid == "E001" and mapped[0][1] == "G1"
        assert mapped[1][0].encounterid == "E002" and mapped[1][1] == "G2"

    finally:
        os.remove(tmp_path)


def test_function4_generate_cooccurrence_table_independent() -> None:
    """Test Function 4: Generate monthly co-occurrence table."""
    enc1 = Encounter("P001", "E001", date(2023, 6, 1), "L100")
    enc2 = Encounter("P001", "E002", date(2023, 6, 10), "L100")
    enc3 = Encounter("P002", "E003", date(2023, 7, 15), "L200")

    mapped = [(enc1, "G1"), (enc2, "G1"), (enc3, "G2")]

    co_df = generate_cooccurrence_table(mapped)

    assert isinstance(co_df, pd.DataFrame)
    assert set(co_df.columns) == {"month", "patientid", "groupcode", "count"}

    assert co_df.shape[0] == 2

    row1 = co_df.loc[
        (co_df["patientid"] == "P001") & (co_df["groupcode"] == "G1")
    ]
    assert row1.iloc[0]["count"] == 2
    assert row1.iloc[0]["month"] == "2023-06"

    row2 = co_df.loc[
        (co_df["patientid"] == "P002") & (co_df["groupcode"] == "G2")
    ]
    assert row2.iloc[0]["count"] == 1
    assert row2.iloc[0]["month"] == "2023-07"


def test_generate_cooccurrence_table_empty_input() -> None:
    """Test that empty input returns empty DataFrame."""
    result = generate_cooccurrence_table([])
    assert isinstance(result, pd.DataFrame)
    assert result.empty
    assert list(result.columns) == ["month", "patientid", "groupcode", "count"]


def test_map_table_from_csv_duplicate_localcode() -> None:
    """Test that duplicate localcodes keep the last mapping."""
    mapping_csv = "localcode,groupcode\nL001,G1\nL001,G2\n"
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".csv"
    ) as tmp:
        tmp.write(mapping_csv)
        tmp_path = tmp.name

    try:
        table = MapTable.from_csv(tmp_path)
        assert table.mapping["L001"] == "G2"
        assert len(table.mapping) == 1
    finally:
        os.remove(tmp_path)


def test_generate_cooccurrence_table_multiple_groupcodes_same_patient() -> (
    None
):
    """Test that different groupcodes for the same patient/month."""
    enc1 = Encounter("P001", "E001", date(2023, 6, 1), "L100")
    enc2 = Encounter("P001", "E002", date(2023, 6, 2), "L200")
    enc3 = Encounter("P001", "E003", date(2023, 6, 3), "L100")

    mapped = [(enc1, "G1"), (enc2, "G2"), (enc3, "G1")]

    co_df = generate_cooccurrence_table(mapped)

    assert co_df.shape[0] == 2

    row_g1 = co_df.loc[
        (co_df["patientid"] == "P001") & (co_df["groupcode"] == "G1")
    ]
    row_g2 = co_df.loc[
        (co_df["patientid"] == "P001") & (co_df["groupcode"] == "G2")
    ]

    assert row_g1.iloc[0]["count"] == 2
    assert row_g1.iloc[0]["month"] == "2023-06"

    assert row_g2.iloc[0]["count"] == 1
    assert row_g2.iloc[0]["month"] == "2023-06"
