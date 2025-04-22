"""Generate Test Data."""

from src.load_data import load_encounters, load_patients


def main() -> None:
    """Roughly Test the functions."""
    patients = load_patients("data_a.csv")
    encounters = load_encounters("data_b.csv")

    print(" Patients:")
    for p in patients:
        print(p)

    print("\n Encounters:")
    for e in encounters:
        print(e)


if __name__ == "__main__":
    main()
