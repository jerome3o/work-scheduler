import tkinter as tk
import pandas as pd
import os
import openpyxl
import json
from tkinter import filedialog, ttk, simpledialog
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import NamedStyle
from datetime import time
from models import TaskType

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
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    input_file_paths.append(file_path)

    file_name = file_path.split("/")[-1]  # Get only the filename from the path

    # Prompt the user to enter the day number using a dialog box
    day = simpledialog.askinteger("Enter Day", f"Enter the day for '{file_name}':")
    input_schedule_days.append(day)

    # Add the file name and the entered number to the table
    file_table.insert("", "end", values=(file_name, day))


def output_directory_dialog():
    output_file_path = filedialog.askdirectory()
    copy_schedule_days(input_file_paths, output_file_path)


def find_token_row_index(token, df):
    return df[df.apply(lambda row: row.astype(str).str.contains(token, case=False).any(), axis=1)].index


def append_empty_rows(sheet, num_rows):
    for _ in range(num_rows):
        empty_row = [None] * sheet.max_column
        sheet.append(empty_row)


def copy_schedule_days(input_files, output_file_directory):
    # Create a new workbook for the output if it doesn't exist
    output_file_name = os.path.join(output_file_directory, "Daily_Schedules.xlsx")
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
            time_style = NamedStyle(name="time_style", number_format="HH:MM")

            # Formatting date time
            for row in sheet.iter_rows(min_row=sheet.max_row - len(selected_data) + 1, max_row=sheet.max_row):
                for cell in row:
                    source_cell = df.iloc[cell.row - sheet.max_row + len(selected_data) - 1, cell.column - 1]

                     # Check if the value is a datetime object and apply the custom style
                    if isinstance(source_cell, pd.Timestamp):
                        cell.style = time_style
                    
                    #preserve the row height
                    sheet.row_dimensions[cell.row].height = sheet.row_dimensions[cell.row - sheet.max_row + len(selected_data)].height

            # Preserve column width
            for column_cells in sheet.columns:
                length = max(len(str(cell.value)) for cell in column_cells)
                sheet.column_dimensions[column_cells[0].column_letter].width = length + 2  # Additional padding

            output_wb.save(output_file_name)

        else:
            print("Day not found in study schedule")
        
        append_empty_rows(sheet, 4)

        i=i+1

        print(f"Successfully created Daily_schedules.xslx")

        excel_to_json(output_file_name, output_file_directory)


def assign_category(task_name):
    # Enumerate task names based on keywords

    doctor = ["EXAM", "EXAMINATION", "PHYSICAL", "DOCTOR", "ELIGIBILITY"]
    nurse = ["DOSE", "PREDOSE", "AE", "ADVERSE", "MEDICATION", "ASSESS", "SITE", "ACCOUNTABILITY", "DISPENSE", "REPORTED", "INFUSION", "MONITOR"]
    crt = ["BREAKFAST", "LUNCH", "DINNER", "SNACK", "SUPINE", "ECG", "VITAL", "VITALS", "ASSESSMENT", "COMMENCE", "BLOCK", "PREG", "DOA", "URINALYSIS", "URINE", "MSU", "WEIGHT", "BMI", "ALCOHOL", "CLEAN", "LINEN", "WALK"]
    any = ["ADMIT", "WRIST", "WRISTBAND", "COMPLIANCE", "REMIND", "ENSURE", "RULES", "TOUR", "WORKBOOK", "DISCHARGE", "ENCOURAGE", "ORIENTATION", "RESTRICTIONS"]
    phlebotomy = ["CANNULA", "CANNULATION", "BLOOD", "SAFETIES", "FLUSH"]
    spiro = ["SPIROMETRY"]
    sputum = ["SPUTUM"]
    triplicate = ["TRIPLICATE"]
    phone = ["PHONE"]
    pharmacy = ["RANDOMISATION"]
    date = ["DATE"]

    assign_tasks = {'doctor' : doctor, 'nurse' : nurse, 'crt' : crt, 'any' : any, 'phlebotomy' : phlebotomy, 'spiro' : spiro, 'sputum' : sputum, 'triplicate' : triplicate, 'phone' : phone, 'pharmacy' : pharmacy, 'date' : date}

    task_type = "OTHER"

    for assignment in assign_tasks:
        for keyword in assign_tasks[assignment]:
            if keyword in str.upper(task_name):
                task_type = str.upper(assignment)
    
    #print(f"CATEGORY found for '{task_name}': {task_type}")
    
    return task_type


def time_to_str(t):
    # Convert time object to a string in HH:MM format
    return t.strftime('%H:%M') if isinstance(t, time) else str(t)


def excel_to_json(schedules, json_file_directory):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(schedules)
    
    # Create a dictionary to store tasks by category
    data = {}

    current_category = None
    current_study = None
    
    for row in df.itertuples(index=False, name=None):
        task = str(row[0])  # Access the first element of the tuple as the task name
        
        if task == "nan" or task.strip() == '':
            continue

        #print(task)

        times = [time_to_str(t) for t in row[1:] if pd.notna(t)]  # Convert times to strings

        category = assign_category(task)

        # Skip adding to data if all times are "nan"
        if not times:
            continue
        
        # Create an instance of the appropriate Enum class based on the category
        if category not in data:
            data[category] = {}
        data[category][task] = times

    # Convert Enum keys to strings before writing to JSON
    json_data = {str(key): value for key, value in data.items()}

    json_file_path = os.path.join(json_file_directory, "JSON_schedules")

    # Create the JSON file and write the dictionary into it
    with open(json_file_path, 'w') as f:
        json.dump(json_data, f, indent=4)


if __name__ == "__main__":
    create_window()
