from datetime import datetime
from typing import Dict, List, Tuple

import aiohttp

BASE_URL = "https://michiganelections.io/api"

# BASE_URL = "https://mi-elections-staging-pr-188.herokuapp.com/api"

async def get_status(
    first_name: str, last_name: str, birth_date: str, zip_code: int
) -> Dict:
    if "-" not in birth_date:
        dt = datetime.strptime(birth_date, "%m/%d/%Y")
        birth_date = dt.date().isoformat()

    async with aiohttp.ClientSession() as session:
        url = f"{BASE_URL}/registrations/?first_name={first_name}&last_name={last_name}&birth_date={birth_date}&zip_code={zip_code}"
        async with session.get(url) as response:
            data = await response.json()

    return data