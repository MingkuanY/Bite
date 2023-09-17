import requests

url = "https://api.tryterra.co/v2/auth/generateWidgetSession"

payload = {
      "reference_id": "eatingbetter-prod-dpMFnuUYIQ",
    "providers": "FITBIT",
    "language": "en"
}
headers = {
    "accept": "application/json",
    "dev-id": "testingTerra",
    "content-type": "application/json",
    "x-api-key": "ussv5SAQ53a1nNTxsMr9G41zj2KUhYMk5eDU1hjG"
}

response = requests.post(url, json=payload, headers=headers)
response.raise_for_status()

url = response.json()["url"]

print(url)