import json
import os
import requests
import time

from time import gmtime, strftime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options as ChromeOption
from selenium.webdriver.firefox.options import Options as FirefoxOption


def get_driver(url: str, browser: str = "chrome") -> WebDriver:
    '''
        This function is used to open a url based on the browser.

        Args:
            url (str): url for scraping the data.
            browser (str): browser used for scraping.

        Returns:
            driver: webdriver.
    '''
    # Set up driver to get URL for scraping
    browser = browser.lower()
    if browser == "safari":
        # initializing webdriver for Safari with our options
        # instance of Options class allows to configure Headless Safari
        driver = webdriver.Safari()
    elif browser == "firefox":
        # initializing webdriver for Firefox with our options
        # instance of Options class allows to configure Headless Firefox
        options = FirefoxOption()
        # this parameter tells Firefox that should be run without UI (Headless)
        options.headless = True
        options.add_argument("window-size=1920x1080")
        driver = webdriver.Firefox(executable_path="./drivers/geckodriver", options=options)
    else:
        # initializing webdriver for Chrome with our options
        # instance of Options class allows to configure Headless Chrome
        options = ChromeOption()
        # this parameter tells Chrome that should be run without UI (Headless)
        options.headless = True
        options.add_argument("window-size=1920x1080")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path="./drivers/chromedriver", options=options)
    driver.get(url)
    time.sleep(5)

    return driver


def create_data_folder(name: str) -> None:

    '''

        This function is used to create a folder in the current directory.

        Args:
            name(str): this string is folder name
    '''
    # Create a raw_data parent folder
    if not os.path.exists(name):
        os.mkdir(name)


