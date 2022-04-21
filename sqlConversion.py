import os
import re
import sqlite3
import time

con = sqlite3.connect(str(time.time()).split(".")[0] + ".db")
cur = con.cursor()


async def createTable(attributes):
    tableElements = ""
    for i in range(len(attributes)):
        if i == 0:
            tableElements = "(" + attributes[i]
        elif i != len(attributes) - 1:
            tableElements = tableElements + ", " + attributes[i]
        else:
            tableElements = tableElements + ", " + attributes[i] + ")"

    query = "CREATE TABLE processors " + tableElements
    cur.execute(query)


async def importData(attributes):
    await createTable(attributes)
    for i in range(len(attributes)):
        if attributes[i] == "ProcessorNumber primary key":
            attributes[i] = "ProcessorNumber"
    for file in os.listdir(os.fsencode("data")):
        with open("data/" + os.fsdecode(file), "r") as f:

            queryValues = {}

            for l in f:
                element = eval(l)
                elementCleaned = re.sub('\W+', '', element.get("element").replace(" ", "").replace("\n", ""))
                if elementCleaned in attributes:
                    queryValues[elementCleaned] = element.get("value")

                sql1 = ""
                sql2 = ""

            for i, x in queryValues.items():
                sql1 = sql1 + i + ", "
                sql2 = sql2 + ":" + i + ", "

            fullSql = "INSERT INTO processors (" + sql1[:-2] + ") VALUES (" + sql2[:-2] + ")"
            try:
                cur.execute(fullSql, queryValues)
                con.commit()
            except:
                print("err")


async def main():
    attributes = []
    with open('webDataAnalysis.txt', "r") as f:
        for l in f:
            attributes.append(l.replace("\n", ""))
    await importData(attributes)
    con.close()


