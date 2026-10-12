import json
import requests

def fetch_winners(season):
    """Забрать победителей сезона из API, вернуть список гонок (как пришло из API)."""
    api = f"https://api.jolpi.ca/ergast/f1/{season}/results/1/?limit=100"
    response = requests.get(api)
    response.raise_for_status()
    data = response.json()
    return data['MRData']['RaceTable']['Races']


def transform(races):
    """Превратить сырые гонки в список словарей {'round', 'race', 'winner'}."""
    winners = []
    for race in races:
        driver = race['Results'][0]['Driver']
        winners.append({
            'round': int(race['round']),
            'race': race['raceName'],
            'winner': driver['givenName'] + ' ' + driver['familyName'],
        })
    return winners

def save_json(winners, path):
    """Записать список в JSON-файл."""
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(winners, file, ensure_ascii=False, indent=2)

def main():
    races = fetch_winners(2025)
    winners = transform(races)
    save_json(winners, 'data/winners_2025.json')
    print('Сохранено гонок:', len(winners))

if __name__ == '__main__':
    main()