import tkinter as tk
from tkinter import filedialog, ttk, simpledialog
import pandas as pd
import os
import openpyxl
from openpyxl import Workbook


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
        output_wb = openpyxl.load_workbook(output_file_name)
    
    output_sheet = output_wb.active
    
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
            selected_data = df.loc[start_index -4 : end_index]

            # Save the extracted data to a new Excel file
            selected_data.to_excel(output_file_name, index=False)
        else:
            print("Start and/or end tokens not found in the DataFrame.")


        """

        study_day = day_tokens[i]

        # Load the input workbook
        input_wb = openpyxl.load_workbook(input_file, data_only=True)
        input_sheet = input_wb.active

        # Initialize variables to track the section copying
        is_copying = False
        copied_rows = 0

        for row in input_sheet.iter_rows(values_only=True):
            cell_value = row[1]  # Assuming the data to copy is in column B (index 1)

            # Check if the token string is found to start copying
            if "Day" in str(cell_value) and str(study_day) in str(cell_value):
                is_copying = True
                continue

            # Check if we are in copying mode
            if is_copying:
                copied_rows += 1

                # Write the row data to the output sheet
                text_values = [str(cell) if cell is not None else "" for cell in row]
                output_sheet.append(text_values)
                

            # Check if we are done copying after encountering the token again
            if is_copying and "Day" in str(cell_value) and str(study_day) not in str(cell_value):
                is_copying = False
        i = i+1
    
        """
    
    # Save the output workbook
    #output_wb.save(output_file_name)
    print(f"Success?")


if __name__ == "__main__":
    create_window()
