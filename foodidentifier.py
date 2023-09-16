import requests
img = 'C:\\Users\\Alex Kranias\\Bite\\images_test\\IMG_4904.JPG'
api_user_token = '72858ab56101a40750278b25356e2ddf8adce260'
headers = {'Authorization': 'Bearer ' + api_user_token}

# Single/Several Dishes Detection
url = 'https://api.logmeal.es/v2/image/segmentation/complete'
resp = requests.post(url,files={'image': open(img, 'rb')},headers=headers)

print(resp.status_code)
print(resp.json()['imageId'])

# Nutritional information
url = 'https://api.logmeal.es/v2/recipe/nutritionalInfo'
resp = requests.post(url,json={'imageId': resp.json()['imageId']}, headers=headers)
print(resp.json()) # display nutritional info