
import FuncHub
from InfoMaker import InfoMaker
from MapMaker import create_custom_map
import time
import json
import logging

class SeaPatriot:
    def __init__(self, config):
        self.config = FuncHub.open_yaml(config, 'SeaPatriot')
        self.info_maker = InfoMaker(config)
        self.map_maker = create_custom_map
        self.info = self.info_maker.get_vessel_coordinates
    def main(self):
        try:
            cached = FuncHub.open_json('Cache/cache_vessel_info.json') 
        except:
            cached = {'last_retrieved': 0}
        if time.time() - cached['last_retrieved'] < 300:
            
            return
        else:
            info = self.info()
        print(info)
        if info:
            self.map_maker(lat=info['latitude'], lon=info['longitude'], address=info['address'], status=info['status'], from_location=info['source'], to_location=info['destination'], direction=info['course'], eta=info['eta'], last_report=info['last_report'])
        else:
            print("No information available")
        info['last_retrieved'] = time.time()
        FuncHub.dump_to_json('Cache/cache_vessel_info.json',info)

if __name__ == '__main__':
    config = 'dev/code/CONFIG/config.yml'
    app = SeaPatriot(config)
    app.main()
        