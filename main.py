import asyncio

import wikiExtract

# Initiate the chain of functions that compile the dataset
# This is run asynchronously utilizing the library asyncio
asyncio.run(wikiExtract.main())