import logging
import time
import requests

BASE_URL = "https://api.jolpi.ca/ergast/f1"
PAGE_SIZE = 100


def _get_page(url, retries=3):
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if attempt == retries:
                raise
            time.sleep(2)


def _flatten(races, season):
    """Из вложенных гонок сделать плоский список строк."""
    rows = []
    for race in races:
        for res in race['Results']:
            rows.append({
                'season': season,
                'round': int(race['round']),
                'race_name': race['raceName'],
                'race_date': race['date'],
                'driver_id': res['Driver']['driverId'],
                'driver_name': res['Driver']['givenName'] + ' ' + res['Driver']['familyName'],       
                'constructor': res['Constructor']['name'],      
                'grid': int(res['grid']),            
                'position': int(res['position']),         
                'points': float(res['points']),       
                'status': res['status'],    
                })          
    return rows

def fetch_results(season):
    all_rows = []
    offset = 0
    total = None

    while total is None or offset < total:
        url = f"{BASE_URL}/{season}/results/?limit={PAGE_SIZE}&offset={offset}"
        data = _get_page(url)
        total = int(data['MRData']['total'])
        races = data['MRData']['RaceTable']['Races']
        all_rows.extend(_flatten(races, season))
        offset += PAGE_SIZE
    return all_rows

if __name__ == '__main__':
    rows = fetch_results(2024)
    print('Строк:', len(rows))