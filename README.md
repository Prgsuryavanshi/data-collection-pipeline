# Project Documentation:-
## Milestone 1:-
### Task 1:-
Set up Github

## Milestone 2:-
### Task 1:-
Decide the website to work on i.e zoopla.co.uk 
Search for the property on the website and scrape the features of each property based on the following criteria:
location- coventry, westmidlands
Min. and max. number of bedroom
Price range
Address
Number of bathroom
Living room
Description

## Milestone 3:-
### Task 1:-
Create a Scraper class
- This class will contain all methods used to scrape data from the website("https://www.zoopla.co.uk/").
### Task 2:-
Using Selenium, create different methods to navigate the webpage.
- Create search_data() method to navigate the home page ("https://www.zoopla.co.uk/")
- Using Xpath scrape search button and send town name.
- Select filter like(min/max beds, price, property type) using Xpath and update filters to update the properties page.
### Task 3:-
Implement a method to bypass cookies
- Create disable_popups() method to clear alert and accept cookies, and add one exception to handle the attribute error
### Task 4:-
Create a method to get links to each page where the details where details are found and store in the list
- Create get_property_list() method to create list of properties to scrape data from and returns the list of all property's links.
### Task 5:-
Run main body of code only within if __name__ == "__main__"
- Create if __name__ == "__main__" block and initialise the class within this block.

## Milstone 4:-
### Task 1:-
Create a function to retrieve text and image data from a single details page
- Create, create_property_features() method to scrape features of individual properties using XPATH.
Features - 
    Property ID, Timestamp, Bedrooms, Bathroom, Reception, Property Images,
    Price, Address & Description
and returns  dictionary of features of individual property added to the list.
### Task 2:-
Extract data and store in dictionary which maps feature name to feature value
- Create an empty dictionary to capture property features 
property_data_dict = dict().
- Add Property ID, Timestamp, Image source list, Price, Address, Bedrooms, Bathrooms, Reception, Description to the property_data_dict.
- Append property_data_dict to the list property_list.
### Task 3:-
Save the raw data dictionaries locally 
- create a method names -> create_data_folder() to create a folder in the current directory.
- Pass the argument name(str)
- Create save_json_data() method to save individual property features as data.json.
### Task 4:-
Create a method to find image links and download images if applicable
- Create download_property_images to download images and save in the folder 
raw_data/{property_id}/images.

## Milestone 5:-
### Task 1:-
Refactor and optimise current code
- Refactor the code based on best coding practice
### Task 2:-
Add docstring to all functions
- Add docstring to all the methods in Scraper class using Google format.
### Task 3:-
Create a unit test for each of the public method.
- Using pytest test the public method:- 
test_create_data_folder()
test_get_driver()
test_disable_popups()
test_save_json_data()
test_download_property_images()
test_generate_data()
### Task 4:-
Create a file which runs all of the tests 
- Crete a file named test_web_scraper.py to run all the tests
### Task 5:-
- Test unittest are paasing for all of the public methods

## Milestone 6:-
### Task 1:-
Containerising the Scraper
### Task 2:-
Check all tests are paasing

