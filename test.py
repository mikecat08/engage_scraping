import os
import pandas as pd
import openpyxl

desktop_path = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop"

print (desktop_path)

df = pd.read_csv("engage202212261907.csv", encoding="Shift-JIS")
df.to_excel("test.xlsx")