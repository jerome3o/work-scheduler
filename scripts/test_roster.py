from src.ui.excel_loader import get_staff_shifts

def main():
    get_staff_shifts(
        roster_path="data\Duty Roster 07 Aug - 20 Aug 2023.xlsx",
        day="MON 07 AUG",
    )

if __name__ == "__main__":
    main()