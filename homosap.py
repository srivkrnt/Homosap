from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from sys import platform
from pyfiglet import figlet_format
import time
import os
import xlwt

print(figlet_format('HomoSapiens - Scraper', font='digital'))

def configure_headless():
    global driver
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")

    if platform == "linux" or platform == "linux2":
        name = "/linux"
    elif platform == "darwin":
        name = "/mac"
    elif platform == "win32":
        name = "/win.exe"
    chrome_driver = os.getcwd() + name
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)

def write_to_excel(data):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("HomoSapiens")

    row = 0
    for item in data:
        col = 0
        for value in item:
            sheet.write(row, col, value)
            col += 1
        row += 1

    workbook.save('sapiens.xls')

def scrapeData(page_source):
    global data
    soup = BeautifulSoup(page_source, 'lxml')
    entries = soup.find_all('tr', attrs={'class':'cdk-row'})

    for entry in entries:
        cols = entry.find_all('td')
        id = cols[0].text
        accession = cols[1].text
        proteinName = cols[2].text
        disorderContent = cols[4].text.replace(' ', '').replace('%','')

        disorderContent = float(disorderContent)
        if disorderContent >= 20:
            print(id, accession, proteinName, disorderContent)
            data.append((id, accession, proteinName, disorderContent))

def homosap(driver):
    page_source = driver.page_source
    scrapeData(page_source)

    for curPage in range(0, 25):
        nextPage = driver.find_element_by_xpath('/html/body/app-root/div/div[2]/app-browse-advanced/div/div/div[2]/div[1]/div/div[2]/div[2]/div/pagination/ul/li[4]/a')
        nextPage.click()
        time.sleep(2)
        page_source = driver.page_source
        scrapeData(page_source)

global driver, data
configure_headless()
data = []
driver.get('https://disprot.org/browse?ncbi_taxon_id=9606')
homosap(driver)
write_to_excel(data)
driver.close()
driver.quit()
