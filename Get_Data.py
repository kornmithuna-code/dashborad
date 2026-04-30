import os
import pandas as pd

path_folder = r"D:\Year 2026\DATA-CSV"

# Select Specific columns
usecolumns=["CustomerID","CustomerName","Date","SalesmanID","Salesman","Phone","Market"
            ,"Commune","District","Province","ItemName","QtyCtn","QtyCtnFOC","AmountUSD","CustomerType"
            ,"YYYY","MM","DAY","Channel","Route","SupplierID","ProductCat","ItemCode","SaleType"
            ,"InvoiceNo","TakeStock","Source","IssueBy","ExpireDate","SizeGroupID","CompanyID"]

# Read Data

get_file = os.listdir(path_folder)

get_file = [ file for file in get_file if file.endswith(".csv")]

raw_data = []

for file in get_file:
    filename = os.path.join(path_folder,file)
    data = pd.read_csv(filename,dtype="str")

    raw_data.append(data)
    print("Complete")

raw_data = pd.concat(raw_data)

raw_data = pd.DataFrame(raw_data)
# raw_data.to_csv(r"D:\Year 2026\dataa.csv")
# print(raw_data)




    
   