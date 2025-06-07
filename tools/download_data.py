# /// script
# dependencies = [
#   "httpx",
#   "python-dotenv",
#   "pydantic"
# ]
# ///

import httpx
from dotenv import load_dotenv
import os
import logging
import json
from pydantic import BaseModel

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

client_id = os.getenv('BNET_CLIENT_ID')
client_secret = os.getenv('BNET_CLIENT_SECRET')




class OAuthResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    sub: str


raw_response = httpx.post(
    'https://oauth.battle.net/token',
    auth=(client_id, client_secret),
    data={'grant_type': 'client_credentials'}
)

oauth_response = OAuthResponse.model_validate(raw_response.json())
access_token = oauth_response.access_token

auth_client = httpx.Client(
    base_url='https://eu.api.blizzard.com',
    headers={'Authorization': f'Bearer {access_token}'}
)

logging.info('Downloading cards...')
cards = []
page_idx = 1
while True:
    page_response = auth_client.get(
        '/hearthstone/cards',
        params={
            'locale': 'en_US',
            'gameMode': 'battlegrounds',
            'pageSize': 1000,
            'page': page_idx,
        }
    ).json()
    cards.extend(page_response['cards'])

    if page_response['pageCount'] == page_idx:
        break

    page_idx += 1

with open('../data/cards.json', 'w') as f:
    json.dump(cards, f, indent=4)
logging.info(f'Saved {len(cards)} cards to ../data/cards.json')


metadata = auth_client.get('/hearthstone/metadata').json()
with open('../data/metadata.json', 'w') as f:
    json.dump(metadata, f, indent=4)
logging.info(f'Saved {len(metadata)} metadata to ../data/metadata.json')

# download /hearthstone/metadata/heroes to heroes.json
heroes = auth_client.get('/hearthstone/metadata/heroes').json()
with open('../data/heroes.json', 'w') as f:
    json.dump(heroes, f, indent=4)