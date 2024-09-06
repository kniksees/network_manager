import requests
import json

class NetworkManager:
   
    def get_request(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.RequestException, ValueError) as e:
            return None
    
    def filter_heroes(self, heroes, gender, has_work):
        filtered_heroes = [
            hero for hero in heroes
            if  'appearance' in hero and 'gender' in hero['appearance'] and
                'work' in hero and 'occupation' in hero['work'] and 'base' in hero['work'] and 
                hero['appearance']['gender'].lower() == gender.lower() and
                (hero['work']['occupation'] != '-' or hero['work']['base'] != '-') == has_work
        ]
        return filtered_heroes
    
    def find_max(self, filtered_heroes):
        max_height = 0
        res_hero = None
        for hero in filtered_heroes:
            height = 0

            if 'appearance' not in hero or 'height' not in hero['appearance']:
                continue
            if len(hero['appearance']['height']) != 2 or len(hero['appearance']['height'][1].split()) != 2:
                continue

            if hero['appearance']['height'][1].split()[1] == 'cm':
                height = float(hero['appearance']['height'][1].split()[0])
            elif hero['appearance']['height'][1].split()[1] == 'meters':
                height = float(hero['appearance']['height'][1].split()[0]) * 100 
            else:
                continue 

            if height > max_height:
                max_height = float(hero['appearance']['height'][1].split()[0])
                res_hero = hero
        return res_hero
    
    def get_the_tallest_hero(self, gender, has_work):
        heroes = self.get_request('https://akabab.github.io/superhero-api/api/all.json')
        filtered_heroes = self.filter_heroes(heroes, gender, has_work)
        tallest_hero = self.find_max(filtered_heroes)
        return(tallest_hero)
