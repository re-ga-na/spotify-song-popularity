import requests

url = 'http://localhost:5000/results'
r = requests.post(url,json={'Song Title': 'Tonight Will Be Alright', 'Artist':'Lionel Richie'})

print(r.json())