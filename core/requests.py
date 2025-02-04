import requests
from typing import List, Dict, Optional

class PatreonAPI:
    BASE_URL = "https://www.patreon.com/api/oauth2/v2"

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            "Authorization": f'Bearer {access_token}',
            "User-Agent": "Patreon API Client",
            'Content-Type': 'application/json',
        }

    def _handle_request_error(self, response):
        try:
            error_details = response.json()
            print(f"Detailed Error: {error_details}")
        except ValueError:
            print(f"Raw Error Response: {response.text}")

        response.raise_for_status()

    def get_comprehensive_member_info(self, member_id: str) -> Dict:
        url = f"{self.BASE_URL}/members/{member_id}"
        params = {
            'include': 'user,currently_entitled_tiers',
            'fields[member]': (
                'campaign_lifetime_support_cents,'
                'currently_entitled_amount_cents,'
                'email,'
                'full_name,'
                'is_follower,'
                'last_charge_date,'
                'last_charge_status,'
                'lifetime_support_cents,'
                'next_charge_date,'
                'note,'
                'patron_status,'
                'pledge_cadence,'
                'pledge_relationship_start,'
                'will_pay_amount_cents'
            ),
            'fields[user]': 'social_connections',
            'fields[tier]': 'title'
        }

        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=params
            )

            if response.status_code != 200:
                self._handle_request_error(response)

            full_response = response.json()

            comprehensive_info = {
                "member_details": {},
                "user_details": {},
                "tiers": []
            }

            if 'data' in full_response and 'attributes' in full_response['data']:
                comprehensive_info['member_details'] = {
                    "campaign_lifetime_support_cents": full_response['data']['attributes'].get(
                        'campaign_lifetime_support_cents'),
                    "currently_entitled_amount_cents": full_response['data']['attributes'].get(
                        'currently_entitled_amount_cents'),
                    "email": full_response['data']['attributes'].get('email'),
                    "full_name": full_response['data']['attributes'].get('full_name'),
                    "is_follower": full_response['data']['attributes'].get('is_follower'),
                    "last_charge_date": full_response['data']['attributes'].get('last_charge_date'),
                    "last_charge_status": full_response['data']['attributes'].get('last_charge_status'),
                    "lifetime_support_cents": full_response['data']['attributes'].get('lifetime_support_cents'),
                    "next_charge_date": full_response['data']['attributes'].get('next_charge_date'),
                    "note": full_response['data']['attributes'].get('note'),
                    "patron_status": full_response['data']['attributes'].get('patron_status'),
                    "pledge_cadence": full_response['data']['attributes'].get('pledge_cadence'),
                    "pledge_relationship_start": full_response['data']['attributes'].get('pledge_relationship_start'),
                    "will_pay_amount_cents": full_response['data']['attributes'].get('will_pay_amount_cents')
                }

            if 'included' in full_response:
                for included in full_response['included']:
                    if included['type'] == 'user':
                        comprehensive_info['user_details'] = {
                            "social_connections": included.get('attributes', {}).get('social_connections', {})
                        }

                    if included['type'] == 'tier':
                        comprehensive_info['tiers'].append({
                            "title": included.get('attributes', {}).get('title')
                        })

            return comprehensive_info

        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return {}