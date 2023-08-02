import tkinter as tk
from tkinter import filedialog, ttk, simpledialog
import pandas as pd
import os
import openpyxl
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import NamedStyle
import datetime


input_file_paths = []
input_schedule_days = []


def create_window():
    root = tk.Tk()
    root.title("Study Schedule Selection")
    root.geometry("500x400")  # Set the initial size of the window (width x height)

    file_select_button = tk.Button(root, text="Select Schedule", command=open_file_dialog)
    file_select_button.pack(pady=10)

    global file_table
    columns = ("Study Schedule", "Day")
    file_table = ttk.Treeview(root, columns=columns, show="headings", selectmode="browse")

    # Set column headings
    for col in columns:
        file_table.heading(col, text=col)
        file_table.column(col, width=150, anchor="center")

    file_table.pack(pady=5)

    generate_schedule_button = tk.Button(root, text="Generate Schedules", command=output_directory_dialog)
    generate_schedule_button.pack(pady=10)

    root.mainloop()


def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    input_file_paths.append(file_path)

    file_name = file_path.split("/")[-1]  # Get only the filename from the path

    # Prompt the user to enter the day number using a dialog box
    day = simpledialog.askinteger("Enter Day", f"Enter the day for '{file_name}':")
    input_schedule_days.append(day)

    # Add the file name and the entered number to the table
    file_table.insert("", "end", values=(file_name, day))


def output_directory_dialog():
    output_file_path = filedialog.askdirectory()
    copy_schedule_days(input_file_paths, output_file_path, input_schedule_days)


# Function to find rows containing the tokens
def find_token_row_index(token, df):
    return df[df.apply(lambda row: row.astype(str).str.contains(token, case=False).any(), axis=1)].index


def copy_schedule_days(input_files, output_file, day_tokens):
    # Create a new workbook for the output if it doesn't exist
    output_file_name = os.path.join(output_file, "Daily_Schedules.xlsx")
    if not os.path.exists(output_file_name):
        output_wb = Workbook()
        output_wb.save(output_file_name)
    else:
        output_wb = openpyxl.load_workbook(output_file_name, values_only=True)
    
    i = 0

    for input_file in input_files:

        df = pd.read_excel(input_file)

        start_token = "Day " + str(input_schedule_days[i])
        end_token = "Workbook"

        start_index = find_token_row_index(start_token, df)
        end_index = find_token_row_index(end_token, df)

        if not start_index.empty and not end_index.empty:
            start_index = start_index[0]
            
            # Find the first occurrence of the ending token after the start token
            end_index = end_index[end_index > start_index][0]

            # Extract the section of data between the tokens (excluding the tokens themselves)
            selected_data = df.loc[start_index - 4: end_index, df.columns != df.columns[0]]  # Exclude the first column from being copied

            # Get the selected sheet to copy data
            sheet = output_wb.active

            # Append the new data to the end of the sheet
            for row in dataframe_to_rows(selected_data, index=False, header=False):
                sheet.append(row)

            # Define a custom style for datetime values
            time_style = NamedStyle(name="time_style", number_format="hh:mm")

            # Formatting date time
            for row in sheet.iter_rows(min_row=sheet.max_row - len(selected_data) + 1, max_row=sheet.max_row):
                for cell in row:
                    source_cell = df.iloc[cell.row - sheet.max_row + len(selected_data) - 1, cell.column - 1]

                     # Check if the value is a datetime object and apply the custom style
                    if isinstance(source_cell, pd.Timestamp):
                        cell.style = time_style

            # Preserve column width
            for column_cells in sheet.columns:
                length = max(len(str(cell.value)) for cell in column_cells)
                sheet.column_dimensions[column_cells[0].column_letter].width = length + 2  # Additional padding

            output_wb.save(output_file_name)

        else:
            print("Day not found in study schedule")

    print(f"Success?")


if __name__ == "__main__":
    create_window()
