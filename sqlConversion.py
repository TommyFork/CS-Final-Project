import os
import re
import sqlite3
import time

# A SQLite database is created and named the current timestamp of when the program was executed
# This timestamp was used for debugging to keep track of which version of code produced which databases
con = sqlite3.connect(str(time.time()).split(".")[0] + ".db")
cur = con.cursor()


async def createTable(attributes):
    tableElements = ""
    # The attributes passed through are iterated through and used to create a string with the format (attribute1, attribute2, ...)
    # This format is the syntax needed for the SQL query used to create the table
    for i in range(len(attributes)):
        # If the attribute is first in the list, add an open parenthesis before it
        if i == 0:
            tableElements = "(" + attributes[i]
        # If the attribute is neither the first nor the last in the list, simply append it to the list with a comma
        elif i != len(attributes) - 1:
            tableElements = tableElements + ", " + attributes[i]
        # If the attribute is the last element in the list, append it to the list with a comma and a close parenthesis
        else:
            tableElements = tableElements + ", " + attributes[i] + ")"

    # The previously generated string of attributes is then concatenated into a query to be used to create the table
    query = "CREATE TABLE processors " + tableElements
    # The query is then executed creating the table
    cur.execute(query)


async def importData(attributes):
    await createTable(attributes)
    # Since the table has been created and the Processor Number has been assigned as its primary key, we must now remove the "primary key" component from the string
    for i in range(len(attributes)):
        if attributes[i] == "ProcessorNumber primary key":
            attributes[i] = "ProcessorNumber"
    # Now we must iterate through each txt file containing the processor elements to populate the database
    for file in os.listdir(os.fsencode("data")):
        with open("data/" + os.fsdecode(file), "r") as f:
            # Because not every txt file contains elements in the same order, we must define the order in the INSERT query
            # We therefore are creating 2 components of the string, one defining the attributes, and one as a placeholder for the values
            # This also accounts for null values, as if it is not contained in the txt file, it will not be contained in the query, and therefore will be populated as null
            queryValues = {}

            for l in f:
                element = eval(l)
                # The element from the txt file is cleaned to ensure that it is in the proper format for an SQL attribute
                elementCleaned = re.sub('\W+', '', element.get("element").replace(" ", "").replace("\n", ""))
                if elementCleaned in attributes:
                    queryValues[elementCleaned] = element.get("value")

                sql1 = ""
                sql2 = ""
            # Once the queryValues dictionary has been populated with all the elements, we must iterate through it and create the components of the query
            # sql1 will serve as a definition of the attributes
            # sql2 will serve as a placeholder for the values, as signified by the : placed before the attribute is defined
            for i, x in queryValues.items():
                sql1 = sql1 + i + ", "
                sql2 = sql2 + ":" + i + ", "

            # The [:-2] attached to the string is used to correct a formatting issue and ensure the syntax is proper for the SQL query
            fullSql = "INSERT INTO processors (" + sql1[:-2] + ") VALUES (" + sql2[:-2] + ")"
            # Once the SQL query has been created and has both the variables defined and the values populated, we will insert it into the database
            try:
                cur.execute(fullSql, queryValues)
                con.commit()
            except:
                print("err")


async def main():
    # The first step is to call the common elements extracted from the webDataAnalysis.main() function
    # These elements, stored in webDataAnalysis.txt, are then passed through the function importData() to begin the SQL population
    attributes = []
    with open('webDataAnalysis.txt', "r") as f:
        for l in f:
            attributes.append(l.replace("\n", ""))
    await importData(attributes)
    con.close()


