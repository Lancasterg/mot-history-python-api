import requests
import time


"""
Usage:

    client = MotHistoryAPI(
        client_secret="abc-def-efg",
        client_id="1234-5678-0987",
        api_key="acbdeg1234567",
        token_url="0987-1234-0987-5555"
    )

    response = client.get_mot_history_by_reg("MUI7181")

"""


class MotHistoryAPI:

    _token: str | None = None
    _token_refresh: float | None = None

    def __init__(self, client_secret: str, client_id: str, api_key: str, token_url: str):
        self._client_secret = client_secret
        self._client_id = client_id
        self._api_key = api_key
        self._token_url = f"https://login.microsoftonline.com/{token_url}/oauth2/v2.0/token"

        self._session = requests.Session()

        self._get_token()

    def _get_token(self) -> str:

        if self._token_refresh is None or time.time() > self._token_refresh:
            headers = {
                "content-type": "application/x-www-form-urlencoded",
            }

            data = {
                "grant_type": "client_credentials",
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "scope": "https://tapi.dvsa.gov.uk/.default"
            }

            response = self._session.post(
                self._token_url,
                headers=headers,
                data=data
            )

            response_json = response.json()

            self._token = response_json["access_token"]

            # token expires after 3599 seconds
            # refresh token if expiry time is less than one minute away
            self._token_refresh = time.time() + (response_json["expires_in"] * 1000) - 60000

        return self._token

    def get_mot_history_by_reg(self, registration: str) -> dict:

        url = f"https://history.mot.api.gov.uk/v1/trade/vehicles/registration/{registration}"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self._get_token()}",
            "X-API-Key": self._api_key
        }

        response = self._session.get(
            url,
            headers=headers
        )

        return response.json()

    def get_mot_history_by_vin(self, vin: str) -> dict:
        url = f"https://history.mot.api.gov.uk/v1/trade/vehicles/vin/{vin}"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self._get_token()}",
            "X-API-Key": self._api_key
        }

        response = self._session.get(
            url,
            headers=headers
        )

        return response.json()

    def bulk_download(self) -> dict:
        raise NotImplementedError("method not yet implemented")
