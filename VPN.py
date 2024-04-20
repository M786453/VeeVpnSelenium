from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class VPN:

    def __init__(self):

        self._setup_driver()

        time.sleep(10)

        self._load_extension_page()

        self._skip_onboarding()

        self.free_locations = ['Local'] + self._get_free_locations()

        self.location_index = 0
    
    def _setup_driver(self):

        options = webdriver.ChromeOptions()

        options.add_extension('extension/vpn.crx')

        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")

        self.driver = webdriver.Chrome(options=options)

    def _load_extension_page(self):

        self.driver.switch_to.window(self.driver.window_handles[1]) # Switch to the new tab

        extension_url = 'chrome-extension://majdfhpaihoncoakbjgbdhglocklcgno/html/foreground.html'

        self.driver.get(extension_url)

        time.sleep(5)

        self.dismiss_add() # Dismiss add if shows up

    def _skip_onboarding(self):

        # Skip onboarding steps

        self.driver.find_element(By.XPATH, "//button[@class='next']").click()

        time.sleep(5)

        self.dismiss_add() # Dismiss add if shows up

        self.driver.find_element(By.XPATH, "//button[@class='next']").click()

        time.sleep(5)

        self.dismiss_add() # Dismiss add if shows up

    def _get_free_locations(self):

        free_locations = []

        time.sleep(5)

        self.dismiss_add() # Dismiss add if shows up

        self.driver.find_element(By.CLASS_NAME, 'current-region-upper-block').click()

        time.sleep(5)

        self.dismiss_add() # Dismiss add if shows up

        all_locations_div = self.driver.find_element(By.ID, 'region-list')

        free_locations_div = all_locations_div.find_element(By.ID, 'region-list')

        free_locations_buttons = free_locations_div.find_elements(By.XPATH, "div[@role='button']")

        for location in free_locations_buttons:

            if "region-folder" in location.get_attribute('class'):

                location.click() # Unpack the heirarchy of the location folder

                time.sleep(5)

                free_locations.extend(location.text.split('\n')[1:])
            
            else:

                free_locations.append(location.text.split('\n')[0])

        self.driver.find_element(By.CLASS_NAME, 'veepn-back-button-wrapper').click() # Get back to home page of VPN

        time.sleep(5)

        self.dismiss_add() # Dismiss add if shows up
        
        return free_locations
    
    def _choose_free_location(self):

        time.sleep(5)

        self.dismiss_add()

        self.driver.find_element(By.CLASS_NAME, 'current-region-upper-block').click() # open locations page

        time.sleep(5)

        self.dismiss_add()

        all_locations_div = self.driver.find_element(By.ID, 'region-list') # all locations divs

        free_locations_div = all_locations_div.find_element(By.ID, 'region-list') # div containing only free locations

        time.sleep(5)

        free_locations_buttons = []

        try:

            free_locations_buttons = free_locations_div.find_elements(By.XPATH, "//div[contains(@class,'region-item')]") # getting all free locations buttons

        except Exception as e:

            print("Free locations buttons not found.")

        print('Checking locations:', len(free_locations_buttons))

        for location in free_locations_buttons:

            print("Checking location text:", location.text)
            
            if self.free_locations[self.location_index] == location.text.split('\n')[0]: # if location text is equal to the text of chosen location, then select the location

                location.click()

                print(f"Location {self.free_locations[self.location_index]} Selected")

                time.sleep(5)

                break
        
        self.dismiss_add()

    def dismiss_add(self):

        try:

            self.driver.find_element(By.XPATH, "//button[contains(@class, 'get-access-button')]").click() # Click 'Get Access' button (it causes open new tab)

            self.driver.switch_to.window(self.driver.window_handles[2]) # Switch to new tab

            self.driver.close() # Close the tab

            self.driver.switch_to.window(self.driver.window_handles[1]) # Switch to pervious tab
        
        except Exception as e:

            print("Get access button not found.")

    def connect(self):

        time.sleep(5)

        self.dismiss_add()

        button = self.driver.find_element(By.ID, 'mainBtn')

        if button.get_attribute('class') == 'disconnected':
            print("Connecting to VPN...")
            self.driver.find_element(By.CLASS_NAME, 'button-clicker').click() # Connect VPN

        time.sleep(5)

        self.dismiss_add()

    def disconnect(self):

        self.driver.switch_to.window(self.driver.window_handles[1]) # switch to vpn tab

        time.sleep(5)

        self.dismiss_add()

        button = self.driver.find_element(By.ID, 'mainBtn')

        if button.get_attribute('class') == 'connected':
            print("Disconnecting existing connection")
            self.driver.find_element(By.CLASS_NAME, 'button-clicker').click() # Disconnect VPN

        time.sleep(5)

        self.dismiss_add()

    def rotate_connection(self):

        self.driver.switch_to.window(self.driver.window_handles[1]) # switch to vpn tab

        self.location_index += 1

        if self.location_index == 6:

            self.location_index = 0

            return

        time.sleep(5)

        try:
            self._choose_free_location()
        except:
            self._load_extension_page()
            self._choose_free_location()

        try:
            self.connect()
        except:
            self._load_extension_page()
            self.connect()

        time.sleep(5)