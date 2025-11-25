import pandas as pd
import os
import glob

pd.set_option("display.max_rows", None)  # show all rows

input_dir = "./dirty_data"
output_dir = "./csv_data/snap_data.csv"
os.makedirs("./csv_data", exist_ok=True)

excel_files = glob.glob(os.path.join(input_dir, "**", "*.xls*"), recursive=True)
all_dfs = []

for file in excel_files:
    file_name = os.path.splitext(os.path.basename(file))[0]

    if file.endswith(".xlsx"):
        csv_dict = pd.read_excel(file, sheet_name=None, engine="openpyxl")
    else:
        csv_dict = pd.read_excel(file, sheet_name=None, engine="xlrd")

    for sheet_name, df in csv_dict.items():
        df = df.reset_index(drop=True)
        df.insert(0, "SheetName", sheet_name)
        df.insert(0, "FileName", file_name)
        all_dfs.append(df)

complete_df = pd.concat(all_dfs, ignore_index=True)
complete_df.to_csv(output_dir, index=False)
