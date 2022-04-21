import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By

import intelExtract

wikiURL = 'https://en.wikipedia.org/wiki/List_of_Intel_processors'


async def main():
    print("Extracting URLS from Wikipedia...")
    driver = webdriver.Chrome()
    driver.get(wikiURL)
    elements = driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "text", " " ))]')
    with open('intelURLS.txt', "w") as f:
        for element in elements:
            elementURL = element.get_attribute('href')
            if await checkURL(elementURL):
                f.write(elementURL + "\n")
    print("Wikipedia URLS extracted.")
    driver.quit()
    await intelExtract.main()


async def checkURL(url):
    if ('ark.intel.com' in url) and ('products' in url) and ('processor' in url) and not ('generation' in url):
        return True
    else:
        return False

