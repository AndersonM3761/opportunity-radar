import httpx
import re
from typing import Dict, Any, List
import asyncio

# Years that are strictly in the past (Current date: 2026)
PAST_YEARS = r"\b(202[0-5])\b"

async def verify_url_live(url: str) -> bool:
    """
    Checks if a URL is live. Follows redirects.
    Returns True if live (200 OK after redirects), False otherwise.
    """
    if not url:
        return False
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=3.0) as client:
            response = await client.head(url)
            # If head fails, try get (some sites block HEAD)
            if response.status_code == 405:
                response = await client.get(url)
            
            if response.status_code == 200:
                return True
            return False
    except Exception as e:
        print(f"URL Verification failed for {url}: {e}")
        return False

def check_stale_deadline(snippet: str) -> str:
    """
    Checks if the snippet contains obvious past deadlines.
    Current Year Context: 2026
    Returns: 'EXPIRED' if past date found, 'UNCLEAR' otherwise.
    """
    if not snippet:
        return 'UNCLEAR'
        
    if re.search(PAST_YEARS, snippet):
        return 'EXPIRED'
        
    return 'UNCLEAR'

async def verify_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Takes a raw Tavily result dict and adds verification metadata.
    """
    url = result.get('url', '')
    snippet = result.get('content', '')
    
    is_live = await verify_url_live(url)
    deadline_status = check_stale_deadline(snippet)
    
    result['verified_live'] = is_live
    result['deadline_status'] = deadline_status
    
    return result

async def filter_raw_results(raw_results_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Takes a list of Tavily results, verifies them concurrently, 
    and drops strictly dead or expired ones.
    """
    verified_results = await asyncio.gather(*[verify_result(r) for r in raw_results_list])
    
    valid_results = []
    for r in verified_results:
        # Drop if dead link
        if r['verified_live'] == False:
            continue
        # Drop if explicitly expired
        if r['deadline_status'] == 'EXPIRED':
            continue
        valid_results.append(r)
        
    return valid_results
