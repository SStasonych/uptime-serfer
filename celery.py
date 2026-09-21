import httpx
from datetime import datetime

async def check_site(site_url: str):
    start_time = datetime.utcnow()
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(site_url)
            status_code = response.status_code
            is_available = 200 <= status_code < 400
    except httpx.HTTPError:
        status_code = 0
        is_available = False
        
    response_time = (datetime.utcnow() - start_time).total_seconds()