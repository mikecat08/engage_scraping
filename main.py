import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import datetime
import os
import pandas as pd
import openpyxl

driver = webdriver.Chrome('./driver/chromedriver')

driver.get('https://en-gage.net/user/#/')
time.sleep(1)

area_btn = driver.find_element_by_link_text("選択")
area_btn.click()
time.sleep(1)

kanto_btn = driver.find_element_by_link_text("関東")
kanto_btn.click()
time.sleep(1)

tokyo_btn = driver.find_element_by_link_text("東京都")
tokyo_btn.click()
time.sleep(1)

shibuya_btn = driver.find_element_by_link_text("渋谷区")
shibuya_btn.click()
time.sleep(1)

option_btn = driver.find_element_by_link_text("職種、給与など、こだわりは？")
option_btn.click()
time.sleep(1)

checkbox_ce3 = driver.find_element_by_xpath("//label[@for='ce_3']")
checkbox_ce3.click()

checkbox_ce5 = driver.find_element_by_xpath("//label[@for='ce_5']")
checkbox_ce5.click()

checkbox_ce7 = driver.find_element_by_xpath("//label[@for='ce_7']")
checkbox_ce7.click()

occupation_btn = driver.find_element_by_link_text("選択してください")
occupation_btn.click()
time.sleep(1)

# occupation_accordion_next = driver.find_element_by_xpath("//div[@class='md_accordion'][8]")
occupation_accordion = driver.find_element_by_xpath("//div[@class='md_accordion'][7]")
# occupation_accordion_next.click()
occupation_accordion.click()

checkbox_p_401000 = driver.find_element_by_xpath("//label[@for='p_401000']")
checkbox_p_401000.click()

checkbox_p_402000 = driver.find_element_by_xpath("//label[@for='p_402000']")
checkbox_p_402000.click()

# checkbox_p_409000 = driver.find_element_by_xpath("//label[@for='p_409000']")
# checkbox_p_409000.click()

search_btn = driver.find_element_by_link_text("選択")
search_btn.click()
time.sleep(1)

search_btn = driver.find_element_by_link_text("この条件で探す")
search_btn.click()
time.sleep(1)

# スクレイピング結果を書き出すcsvの用意
csv_date = datetime.datetime.today().strftime("%Y%m%d%H%M")
csv_file_name = 'engage' + csv_date + '.csv'

# ファイルの閉じ忘れが怖いのでwithで開く
with open(csv_file_name, 'w', encoding='cp932', errors='ignore') as f:
  writer = csv.writer(f, lineterminator='\n')
  csv_header = ["検索順位", "求人タイトル", "URL"]
  writer.writerow(csv_header)

  # 検索順位の定義
  item = 1

  # 求人のタイトルをすべて取得する
  for elem_ttl in driver.find_elements_by_xpath("//a[@class='headArea']/div[@class='catch']"):
      elem_a = elem_ttl.find_element_by_xpath('..')
      csvlist = []
      csvlist.append(str(item))
      csvlist.append(elem_ttl.text)
      csvlist.append(elem_a.get_attribute('href'))
      writer.writerow(csvlist)
      item = item + 1

print ('csvファイルを作成しました。')

# 作成したcsvファイルをpandasで読み込み
df = pd.read_csv(csv_file_name, encoding="Shift-JIS")

# デスクトップへのパスを取得
desktop_path = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop"

# デスクトップにresultというフォルダを作成
dir = desktop_path + '\\' + 'result'
os.makedirs(dir, exist_ok=True)

# xlsxファイルをデスクトップのresultフォルダに書き出し
xlsx_file_name = 'engage' + csv_date + '.xlsx'
df.to_excel(dir + '//' + xlsx_file_name)
print ('xlsxファイルを作成しました。')

# csvファイルはもう使わないので削除
os.remove(csv_file_name)
print ('csvファイルを削除しました。')

# ブラウザを閉じる
driver.close()



