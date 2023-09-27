import requests
import json
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import datetime
import time
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')  # 啟動Headless 無頭
options.add_argument('--disable-gpu') #關閉GPU 避免某些系統或是網頁出錯

total = []
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.implicitly_wait(10)



def date_range(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates
 
date_list_str=date_range("2020-01-22","2023-03-15")

for i in range (len(date_list_str)):
    driver.get("https://covid-19.nchc.org.tw/city_confirmed.php?mycity=%E5%85%A8%E9%83%A8%E7%B8%A3%E5%B8%82")
    soup = BeautifulSoup(driver.page_source, "lxml")
    element1 = driver.find_element(By.XPATH, '//*[@id="myTable03_wrapper"]/div[4]/div[3]/div/table/tfoot/tr/th[1]/input')
    element1.click()
    element1.clear()    
    element1.send_keys(date_list_str[i])

    element2 = driver.find_element(By.XPATH, '//*[@id="myTable03_wrapper"]/div[4]/div[3]/div/table/tfoot/tr/th[3]/input')
    element2.click()
    element2.clear()   
    element2.send_keys("全區")
    
    time.sleep(2)
    
    Now_page_src = driver.page_source
    tag_tbody = driver.find_element(By.XPATH, '/html/body/div[3]/section/div[4]/div/div[4]/div[2]/table/tbody')
    Now_page_src = tag_tbody
    #print(tag_tbody.text)
    
    list1 = tag_tbody.text.split()
    
    list2 = [date_list_str[i]]
    #print(list2)
    initial = {"南投縣":0,"台中市":0,"台北市":0,"台南市":0,"台東縣":0,"嘉義市":0,"嘉義縣":0,"基隆市":0,"境外移入":0,"宜蘭縣":0,"屏東縣":0,"彰化縣":0,"新北市":0,"新竹市":0,"新竹縣":0,"桃園市":0,"澎湖縣":0,"花蓮縣":0,"苗栗縣":0,"連江縣":0,"金門縣":0,"雲林縣":0,"高雄市":0}
    #blank = [date_list_str[i],"","","","","","","","","","","","","","","","","","","","","","",""]
    ifblank= 0
    for i in range(0, len(list1), 5):
        initial[list1[i+1]] = list1[i+3]
    #print(initial)
    for keys,values in initial.items():
        if(initial[keys]=="found"):
            ifblank= 1
        elif(initial[keys]!="found"):
            list2.append(initial[keys])
    
    if(ifblank==0):
        print(list2)
        total += [list2]
    

csvfile = "covid_19 data1.csv"
with open(csvfile, 'w+', newline='') as fp:
    writer = csv.writer(fp)
    writer.writerow(["日期","南投縣","台中市","台北市","台南市","台東縣","嘉義市","嘉義縣","基隆市","境外移入","宜蘭縣","屏東縣","彰化縣","新北市","新竹市","新竹縣","桃園市","澎湖縣","花蓮縣","苗栗縣","連江縣","金門縣","雲林縣","高雄市"])
    for row in total:
        writer.writerow(row)

driver.quit()

