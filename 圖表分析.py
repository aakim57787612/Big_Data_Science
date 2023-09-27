import csv
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
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

driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.implicitly_wait(10)

sns.set_style("whitegrid",{"font.sans-serif":['Microsoft JhengHei']})

arr=["南投縣","臺中市","臺北市","臺南市","臺東縣","嘉義市","嘉義縣","基隆市","境外移入","宜蘭縣","屏東縣","彰化縣","新北市","新竹市","新竹縣","桃園市","澎湖縣","花蓮縣","苗栗縣","連江縣","金門縣","雲林縣","高雄市"]

max_num=[]
all_total=[]
date=[]
max_date = '2020/1/22'
max_total = 0
x_date=['2020/1/22','2020/7/3','2021/1/1','2021/6/26','2022/1/1','2022/2/1',
     '2022/3/1','2022/4/1','2022/5/1','2022/6/1','2022/7/1','2022/8/1','2022/9/1','2022/10/1'
     ,'2022/11/1','2022/12/1','2023/1/1','2023/2/1','2023/3/1']

for row in csv.DictReader(open('covid_19 data.csv', 'r',encoding="utf-8")):
    date.append(row['\ufeff日期'])
    total = 0
    for i in arr:
        total+=int(row[i].replace(",",""))
    all_total.append(total)
    if(total>max_total):
        max_total = total
        max_date = row['\ufeff日期']
        max_num=[]
        for i in arr:
            max_num.append(int(row[i].replace(",","")))


# 1.a
sns.set_style("darkgrid", {"axes.axisbelow": True})
sns.lineplot(x=date, y=all_total)
plt.xticks(x_date, rotation=90)
plt.xlabel("日期")
sns.set_style("whitegrid",{"font.sans-serif":['Microsoft JhengHei']})

plt.tight_layout()
plt.savefig('1.a.png')
plt.show()


# 1.b
start_date_index = date.index('2022/4/1')
raise_area_date = date[start_date_index:]
raise_area_all_total = all_total[start_date_index:]

start_x_date_index = x_date.index('2022/4/1')
raise_area_x_date = x_date[start_x_date_index:]

sns.set_style("darkgrid", {"axes.axisbelow": True})
sns.lineplot(x=raise_area_date, y=raise_area_all_total)
plt.xticks(raise_area_x_date, rotation=90)
plt.xlabel("日期")
sns.set_style("whitegrid",{"font.sans-serif":['Microsoft JhengHei']})

plt.tight_layout()
plt.savefig('1.b.png')
plt.show()


# 2.a
max_date_index = date.index(max_date)
plt.figure(figsize=(10, 10))
patches,l_text,p_text =plt.pie(max_num, autopct='%.1f%%')
plt.legend(patches, arr, loc="right")
plt.title(max_date+"確診分布") 
plt.axis("equal")
sns.set_style("whitegrid",{"font.sans-serif":['Microsoft JhengHei']})

plt.tight_layout()
plt.savefig('2.a.png')
plt.show()


# 2.b
driver.get("https://zh.wikipedia.org/zh-tw/%E8%87%BA%E7%81%A3%E8%A1%8C%E6%94%BF%E5%8D%80%E4%BA%BA%E5%8F%A3%E5%88%97%E8%A1%A8")
soup = BeautifulSoup(driver.page_source, "lxml")

dists={"name": [],
         "area": [],
         "num": []}

arr1=["臺北市","新北市","基隆市","宜蘭縣","桃園市","新竹市","新竹縣","苗栗縣","臺中市","彰化縣","南投縣",
     "雲林縣","嘉義市","嘉義縣","臺南市","高雄市","屏東縣","花蓮縣","臺東縣","澎湖縣","連江縣","金門縣"]

for item in arr1:
    dists["name"].append(item)
    dists["area"].append(0)
    dists["num"].append(0)

for i in range(1,23):
    name_path = '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr['+str(i)+']/td[2]/a'
    tag_name = driver.find_element(By.XPATH, name_path)
    
    #print(tag_name.text)
    dists_index = dists["name"].index(tag_name.text)
    arr_index = arr.index(tag_name.text)
    
    area_path = '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr['+str(i)+']/td[6]'
    tag_area = driver.find_element(By.XPATH, area_path)
    #print(tag_area.text)
    dists["area"][dists_index]=float(tag_area.text.replace(",",""))
    dists["num"][dists_index]=max_num[arr_index]

sns.set_style("darkgrid", {"axes.axisbelow": True})
df = pd.DataFrame(dists, 
                  columns=["num", "area"],
                  index=dists["name"])
fig, ax = plt.subplots()
fig.suptitle("縣市確診人數VS.縣市面積("+max_date+")")
#ax ax2為series物件
ax.set_ylabel("確診人數")
ax.set_xlabel("縣市")
ax2 = ax.twinx()
ax2.set_ylabel("縣市面積")

df["num"].plot( ax=ax, 
                 style="r-o",
                 use_index=True,
                 rot=90,
                 label="確診人數")
df["area"].plot( ax=ax2, 
                 style="g--",
                 use_index=True,
                 rot=90,
                 label="縣市面積")
sns.set_style("whitegrid",{"font.sans-serif":['Microsoft JhengHei']})

plt.xticks(range(len(df.index)), df.index, rotation='vertical')

lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2,loc='upper right')

plt.tight_layout()
plt.savefig('2.b.png')
plt.show()


# 2.c = 2.a + 2.b
plt.figure(figsize=(18, 6))

# 2.a
plt.subplot(1, 2, 1)
max_date_index = date.index(max_date)
patches, l_text, p_text = plt.pie(max_num, autopct='%.1f%%')
plt.legend(patches, arr, loc="right")
plt.title(max_date + "確診分布")
plt.axis("equal")

# 2.b
plt.subplot(1, 2, 2)
sns.set_style("darkgrid", {"axes.axisbelow": True})
ax = plt.gca()
fig.suptitle("縣市確診人數VS.縣市面積(" + max_date + ")")
ax.set_ylabel("確診人數")
ax.set_xlabel("縣市")
ax2 = ax.twinx()
ax2.set_ylabel("縣市面積")
df["num"].plot(ax=ax, 
               style="r-o",
               use_index=True,
               rot=90,
               label="確診人數")
df["area"].plot(ax=ax2, 
                style="g--",
                use_index=True,
                rot=90,
                label="縣市面積")
sns.set_style("whitegrid", {"font.sans-serif": ['Microsoft JhengHei']})
plt.xticks(range(len(df.index)), df.index, rotation='vertical')
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper right')

plt.tight_layout()
plt.savefig('2.c.png')
plt.show()















