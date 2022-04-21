import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By

import webDataAnalysis


async def extractData(url):
    driver = webdriver.Chrome()

    driver.get(url)

    elements = driver.find_elements(By.XPATH, '//*[(@id = "bladeInside")]//li')
    name = ""
    elementData = [{"element":"url", "value":url}]
    for i in range(len(elements)):
        elData = {
            "element": elements[i].text.split("\n")[0],
            "value": elements[i].text.split("\n")[1]
        }
        elementData.append(elData)

        if elData.get("element") == "Processor Number":
            name = elData.get("value")
            print("Extracting data from " + name)

    with open("data/" + name + ".txt", "w") as f:
        for i in elementData:
            f.write(str(i) + "\n")

    driver.quit()
    print("Data extraction complete.")


async def main():
    with open('intelURLS.txt', "r") as f:
        for l in f:
            url = l.replace("\n", "")
            await extractData(url)
    await webDataAnalysis.main()


