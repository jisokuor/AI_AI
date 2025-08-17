"""
Internet connectivity checker using requests.
Attempts a GET request to Google with timeout and error handling.
Reusable as a module.
"""
import requests

def is_connected(url="https://www.google.com", timeout=3):
    """
    Checks internet connectivity by attempting to GET the given URL.
    Returns True if reachable, else False.
    Raises only in the event of invalid input (never on network error).
    Args:
        url (str): URL to test (default google.com)
        timeout (float): seconds for connect & read timeouts
    Returns:
        bool: True if network reachable
    """
    try:
        resp = requests.get(url, timeout=(timeout,timeout))
        # Accept status 200/204/301/302 etc. as 'online' (not strict)
        return resp.status_code < 500
    except requests.exceptions.RequestException:
        return False
