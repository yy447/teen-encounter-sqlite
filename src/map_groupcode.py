"""Load Data."""

import pandas as pd

from load_data import Encounter


class MapTable:
    """Mapping from localcode to groupcode."""

    def __init__(self, mapping: dict[str, str]):
        """Initialize maptable."""
        self.mapping = mapping

    @classmethod
    def from_csv(cls, path: str) -> "MapTable":
        """Load map table."""
        df = pd.read_csv(path)
        if "localcode" not in df.columns or "groupcode" not in df.columns:
            raise ValueError(
                "Mapping file must contain 'localcode' and 'groupcode'"
            )
        mapping = dict(zip(df["localcode"], df["groupcode"]))
        return cls(mapping)

    def map_encounters(
        self, encounters: list[Encounter]
    ) -> list[tuple[Encounter, str]]:
        """Return encounters with groupcodes as (Encounter, groupcode)."""
        results = []
        for enc in encounters:
            groupcode = self.mapping.get(enc.localcode)
            if groupcode:
                results.append((enc, groupcode))
        return results


def generate_cooccurrence_table(
    mapped_encounters: list[tuple[Encounter, str]],
) -> pd.DataFrame:
    """Generate monthly groupcode counts from mapped encounters."""
    records = []
    for enc, groupcode in mapped_encounters:
        month = enc.encounterdate.strftime("%Y-%m")
        records.append((month, enc.patientid, groupcode))

    df = pd.DataFrame(records, columns=["month", "patientid", "groupcode"])
    cooccur_df = (
        df.groupby(["month", "patientid", "groupcode"])
        .size()
        .reset_index(name="count")
    )
    return cooccur_df


if __name__ == "__main__":
    pass
