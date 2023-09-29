import requests

url = 'http://127.0.0.1:5555/anime/update_anime_list?year=2023&broadcast_season=2'
response = requests.post(url)

print(response.text)