from selenium import webdriver
from selenium.webdriver.common.by import By

import webDataAnalysis


async def extractData(url):
    # Define the driver as Chrome and request the parsed URL
    driver = webdriver.Chrome()
    driver.get(url)

    # Find all the processor's elements using the XPATH which targets list items with the id "bladeInside"
    elements = driver.find_elements(By.XPATH, '//*[(@id = "bladeInside")]//li')
    # Define variables that will be uniform across all the processor data extractions, such as the processor's number, defined as name, and its elements, defined as elementData
    name = ""
    # Here, we are populating an element not found on the page, URL, so that we can keep track of which pages each processor corresponds to
    elementData = [{
        "element": "url",
        "value": url
    }]
    for i in range(len(elements)):
        elData = {
            "element": elements[i].text.split("\n")[0],
            "value": elements[i].text.split("\n")[1]
        }
        elementData.append(elData)

        # Once we scrape the element "Processor Number", we will use this as the primary key of the processor
        # Therefore, we will assign the name variable this value which will ultimately be the name of the text file used to store the data before being populated in the SQL database
        if elData.get("element") == "Processor Number":
            name = elData.get("value")
            print("Extracting data from " + name)

    # Once all the elements have been extracted from the page, we will create a file for the processor so that we can easily access the extracted data later without having to render the html page again
    with open("data/" + name + ".txt", "w") as f:
        for i in elementData:
            f.write(str(i) + "\n")

    driver.quit()
    print("Data extraction complete.")


async def main():
    # Iterate through each Intel.com URL, and then call the function extractData() to open each page and extract its data
    # These URLs were pulled from Wikipedia through the function wikiExtract.main()
    with open('intelURLS.txt', "r") as file:
        for line in file:
            # Clean the element to remove \n values so that it is in proper format for a Selenium request
            url = line.replace("\n", "")
            await extractData(url)
    # Once all the URLs have been called and all the data has been extracted, call the webDataAnalysis function
    # The next function will analyze the attributes pulled to determine which ones are most common and should be used for the database creation
    await webDataAnalysis.main()
