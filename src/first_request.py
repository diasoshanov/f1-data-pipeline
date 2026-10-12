import requests
import json

api = "https://api.jolpi.ca/ergast/f1/2025/results/1/?limit=100"

response = requests.get(api)

data = response.json()

races = data['MRData']['RaceTable']['Races']

winners = []

for race in races:
    winner = race['Results'][0]['Driver']
    one_race = {'Round': int(race['round']),
                'race':['raceName'], 
                'winner': winner['givenName'] + ' ' + winner['familyName']
                }
    winners.append(one_race)

with open ('data/winners_2025.json', 'w', encoding='utf-8') as file:
    json.dump(winners, file,ensure_ascii=False,indent=2)

print(winners)