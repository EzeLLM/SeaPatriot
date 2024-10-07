import FuncHub
from InfoMaker import InfoMaker
from MapMaker import create_custom_map
import time
import json
import logging
import threading
import LLM
class SeaPatriot:
    def __init__(self, config):
        self.config = FuncHub.open_yaml(config, 'SeaPatriot')
        self.info_maker = InfoMaker(config)
        self.map_maker = create_custom_map
        self.info = self.info_maker.get_vessel_coordinates
        self.lock = threading.Lock()  # To ensure thread-safe access to the cache
        self.cache_file = 'Cache/cache_vessel_info.json'
        self.llm = LLM.Chatbot()
        self.refresh_thread = threading.Thread(target=self.refresh_cache, daemon=True)
        self.refresh_thread.start()

    def refresh_cache(self):
        while True:
            time.sleep(300)  # Sleep for 5 minutes
            self.update_cache()

    def update_cache(self):
        with self.lock:
            try:
                info = self.info()  # Fetch fresh vessel information
                if info:
                    self.map_maker(
                        lat=info['latitude'], lon=info['longitude'], address=info['address'],
                        status=info['status'], from_location=info['source'], to_location=info['destination'],
                        direction=info['course'], eta=info['eta'], last_report=info['last_report']
                    )
                    info['last_retrieved'] = time.time()
                    FuncHub.dump_to_json(self.cache_file, info)
                    print("Cache updated with fresh vessel info.")
            except Exception as e:
                print(f"Error updating cache: {e}")

    def main(self):
        with self.lock:
            try:
                cached = FuncHub.open_json(self.cache_file)
            except:
                cached = {'last_retrieved': 0}

            if time.time() - cached['last_retrieved'] < 300:
                print("Returning cached data")
                return cached
            else:
                print("No recent cache, returning stale data")
                return cached  # Return stale data if no recent cache available

    def chat(self, user_input, chat_id):
        si = json.dumps(self.main())
        print(si)
        return self.llm.chat(user_input, ship_info=si, chat_id=chat_id)


if __name__ == '__main__':
    config = 'dev/code/CONFIG/config.yml'
    app = SeaPatriot(config)
    print("Simple SeaPatriot Chatbot. Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = app.chat(user_input)
        print(f"Bot: {response}")
