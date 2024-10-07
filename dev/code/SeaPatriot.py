
import FuncHub
from InfoMaker import InfoMaker
from MapMaker import create_custom_map
import time
import json
import logging
import LLM
class SeaPatriot:
    def __init__(self, config):
        self.config = FuncHub.open_yaml(config, 'SeaPatriot')
        self.info_maker = InfoMaker(config)
        self.map_maker = create_custom_map
        self.info = self.info_maker.get_vessel_coordinates
        self.llm = LLM.Chatbot()
    def main(self):
        try:
            cached = FuncHub.open_json('Cache/cache_vessel_info.json') 
        except:
            cached = {'last_retrieved': 0}
        if time.time() - cached['last_retrieved'] < 300:
            return cached
        else:
            info = self.info()
        print(info)
        if info:
            self.map_maker(lat=info['latitude'], lon=info['longitude'], address=info['address'], status=info['status'], from_location=info['source'], to_location=info['destination'], direction=info['course'], eta=info['eta'], last_report=info['last_report'])
        else:
            print("No information available")
        info['last_retrieved'] = time.time()
        FuncHub.dump_to_json('Cache/cache_vessel_info.json',info)
        return info
    def chat(self,user_input):
        si = json.dumps(self.main())
        print(si)
        return self.llm.chat(user_input,ship_info=si)


if __name__ == '__main__':
    config = 'dev/code/CONFIG/config.yml'
    app = SeaPatriot(config)
    app.main()
    print("Simple SeaPatriot Chatbot. Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = app.chat(user_input)
        print(f"Bot: {response}")        