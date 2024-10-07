from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import time
import os
from webdriver_manager.chrome import ChromeDriverManager
import FuncHub
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError



BASE_URL = "https://www.vesselfinder.com/?imo=" # This script is designed to work with VesselFinder and NOT MarineTraffic or any other website
class InfoMaker:
    def __init__(self,config):
        self.config = FuncHub.open_yaml(config,'InfoMaker')
        self.IMMO = self.config['IMMO']
        self.url =  BASE_URL + str(self.IMMO)


    def get_vessel_coordinates(self):
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
        except WebDriverException as e:
            print(f"Error setting up WebDriver: {e}")
            return None
        try:
            driver.get(self.url)
            time.sleep(10)
            def safe_get_text(xpath):
                try:
                    element = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    return element.text.strip()
                except TimeoutException:
                    print(f"Element not found: {xpath}")
                    return None
            latitude = safe_get_text("/html/body/main/div[2]/div[1]/div[6]/div[3]/div[3]/div/div[1]/div[2]")
            longitude = safe_get_text("/html/body/main/div[2]/div[1]/div[6]/div[3]/div[3]/div/div[1]/div[5]")
            course = safe_get_text("/html/body/main/div[3]/div[1]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]")
            source_ = safe_get_text("/html/body/main/div[3]/div[1]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[3]/div/div/div[1]")
            destination_ = safe_get_text("/html/body/main/div[3]/div[1]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div[1]")
            speed_ = safe_get_text("/html/body/main/div[3]/div[1]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]")
            status_ = safe_get_text("/html/body/main/div[3]/div[1]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div/div")
            eta = safe_get_text("/html/body/main/div[3]/div[1]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div[2]/span[1]")
            last_report = safe_get_text("/html/body/main/div[3]/div[1]/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]")
            try:
                latitude = float(latitude) if latitude else None
                longitude = float(longitude) if longitude else None
                course = float(course[:-1]) if course else None
            except ValueError:
                print("Could not convert coordinates to float")

            return {"latitude": latitude, 
                    "longitude": longitude,
                    "course": course,
                    "source": source_,
                    "destination": destination_,
                    "speed": speed_,
                    "status": status_,
                    "address": self.get_vague_address(latitude, longitude),
                    "eta": eta + (" (!)" if status_ == "Moored" else ""),
                    "last_report": last_report
                    }
        

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        finally:
            # Close the browser
            driver.quit()
    def get_vague_address(self,latitude, longitude):
        geolocator = Nominatim(user_agent="SeaPatriotApp")
        
        try:
            location = geolocator.reverse((latitude, longitude), exactly_one=True, timeout=10, language="en")
            
            if location:
                address_details = location.raw.get('address', {})
                
                # Check for sea or ocean
                if 'sea' in address_details:
                    return f"{address_details['sea']}, {address_details.get('country', '')}"
                elif 'ocean' in address_details:
                    return f"{address_details['ocean']}, {address_details.get('country', '')}"
                
                # Check for other water bodies
                water_bodies = ['bay', 'strait', 'channel', 'gulf']
                for body in water_bodies:
                    if body in address_details:
                        return f"{address_details[body]}, {address_details.get('country', '')}"
                
                # Check for city
                if 'city' in address_details:
                    return f"{address_details['city']}, {address_details.get('country', '')}"
                elif 'town' in address_details:
                    return f"{address_details['town']}, {address_details.get('country', '')}"
                elif 'village' in address_details:
                    return f"{address_details['village']}, {address_details.get('country', '')}"
                
                # Fallback to state/region and country
                state = address_details.get('state', '')
                country = address_details.get('country', '')
                if state and country:
                    return f"{state}, {country}"
                elif country:
                    return country
            
            return "Unknown location"
        except:
            return "Unknown location, Contact dev"

# Usage
if __name__ == "__main__":
    config = 'dev/code/CONFIG/config.yml'
    info_maker = InfoMaker(config)
    vessel_info = info_maker.get_vessel_coordinates()
    print(vessel_info)