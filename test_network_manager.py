from network_manager import NetworkManager

class TestNetworkManager:

    def test_get_request(self):
        nm = NetworkManager()
        assert nm.get_request('https://akabab.github.io/superhero-api/api/all.json') != ''

    def test_filter_heroes(self):
        heroes = [
            {"id":  1, "appearance": {"gender": "male"},    "work": {"occupation": "true",  "base": "true"}},
            {"id":  2, "appearance": {"gender": "male"},    "work": {"occupation": "-",     "base": "-"}},
            {"id":  3, "appearance": {"gender": "male"},    "work": {"occupation": "-",     "base": "true"}},
            {"id":  4, "appearance": {"gender": "male"},    "work": {"occupation": "true",  "base": "-"}},
            {"id":  5, "appearance": {"gender": "female"},  "work": {"occupation": "true",  "base": "true"}},
            {"id":  6, "appearance": {"gender": "female"},  "work": {"occupation": "-",     "base": "-"}},
            {"id":  7, "appearance": {"gender": "female"},  "work": {"occupation": "-",     "base": "true"}},
            {"id":  8, "appearance": {"gender": "female"},  "work": {"occupation": "true",  "base": "-"}},
            {"id":  9, "appearance": {"gender": "-"},       "work": {"occupation": "true",  "base": "true"}},
            {"id": 10, "appearance": {"gender": "-"},       "work": {"occupation": "-",     "base": "-"}},
            {"id": 11, "appearance": {"gender": "-"},       "work": {"occupation": "-",     "base": "true"}},
            {"id": 12, "appearance": {"gender": "-"},       "work": {"occupation": "true",  "base": "-"}},
            {"id": 13},
            {"id": 14, "appearance": {}},
            {"id": 15, "appearance": {"gender": "-"}},
            {"id": 12, "work": {}},
            {"id": 12, "work": {"base": "-"}},
            {"id": 12, "work": {"occupation": "true"}},
        ]
        nm = NetworkManager()  
        assert nm.filter_heroes(heroes, 'male', True) ==       [{'id':  1, 'appearance': {'gender': 'male'},    'work': {'occupation': 'true',  'base': 'true'}},
                                                                {'id':  3, 'appearance': {'gender': 'male'},    'work': {'occupation': '-',     'base': 'true'}},
                                                                {'id':  4, 'appearance': {'gender': 'male'},    'work': {'occupation': 'true',  'base': '-'}}]
        
        assert nm.filter_heroes(heroes, 'male', False) ==      [{'id':  2, 'appearance': {'gender': 'male'},    'work': {'occupation': '-',     'base': '-'}}]

        assert nm.filter_heroes(heroes, 'female', True) ==     [{'id':  5, 'appearance': {'gender': 'female'},  'work': {'occupation': 'true',  'base': 'true'}},
                                                                {'id':  7, 'appearance': {'gender': 'female'},  'work': {'occupation': '-',     'base': 'true'}},
                                                                {'id':  8, 'appearance': {'gender': 'female'},  'work': {'occupation': 'true',  'base': '-'}}]
        
        assert nm.filter_heroes(heroes, 'female', False) ==    [{'id':  6, 'appearance': {'gender': 'female'},  'work': {'occupation': '-',     'base': '-'}}]

        assert nm.filter_heroes(heroes, '-', True) ==          [{'id':  9, 'appearance': {'gender': '-'},       'work': {'occupation': 'true',  'base': 'true'}},
                                                                {'id': 11, 'appearance': {'gender': '-'},       'work': {'occupation': '-',     'base': 'true'}},
                                                                {'id': 12, 'appearance': {'gender': '-'},       'work': {'occupation': 'true',  'base': '-'}}]
        
        assert nm.filter_heroes(heroes, '-', False) ==         [{'id': 10, 'appearance': {'gender': '-'},       'work': {'occupation': '-',     'base': '-'}}]

        assert nm.filter_heroes(heroes, 'not valid gender', True) == []

        assert nm.filter_heroes(heroes, 'not valid gender', False) == []


    def test_find_max(self):
        nm = NetworkManager()
        heroes = [
            {"id":  1, "appearance": {"gender": "male",  "height": ["-", "99 cm"]},      "work": {"occupation": "true", "base": "true"}},
            {"id":  2, "appearance": {"gender": "male",  "height": ["-", "1 meters"]},   "work": {"occupation": "true", "base": "true"}},
            {"id":  3, "appearance": {"gender": "male",  "height": ["-", "2 kg"]},       "work": {"occupation": "true", "base": "true"}},
            {"id":  4},
            {"id":  5, "appearance": {"gender": "male",  "height": []},                  "work": {"occupation": "true", "base": "true"}},
        ]
        assert nm.find_max(heroes) == {'id': 2, 'appearance': {'gender': 'male', 'height': ['-', '1 meters']}, 'work': {'occupation': 'true', 'base': 'true'}}
            
'''
    def test_get_the_tallest_hero(self):
        nm = NetworkManager()
        hero = nm.get_the_tallest_hero('male', True)
        assert hero is not None
        if hero is not None:
            assert hero['id'] == 728

        hero = nm.get_the_tallest_hero('male', False)
        assert hero is not None
        if hero is not None:
            assert hero['id'] == 574

        hero = nm.get_the_tallest_hero('female', True)
        assert hero is not None
        if hero is not None:
            assert hero['id'] == 716
        
        hero = nm.get_the_tallest_hero('female', False)
        assert hero is not None
        if hero is not None:
            assert hero['id'] == 42
        
        hero = nm.get_the_tallest_hero('-', True)
        assert hero is not None
        if hero is not None:
            assert hero['id'] == 409
        
        hero = nm.get_the_tallest_hero('-', False)
        assert hero is not None
        if hero is not None:
            assert hero['id'] == 287

        hero = nm.get_the_tallest_hero('not valid gender', True)
        assert hero is None

        hero = nm.get_the_tallest_hero('not valid gender', False)
        assert hero is None

'''






