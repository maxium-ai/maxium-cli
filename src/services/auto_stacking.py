import click
import requests

from src.util import get_token
from src.config import config

def auto_stack_commits(commits_data: list[dict]) -> dict:
   """Send commits to API for auto-stacking
   
   Example API Response:
   {
       "needs_stacking": true,
       "reason": "Large changes detected that can be logically grouped",
       "stacks": [
           {
               "base_commit": "hash1", 
               "description": "Core API changes",
               "commits": [
                   {
                       "hash": "hash1",
                       "message": "Add new API endpoints"
                   },
                   {
                       "hash": "hash2", 
                       "message": "Implement handlers"
                   }
               ]
           }
       ]
   }
   
   Or when no stacking needed:
   {
       "needs_stacking": false,
       "reason": "Changes are already well structured and coherent",
       "stacks": []
   }
   """
   
   try:
       token = get_token()
       response = requests.post(
           config.BASE_AUTO_STACKING_URL,
           json={'commits': commits_data},
           headers={
               'X-Verification-Token': token or 'no-token-available', 'Content-Type': 'application/json'
           }
       )
       response.raise_for_status()
       return response.json()
   except requests.RequestException:
       raise click.ClickException("Failed to auto-stack commits due to an issue. Please try again later.")
