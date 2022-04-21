import asyncio
import os
import re

import sqlConversion

comElements = {}


async def main():
    it = 0
    for file in os.listdir(os.fsencode("data")):
        print('Analyzing ' + str(os.fsencode(file)) + ' [' + str(it) + "/273]")
        with open("data/" + os.fsdecode(file), "r") as f:
            for l in f:
                element = eval(l).get("element")
                if element in comElements:
                    comElements[element] = comElements[element] + 1
                else:
                    comElements[element] = 1
        it = it + 1

    with open('webDataAnalysis.txt', "w") as f:
        f.write("ProcessorNumber primary key\n")
        for element, key in comElements.items():
            elementCleaned = re.sub('\W+','', element.replace(" ", "")) + "\n"
            if key > (len(os.listdir(os.fsencode("data"))) *.8) and elementCleaned != "ProcessorNumber\n":
                f.write(elementCleaned)
    await sqlConversion.main()
