import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import simpledialog
import pandas as pd
import os
import shutil

def open_file_dialog():
    file_paths = filedialog.askopenfilenames(filetypes=[("All Files", "*.*")])
    for file_path in file_paths:
        file_name = file_path.split("/")[-1]  # Get only the filename from the path

        # Prompt the user to enter the day number using a dialog box
        day = simpledialog.askinteger("Enter Day", f"Enter the day for '{file_name}':")

        # Add the file name and the entered number to the table
        file_table.insert("", "end", values=(file_name, day))

def create_window():
    root = tk.Tk()
    root.title("Study Schedule Selection")
    root.geometry("500x300")  # Set the initial size of the window (width x height)

    file_select_button = tk.Button(root, text="Select Schedule", command=open_file_dialog)
    file_select_button.pack(pady=10)

    global file_table
    columns = ("File Name", "Day")
    file_table = ttk.Treeview(root, columns=columns, show="headings", selectmode="browse")

    # Set column headings
    for col in columns:
        file_table.heading(col, text=col)
        file_table.column(col, width=150, anchor="center")

    file_table.pack(pady=5)

    root.mainloop()


def extract_section(file_path, sheet_name, start_row, end_row):
    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=start_row-1, nrows=end_row-start_row+1)
    return df

def combine_sections(directory, sheet_name, start_row, end_row):
    combined_df = pd.DataFrame()

    for file in os.listdir(directory):
        if file.endswith(".xlsx"):  # Assuming all files are Excel files
            file_path = os.path.join(directory, file)
            section_df = extract_section(file_path, sheet_name, start_row, end_row)
            combined_df = pd.concat([combined_df, section_df])

    return combined_df

if __name__ == "__main__":
    create_window()
