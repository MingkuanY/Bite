import requests
img = <'replace-with-path-to-image'>
api_user_token = <'replace-with-your-api-user-token'>
headers = {'Authorization': 'Bearer ' + api_user_token}

# Single/Several Dishes Detection
url = 'https://api.logmeal.es/v2/image/segmentation/complete'
resp = requests.post(url,files={'image': open(img, 'rb')},headers=headers)

# Nutritional information
url = 'https://api.logmeal.es/v2/recipe/nutritionalInfo'
resp = requests.post(url,json={'imageId': resp.json()['imageId']}, headers=headers)
print(resp.json()) # display nutritional info
