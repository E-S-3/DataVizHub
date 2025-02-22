import requests
import asyncio
import aiohttp
from datetime import datetime

# URL HERE
CSV_URL = "" 
CSV_FILE = "data/dataset.csv"

async def download_csv():
    async with aiohttp.ClientSession() as session:
        async with session.get(CSV_URL) as response:
            with open(CSV_FILE, "wb") as file:
                file.write(await response.read())
