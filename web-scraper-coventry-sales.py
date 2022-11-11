import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class Scraper():
    def __init__(self):
        '''
    Instance variables i.e URL, link_list and dict_properties are declared 
    inside the constructor which is the __init__method.
    '''
        self.URL = "https://www.zoopla.co.uk/for-sale/property/coventry/?q=Coventry%2C%20West%20Midlands&search_source=home"
        self.link_list = []
        self.dict_properties = {'Price': [], 'Address': [], 'Bedrooms': [], 'Bathroom': [], 'Reception': [], 'Description': []}
    

    def get_link(self,URL):
        '''
    webdriver is used to writing the action, here we picked the browser(Chrome)
    and opened a website by .get() and waited for 5 sec. to load the website 
    properly, then clear_alert method is called.
     '''
        self.driver = webdriver.Chrome()
        self.driver.get(URL)       
        time.sleep(5)
        self.clear_alert()
    
    def clear_alert(self):

        '''
            try block is for clearing the cookies which will come after webpage
            gets loaded.
            except is for clearing attribute error
            another except is for paas when there will be no cookies.

            Another try block is for clearing the pop-op message by hitting cross button
            if it will not found then will paas.
        '''
        try:
            self.driver.switch_to_frame('gdpr-consent-notice') # This is the id of the frame
            accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//*[@id="save"]')
            accept_cookies_button.click()

        except AttributeError: # If you have the latest version of Selenium, the code above won't run because the "switch_to_frame" is deprecated
            self.driver.switch_to.frame('gdpr-consent-notice') # This is the id of the frame
            accept_cookies_button = self.driver.find_element(by=By.XPATH, value='//*[@id="save"]')
            accept_cookies_button.click()

        except:
            pass # If there is no cookies button, we won't find it, so we can pass

        try:
            click_cross_button = self.driver.find_element(by=By.XPATH, value='//button[@data-testid="modal-close"]')
            click_cross_button.click()
        
        except:
            pass
    
    
    def prop_list(self):
        '''
    prop_container represent the list of properties on the website, to get
    all the <div> tag inside
    for all the occurance of this xpath using find_elements by xpath store
    in the prop_list1(list of the link of the properties).
    Now using for loop will iterate through this list and append it to the 
    instance variable link_list.
    using formatted print statement gives the count of properties in the page
    '''
        time.sleep(2)
        prop_container = self.driver.find_element(by=By.XPATH, value='//div[@data-testid="regular-listings"]') # XPath corresponding to the Container a_tag = house_property.find_element(by=By.TAG_NAME, value='a')
        prop_list1 = prop_container.find_elements(by=By.XPATH, value='./div')
        for house_property in prop_list1:
            a_tag = house_property.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            self.link_list.append(link)
        print(f'There are {len(self.link_list)} properties in this page')
        #print(self.link_list)
        #self.link = a_tag.get_attribute('href')
        #print(self.link)
        return self.link_list
    
    def prop(self):
        '''
    using for loop it will iterate through each link to extract the 
    data we were interested on (Price, Address,Bedrooms, Bathroom, Reception 
    and Description)
    using try, except block it will check the all features and will extend
    the element and append it to the instance variable dict_properties 
    '''
        for link in self.link_list:
            self.driver.get(link)
            try:
                price = self.driver.find_element(by=By.XPATH, value='//p[@data-testid="price"]').text
                self.dict_properties['Price'].append(price)
            except:
                self.dict_properties['Price'].append("null")
            try:
                address = self.driver.find_element(by=By.XPATH, value='//address[@data-testid="address-label"]').text
                self.dict_properties['Address'].append(address)
            except:
                self.dict_properties['Address'].append("null")
    
            room = self.driver.find_elements(by=By.XPATH, value='//div[@class="c-cbuYEU c-cbuYEU-egQFzo-isAnAttribute-true c-cbuYEU-iPJLV-css"]') # Change this xpath with the xpath the current page has in their properties
            try:
                if self.driver.find_element(By.XPATH,  "//*[contains(@href, '#bedroom-medium')]"):
                    print('bed')
                    print(room[0].text)
                    self.dict_properties['Bedrooms'].append(room[0].text)
            except:
                print('no bed')
            try: 
                if self.driver.find_element(By.XPATH,  "//*[contains(@href, '#bathroom-medium')]"):
                    print('bath')
                    print(room[1].text)
                    self.dict_properties['Bathroom'].append(room[1].text)
            except:
                print('no bath')
            try:
                if self.driver.find_element(By.XPATH,  "//*[contains(@href, '#living-room-medium')]"):
                    print('living')
                    print(room[2].text)
                    self.dict_properties['Reception'].append(room[2].text)
            except:
                print('no living')            
            try:
                div_tag = self.driver.find_element(by=By.XPATH, value='//div[@data-testid="truncated_text_container"]')
                span_tag = div_tag.find_element(by=By.XPATH, value='.//span')
                description = span_tag.text
                self.dict_properties['Description'].append(description)
            except:
                self.dict_properties['Description'].append("null")
                #print(dict_properties)
            time.sleep(3)
        return(self.dict_properties)    
    
    def pagination(self):
        '''
    calling get_link method to open a webpage and clearing the cookies and alert as well
    using for loop will it will open the pages one after another 2 represets no. of 
    pages, it will go 0 to 1.
    Home webpage has already been open by calling get_link method
    for loop:-
    0 in range(2)
    then, prop_list method will be called where list of the link of the properties
    will be appended in link_list.
    if condition will check i.e 0<1, then it will click to the next page
    clear_alert() will be called to clear the cookies and alert, after that
    prop() method will be called to extract all the features of the properties
    '''
        self.get_link(self.URL)
        for i in range(2):
            self.prop_list()
            if i < 1:
                next_page = self.driver.find_element(by=By.XPATH, value='//li[@class="css-qhg1xn-PaginationItemPreviousAndNext-PaginationItemNext eaoxhri2"]')
                next_page.click()
                time.sleep(2)
                self.clear_alert()
                time.sleep(2)
            else:
                pass
        self.prop()
        return
    

    def csv_output(self):
        '''
    It will open the CSV file for writing (w mode) by using the 
    open() function.
    Created a CSV writer object by calling the writer() function of the csv module.
    write data to CSV file by calling the writerow() or writerows() method of the CSV writer object.
    '''
        with open("output.csv", "w", newline="") as outfile:

            # pass the csv file to csv.writer function.
            writer = csv.writer(outfile)
        
            # pass the dictionary keys to writerow
            # function to frame the columns of the csv file
            writer.writerow(self.dict_properties.keys())
        
            # make use of writerows function to append
            # the remaining values to the corresponding
            # columns using zip function.
            writer.writerows(zip(*self.dict_properties.values()))
    

if __name__ == "__main__":
    webdata = Scraper()
    '''
    Created an instance of the Scraper class
    '''
    webdata.pagination()
    '''
    instance method(pagination) call
    '''
    webdata.csv_output()
    '''
    Open a csv file with all the data as output
    '''
    time.sleep(10)
    webdata.driver.close()
    '''
    After completion of task webpage will be closed
    '''

