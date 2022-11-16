# Project Documentation :-
## Milestone 1:-
### Task 1:-
Set up Github

## Milestone 2:-
### Task 1:-
Decide the website to work on i.e zoopla.co.uk  
Search for the property on the website and scrape the features of each property based on the following criteria:  
&emsp;&emsp;&emsp;Location- Coventry, West Midlands  
&emsp;&emsp;&emsp;Bedroom - min & max  
&emsp;&emsp;&emsp;Price - min & max  
&emsp;&emsp;&emsp;Property Type - Semi Detached, Detached, Terraced, Flats & Bunglows  
&emsp;&emsp;&emsp;Exclude - Retirements homes & Auction 

## Milestone 3:-
### Task 1:-
Create a Scraper class
- This class will contain all methods used to scrape data from the website - "https://www.zoopla.co.uk/".
### Task 2:-
Create a method **generate_data()** to navigate different pages of the website based on certain search criteria and capture property features, individual property links and image source.  

Create a different method to navigate the webpage using Selenium.
- Create **__search_data()** method to navigate the home page - "https://www.zoopla.co.uk/".
- Using Xpath, scrape search button and send location for search.
- Select filters (e.g., min/max beds, price range, property type) using Xpath and click Update to load the properties page.
### Task 3:-
Implement a method to bypass cookies
- Create **disable_popups()** method to clear alert and accept cookies,
- Add exception to handle the attribute error
### Task 4:-
Create a private method to get links of individual property in a page (using xpath @data-testid="regular-listings") and store it in a list - **property_url_list**
- Create **__get_property_list()**  method to generate a list of properties to scrape data from and return the list.
### Task 5:-
Run main body of code only within   if __name__ == "__main__" 
- Create if __name__ == "__main__" block and initialise the class within this block.

## Milstone 4:-
### Task 1:-
Create a method to retrieve text and image data from a individual property's link page.
- Create **__create_property_features()** method to scrape features of individual properties using XPATH.  
Features -  
&emsp;&emsp;&emsp;&emsp;_Property ID_,  
&emsp;&emsp;&emsp;&emsp;_Timestamp_,   
&emsp;&emsp;&emsp;&emsp;_Bedrooms_,   
&emsp;&emsp;&emsp;&emsp;_Bathroom_,  
&emsp;&emsp;&emsp;&emsp;_Reception_,  
&emsp;&emsp;&emsp;&emsp;_Property Images_,   
&emsp;&emsp;&emsp;&emsp;_Price_,  
&emsp;&emsp;&emsp;&emsp;_Address_ &  
&emsp;&emsp;&emsp;&emsp;_Description_   
and returns  dictionary of features of individual property added to the list.
### Task 2:-
Extract data and store in dictionary which maps feature name to feature value
- Create an empty dictionary to capture property features 
**property_data_dict = dict()**.
- Add Property ID, Timestamp, image source list, Price, Address, Bedrooms, Bathrooms, Reception &Description to the property_data_dict.
- Append property_data_dict to the list - **property_list**.
### Task 3:-
Save the raw data dictionaries locally 
- Create a method -> **create_data_folder()** to create a folder in the current directory.
- Pass the argument name(str)
- Create **save_json_data()** method to save individual property features as _data.json_.
### Task 4:-
Create a method  to find image links and download images if applicable and pass argument prop_url and prop_id. Return a list of image src links for a particular property
- Create **download_property_images()** to download images and save in the folder 
_raw_data/{property_id}/images_.

## Milestone 5:-
### Testing and code refactoring
### Task 1:-
Refactor and optimise current code
- Refactor the code based on best coding practice
### Task 2:-
Add docstring to all functions
- Add docstring to all the methods in Scraper class using Google format.
### Task 3:-
Create a unit test for each of the public method.
- Using pytest, test the public method:-  
&emsp;&emsp;&emsp;&emsp;**test_create_data_folder()**  
&emsp;&emsp;&emsp;&emsp;**test_get_driver()**  
&emsp;&emsp;&emsp;&emsp;**test_disable_popups()**  
&emsp;&emsp;&emsp;&emsp;**test_save_json_data()**  
&emsp;&emsp;&emsp;&emsp;**test_download_property_images()**  
&emsp;&emsp;&emsp;&emsp;**test_generate_data()**  
### Task 4:-
Create a file which runs all the tests 
- Create a file named _test_web_scraper.py_ to run all the tests
### Task 5:-
- Validate the unit tests are passing for all of the public methods

## Milestone 6:-
### Containerising the Scraper
### Task 1:-
Final refactoring of code
### Task 2:-
Check all tests are passing
### Task 3:-
Run the Scraper class in headless mode
### Task 4:-
Create a docker image which runs the Scraper
### Task 5:-
Push the container to Docker Hub

## Milestone 7:-
### Create a CI/CD pipeline to build & deploy Docker image to Docker hub
### Task 1:-
Setup Github secrets
### Task 2:-
Create Github actions

## Note :-

Please replace the respective driver as per OS in the path of the project directory - ./drivers

Chrome Driver Version 107.0.5304.62 - 

https://chromedriver.storage.googleapis.com/index.html?path=107.0.5304.62/

Firefox Driver Version 0.32.0 - 
https://github.com/mozilla/geckodriver/releases

