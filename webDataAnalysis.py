import os
import re

import sqlConversion

# Define the dictionary which will be used to count the number of occurrences of each element on each processor's page
# The dictionary's key will be the element, and the value will be the number of occurrences
# Short for common elements
comElements = {}


async def main():
    # The variable "it" stands for iteration and is used to print the progress of the data iteration
    # It is a count of how many files have been open and analyzed used simply to show the program's progress
    it = 0
    # Get the name of each file in the folder data
    # The names correspond to the processor numbers, previously extracted by the intelExtract.main() function
    for file in os.listdir(os.fsencode("data")):
        print('Analyzing ' + str(os.fsencode(file)) + ' [' + str(it) + "/273]")
        # Iterate through every processor's file in the data folder found by processor number
        with open("data/" + os.fsdecode(file), "r") as f:
            # For each element in the processor's text file, add its count to the common elements dictionary
            for l in f:
                element = eval(l).get("element")
                # If it already exists in the dictionary, add 1 to its count
                if element in comElements:
                    comElements[element] = comElements[element] + 1
                # If it doesn't exist in the dictionary, define it and set its count to one
                else:
                    comElements[element] = 1
        it = it + 1

    # Once all the attributes, have been counted, create a new file "webDataAnalysis.txt" to store all the most common elements
    with open('webDataAnalysis.txt', "w") as f:
        # The Processor Number is manually defined as the primary key for to be used in the table
        f.write("ProcessorNumber primary key\n")
        # Iterate through all the elements in the common elements dictionary
        for element, key in comElements.items():
            # Clean the element to remove spaces and \n values so that it is in proper format for database fields
            elementCleaned = re.sub('\W+','', element.replace(" ", "")) + "\n"
            # Check to see if the element is common among 80% of processors, if true then add element to text file to be placed in database
            # Also check to make sure the element is not the Processor Number, as that was already added and assigned as the primary key earlier
            if key > (len(os.listdir(os.fsencode("data"))) *.8) and elementCleaned != "ProcessorNumber\n":
                f.write(elementCleaned)
    # Once all the elements common in 80% of the processors have been placed into the text file, the next step is to call the SQL conversion function
    # This next function will create the database and table, and begin populating it with each processor's attributes and specifications
    await sqlConversion.main()
