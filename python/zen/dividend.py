from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome("/mnt/c/Users/Peter/Documents/setup/chromedriver")
driver.get("http://www.dividend.com/ex-dividend-dates.php?from_filter=yes&ex_div_date_min=2018-01-11&ex_div_date_max=2018-01-11&common_shares=on&preferred_shares=on&adrs=on&etns=on&funds=on&notes=on&etfs=on&reits=on")
soup = BeautifulSoup(driver.page_source,"lxml")
driver.quit()
table = soup.select("table#ex-dividend-dates")[0]
list_row =[[tab_d.text.strip().replace("\n","") for tab_d in item.select('th,td')] for item in table.select('tr')]

for data in list_row[:2]:
    print(' '.join(data))