class Scraper():

    '''
        This class is used to scrape web data.

        Attributes:
            driver (str): driver to fetch url.
            property_url_list (list): the list of all properties' links.
            delay (int): the delay in sec.
            property_id (int): the list of id of all properties.
            timestamp (int): the timestamp when data is captured.
            image_src_list (list): the list of images links for a particular property.
            property_list (list): the list of all properties.
    '''

    def __init__(self, url: str, browser: str) -> None:

        '''
        This function is used to initialise variables for class object.

        Args:
            url (str): url for scraping the data.
            browser (str): browser used for scraping.
        '''
        self.driver = get_driver(url, browser)
        self.property_url_list = list()
        self.delay = 10
        self.property_id = 0
        self.timestamp = 0
        self.image_src_list = list()
        self.property_list = list()
        self.data_folder = "raw_data"


    def __search_data(self) -> None:
        '''
            This function is used to scrape data based on filter selection.
            Selection criteria :- 
            Minimum beds, Maximum beds, Price range, Property types and last 14 days 
            properties' list.

        '''

        # Pass search criteria 'Coventry, West Midlands' and 
        # search the list of available properties
        search_bar = self.driver.find_element(By.XPATH,"//input[@class='c-voGFy']")
        city_xpath = '//*[@placeholder="Enter a city, town or postcode"]'
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, city_xpath)))
        search_bar.send_keys("Coventry, West Midlands")
        search_bar.send_keys(Keys.RETURN)
        bed_xpath = '//*[@title="Any beds"]'
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, bed_xpath)))

        # Select max and min beds
        any_beds = self.driver.find_element(By.XPATH,"//*[@id='AnyBeds_testId']").click()
        self.driver.find_element(By.XPATH, value = "//*[@id='beds_min']/option[text()='2']").click()
        self.driver.find_element(By.XPATH, value = "//*[@id='beds_max']/option[text()='4']").click()
        price_xpath = "//*[@data-testid='any_price']"
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, price_xpath)))

        # Select max and min price
        any_price = self.driver.find_element(By.XPATH, value = "//*[@data-testid='any_price']").click()
        self.driver.find_element(By.XPATH, value = "//*[@id='price_min']/option[text()='£140,000']").click()
        self.driver.find_element(By.XPATH, value = "//*[@id='price_max']/option[text()='£350,000']").click()
        search_xpath = "//*[@data-testid='search-button']"
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, search_xpath)))

        # Select property type button(show all button)
        propertytype_xpath = "//*[@data-testid='PropertyType_testId']"
        self.driver.find_element(By.XPATH, value = propertytype_xpath).click()
        
        # Select check boxes - Semi-detached, Detached, Terraced, Flats & Bunglows
        self.driver.find_element(By.XPATH, value = "//*[@id='semi_detached-label']").click()
        self.driver.find_element(By.XPATH, value = "//*[@id='flats']").click()
        self.driver.find_element(By.XPATH, value = "//*[@id='detached']").click()
        self.driver.find_element(By.XPATH, value = "//*[@id='terraced']").click()
        self.driver.find_element(By.XPATH, value = "//*[@id='bungalow']").click()

        # Select filters to exclude - Retirements and Auction homes
        header_xpath = "//*[@data-testid='search-results-header_filters-button']"
        self.driver.find_element(By.XPATH, value = header_xpath).click()
        include_xpath = "//*[contains(text(), 'Include, exclude & show only')]"
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, include_xpath))).click()
        retirement_xpath = "//*[@id='retirement_homes_exclude']"
        WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.XPATH, retirement_xpath))).click()
        auction_xpath = "//*[@id='auction_exclude']"
        WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.XPATH, auction_xpath))).click()


        # Select filter - properties added in the last 14 days
        added_xpath = "//*[contains(text(), 'Added to site')]"
        WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, added_xpath))).click()
        added1_xpath = "//*[@id='added_14_days']"
        WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.XPATH, added1_xpath))).click()


        # Update results based on filter criteria 
        update_xpath = "//*[contains(text(), 'Update Results')]"
        WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.XPATH, update_xpath))).click()
        print("Filter Selection is done")


    def disable_popups(self) -> None:

        '''
            This function is used to clear alert and accept cookies.
        '''
        # Clear/accept cookies
        try:
            # This is the id of the frame
            self.driver.switch_to_frame('gdpr-consent-notice') 
            accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//*[@id="save"]')
            accept_cookies_button.click()

        except AttributeError: 
            # If you have the latest version of Selenium, the code above won't run 
            # because the "switch_to_frame" is deprecated
            self.driver.switch_to.frame('gdpr-consent-notice') 
            # This is the id of the frame
            accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//*[@id="save"]')
            accept_cookies_button.click()

        except Exception as e:
            # If there is no cookies button, print exception
            print("No cookies popup present - ", e) 

        # Clear alert window
        try:
            click_cross_button = self.driver.find_element(by=By.XPATH, value='//button[@data-testid="modal-close"]')
            click_cross_button.click()
        
        except Exception as e:
            # If there is no alert window, print exception
            print("No alert popup present - ", e) 


    def __get_property_list(self) -> list:
        '''
            This function is used to create list of properties to scrape data from.

            Returns:
                property_url_list (list): the list of all property's links.
        '''

        # Wait for 2 secs before scrapping property links
        time.sleep(2)
        # Capture elements containing regular listing - properties
        prop_container = self.driver.find_element(by=By.XPATH, value='//div[@data-testid="regular-listings"]')
        prop_list1 = prop_container.find_elements(by=By.XPATH, value='./div')
        # Scrape individual links for 25 properties
        for house_property in prop_list1:
            a_tag = house_property.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            self.property_url_list.append(link)

        print(f'There are {len(self.property_url_list)} properties in this page')
        #  return list of property
        return self.property_url_list
    

    def __create_property_features(self) -> list:

        '''
            This function is used to scrape features of individual properties.
            Features - 
            Property ID, Timestamp, Bedrooms, Bathroom, Reception, Property Images,
            Price, Address & Description

            Returns:
                property_list (list): dictionary of features of individual 
                    property added to the list.
        '''

        for link in self.property_url_list:
            # Create an empty dictionary to capture property features
            property_data_dict = dict()
            # Get the URL using chromedriver
            self.driver.get(link)
            time.sleep(1)
            # Add Property ID to the property_data_dict
            prop_id = link.split('details/')[1].split('/?search')[0]
            property_data_dict['Property ID'] = prop_id


            # Add Timestamp to the property_data_dict
            self.timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            property_data_dict['Timestamp'] = self.timestamp

            # Add Property Image (src link list) to the property_data_dict
            # __get_property_image_links function is called
            self.__get_property_image_links(link, prop_id)
            # Image source list is added to the dictionary property_data_dict
            property_data_dict['Property Images'] = self.image_src_list
            # Ressetting image_src_list for next property features; 
            # after it is added to the property_data_dict
            self.image_src_list = [] 

            # Add Price to the property_data_dict
            try:
                price = self.driver.find_element(by=By.XPATH, value='//p[@data-testid="price"]').text
                property_data_dict['Price'] = price
            except Exception as e:
                property_data_dict['Price'] = 'null'

            # Add Address to the property_data_dict
            try:
                address = self.driver.find_element(by=By.XPATH, value='//address[@data-testid="address-label"]').text
                property_data_dict['Address'] = address
            except Exception as e:
                property_data_dict['Address'] = 'null'

            # Add no of rooms to the property_data_dict - Beedrooms, Bathroom & Reception
            property_rooms = self.driver.find_elements(by=By.XPATH, value='//*[@class="c-PJLV c-PJLV-iiNveLf-css"]') 
            if len(property_rooms) > 0:
                try:
                    bedroom = self.driver.find_element(By.XPATH,  "//*[contains(@href, '#bedroom-medium')]/../../..")
                    property_data_dict['Bedrooms'] = bedroom.text
                except NoSuchElementException:
                    property_data_dict['Bedrooms'] = "Bedroom not mentioned"
                    
                try:
                    bathroom = self.driver.find_element(By.XPATH,  "//*[contains(@href, '#bathroom-medium')]/../../..") 
                    property_data_dict['Bathroom'] = bathroom.text
                except NoSuchElementException:
                    property_data_dict['Bathroom'] = "Bathroom not mentioned"
                try:
                    reception = self.driver.find_element(By.XPATH,  "//*[contains(@href, '#living-room-medium')]/../../..")     
                    property_data_dict['Reception'] = reception.text
                except NoSuchElementException:
                    property_data_dict['Reception'] = "Reception not mentioned"           
            else: 
                # Pass default parameters if no beds, bathrooms and reception are present
                property_data_dict['Bedrooms'] = "Bedroom not mentioned"
                property_data_dict['Bathroom'] = "Bathroom not mentioned"
                property_data_dict['Reception'] = "Reception not mentioned"

            # Add Description of the property to the property_data_dict
            try:
                div_tag = self.driver.find_element(by=By.XPATH, value='//div[@data-testid="truncated_text_container"]')
                span_tag = div_tag.find_element(by=By.XPATH, value='.//span')
                description = span_tag.text
                property_data_dict['Description'] = description
            except Exception as e:
                property_data_dict['Description'] = "null"

            # Append property_data_dict to the list property_list
            self.property_list.append(property_data_dict)
        return self.property_list    


    def generate_data(self, no_of_pages: int = 2) -> None:

        '''
            This function is used to generate web scrapping data.

            Args:
            no_of_pages (int): no of pages to scrape data from.

        '''
        # Clear cookies and popups
        try:
            self.disable_popups()
        except Exception as e:
            print(f"Exception - {e.msg}")
        # Call method to select filter criteria
        self.__search_data()
        # Clear cookies and popups
        try:
            self.disable_popups()
        except Exception as e:
            print(f"Exception - {e.msg}")   

        # Iterate through loop to get property links form n pages - range(n)
        for i in range(no_of_pages):
            self.__get_property_list()
            if i < (no_of_pages-1):
                pagination_xpath = "//li[@class='css-qhg1xn-PaginationItemPreviousAndNext-PaginationItemNext eaoxhri2']"
                try:
                    WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.XPATH, pagination_xpath))).click()
                except TimeoutException as e:
                    print(f"Exception - {e.msg}")
                time.sleep(2)
                try:
                    self.disable_popups()
                except Exception as e:
                    print(f"Exception - {e.msg}")                      
            else:
                pass
        # Call method to scrape features for each property 
        self.__create_property_features()


    def save_json_data(self) -> None:

        '''
            This function is used to save individual property features as data.json.

        '''
        # Create a folder by property id name
        for property in self.property_list:
            if not os.path.exists(f"./{self.data_folder}/{property['Property ID']}"):
                os.makedirs(f"./{self.data_folder}/{property['Property ID']}")

            # Property data to be written from property_list
            with open(f"./{self.data_folder}/{property['Property ID']}/data.json", "w") as outfile:
                json.dump(property, outfile, indent=4)


    def __get_property_image_links(self, prop_url: str, prop_id: str) -> list:

        '''
            This function is used to get image source links for all the images of a 
            particular property and save it in image_src_list.

           Args:
            prop_id(str): this string is property id
            prop_url(str): thi string is property url
           
           Returns:
                image_src_list (list): a list of image src links for a particular property
        '''

        # Scrape element using Selenium - all elements containing <img> tag and src attribute
        try:
            no_of_images_str = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, "//*[@data-testid='gallery-counter']"))).text
            no_of_images = int(no_of_images_str.split()[0].split('/')[1])
            if no_of_images > 1:

                # Iterate through <li> tag to get image src links and append it to image_src_list
                for _ in range(no_of_images): 
                    image_element = self.driver.find_element(By.XPATH, "//li[@aria-hidden='false' and @data-testid='gallery-image']")
                    image_src = image_element.find_element(by=By.TAG_NAME, value='img').get_attribute('src')
                    self.image_src_list.append(image_src)
                    # Click next button to capture images
                    try:
                        WebDriverWait(self.driver, self.delay).until(EC.element_to_be_clickable((By.XPATH, "//*[@data-testid='arrow_right']"))).click()
                    except TimeoutException as e:
                        print(f"Exception - {e.msg}")
                    time.sleep(1)
            else:
                image_element = self.driver.find_element(By.XPATH, "//li[@aria-hidden='false' and @data-testid='gallery-image']")
                image_src = image_element.find_element(by=By.TAG_NAME, value='img').get_attribute('src')
                self.image_src_list.append(image_src)
        except Exception as e:
            print(f"No images available for the property: Property ID - {prop_id}, \
                    Property Url - {prop_url}")

            
        return self.image_src_list


    def download_property_images(self) -> None:

        '''
            This function is used to download images and save in the folder.
        '''
        
        # Iterate through the property_list to get ID and image URL for download 
        # Change the name of the image downloaded to include ID,timestamp and image order.
        for property in self.property_list:
            # Create an image folder in the property id folder
            if not os.path.exists(f"./{self.data_folder}/{property['Property ID']}/images"):
                os.mkdir(f"./{self.data_folder}/{property['Property ID']}/images")
            # A variable to iterate through image order and concatenate it to the image name
            image_order=0
            # Iterate through links in the Property Images list to download
            # Save the downloaded file in the images folder
            for image in range(len(property['Property Images'])): 
                reponse = requests.get(property['Property Images'][image])
                if reponse.status_code == 200:
                    with open(f"{self.data_folder}/{property['Property ID']}/images/{strftime('%d%m%Y_%H%M%S', gmtime())}_{image_order+1}.jpg","wb") as file:
                        file.write(reponse.content)
                image_order +=1


if __name__ == "__main__":
    # Create an instance of the Scraper
    url = "https://www.zoopla.co.uk/"
    browser = "chrome"
    web_scraper = Scraper(url, browser)

    # Disable pop-ups
    web_scraper.disable_popups()

    # Method call to create the main raw_data folder
    data_folder_name = "raw_data"
    create_data_folder(name=data_folder_name)
    web_scraper.data_folder = data_folder_name

    # Method call for pagination and features capture
    no_of_pages = 2
    web_scraper.generate_data(no_of_pages)

    print("Data generated.")

    # Method call to save json data for each property
    web_scraper.save_json_data()

    print("Data saved - json")

    # Method call to save download images for each property
    web_scraper.download_property_images()
    print("Property images downloaded.")

    # Wait time of 10 sec below closing the browser
    time.sleep(10)

    # Close the browser
    web_scraper.driver.close()
