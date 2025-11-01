import requests
import json
import time
import os
from typing import Optional, List, Dict, Any

# Utility function to compute the agent card URL from agent_url

def get_agent_card_url(agent_url: str) -> str:
    """
    Given an agent_url (which may end with '/a2a'), return the base URL with '/.well-known/agent.json' appended.
    """
    if agent_url.endswith('/a2a'):
        base_url = agent_url[:-4]  # Remove '/a2a'
    else:
        base_url = agent_url
    # Remove trailing slash if present
    if base_url.endswith('/'):
        base_url = base_url[:-1]
    return f"{base_url}/.well-known/agent.json"


def fetch_agent_card(agent_url: str, timeout: float = 5.0) -> Optional[Dict[str, Any]]:
    """
    Fetch the agent card from the agent's /.well-known/agent.json endpoint.
    Uses the get_agent_card_url utility to compute the correct URL.
    """
    card_url = get_agent_card_url(agent_url)
    try:
        resp = requests.get(card_url, timeout=timeout)
        if resp.status_code == 200:
            return resp.json()
        else:
            return None
    except Exception:
        return None


def send_a2a_message(agent_url: str, message: str, attachments: Optional[List[str]] = None, context_id: Optional[str] = None, reset: bool = False, timeout: float = 30.0) -> Dict[str, Any]:
    """
    Send a message to a FastA2A-compatible agent and return the response.
    """
    # Always POST to /a2a endpoint
    if agent_url.endswith('/a2a'):
        post_url = agent_url
    else:
        # Ensure single trailing slash
        post_url = agent_url.rstrip('/') + '/a2a'

    payload = {
        "message": message,
        "attachments": attachments or [],
        "reset": reset
    }
    if context_id:
        payload["context_id"] = context_id

    headers = {"Content-Type": "application/json"}
    resp = requests.post(post_url, data=json.dumps(payload), headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def get_agent_metadata(agent_url: str, timeout: float = 5.0) -> Optional[Dict[str, Any]]:
    """
    Fetch and return the agent card (metadata) for the given agent_url.
    Uses the fetch_agent_card function which applies the correct URL logic.
    """
    return fetch_agent_card(agent_url, timeout=timeout)


# Example usage in tool logic (pseudo-code, not executed here):
#
# agent_url = "http://localhost:8000/a2a"
# card = get_agent_metadata(agent_url)
# if card is None:
#     raise Exception("Could not fetch agent card!")
#
# response = send_a2a_message(agent_url, "Hello!", attachments=[], reset=False)
# print(response)

