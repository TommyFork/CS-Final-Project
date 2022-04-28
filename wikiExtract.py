from selenium import webdriver
from selenium.webdriver.common.by import By

import intelExtract

# Define the URL of the Wikipedia page containing the list of Intel processors we will be extracting
wikiURL = 'https://en.wikipedia.org/wiki/List_of_Intel_processors'


async def main():
    print("Extracting URLS from Wikipedia...")
    # Define the driver as Chrome and request the Wikipedia URL
    driver = webdriver.Chrome()
    driver.get(wikiURL)
    # Find all the processor's URLs using the XPATH found with the Chrome extension SelectorGadget
    elements = driver.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "text", " " ))]')
    # Once all the URLS have been scraped, create a new file "intelURLS.txt" to store all the URLs to be scraped by the intelExtract.main() function
    with open('intelURLS.txt', "w") as f:
        for element in elements:
            # Extract the href attribute from the URL to ensure we are only extracting the link
            elementURL = element.get_attribute('href')
            # Check to see if the URL meets a set of criteria used to eliminate non-product page URLs
            # If the criteria is met, add the URL to the text file
            if await checkURL(elementURL):
                f.write(elementURL + "\n")
    print("Wikipedia URLS extracted.")
    driver.quit()

    # Once all the URLs have been extracted from the Wikipedia page and placed in the text file, the next step is to go page-by-page and extract each element from the processor
    # This next function will use the intelURLS.txt file to iterate through each product page
    await intelExtract.main()


async def checkURL(url):
    # After examining the URLs, we determined that all the product pages contained “ark.intel.com”, “products”, and “processor” and not “generation”
    # This function was created to only accept URLs meeting these conditions
    if ('ark.intel.com' in url) and ('products' in url) and ('processor' in url) and not ('generation' in url):
        return True
    else:
        return False

