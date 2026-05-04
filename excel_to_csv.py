import os
import pandas as pd


path = r"D:\Year 2026\Report Mr. Tree\DATA"

allexcelfile = [i for i in os.listdir(path) if i.endswith(".xlsx")]
complete = 0
for i in allexcelfile:
    
    join = os.path.join(path,i)
    newfile = pd.read_excel(join)
    newpath = i.replace(".xlsx",".csv")

    newcsv = newfile.to_csv(f"D:\Year 2026\DATA-CSV\{newpath}")
    complete += 1
    print(f"Convert Excel to CSV {complete} Completed")