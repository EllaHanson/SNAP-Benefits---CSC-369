import pandas as pd
import os

pd.set_option("display.max_rows", None)  # show all rows

input_dir = "./dirty_data"
output_dir = "./csv_data"
os.makedirs(output_dir, exist_ok=True)

dir_files = glob.glob(os.path.join(input_dir, "*.xls"))

sheet_dict = pd.read_excel(input_f, sheet_name=None, engine="xlrd")

data = sheet_dict["NERO"]
sheets_df = []

for name, data in sheet_dict.items():
    data = data.reset_index(drop=True)
    data.insert(0, "SheetName", name)
    sheets_df.append(data)

tot_file = pd.concat(sheets_df)
tot_file.to_csv(output_f, index=False)
