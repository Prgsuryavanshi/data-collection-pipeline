import os
import time
import json
import shutil
import pytest
import requests
import webscraper_property_sales as ws
from selenium import webdriver
from unittest.mock import patch, mock_open


@pytest.mark.parametrize("folder_name", ["temp"])
def test_create_data_folder(folder_name):
    '''
        This function is used to test the create_data_folder and 
        assert functionality is used to validate the presence of 
        directory before and after.
    '''
    # Check if the folder is present
    is_exist = os.path.exists(folder_name)
    assert False == is_exist
    # Call the method to create a folder
    ws.create_data_folder(folder_name)
    is_exist = os.path.exists(folder_name)
    assert True == is_exist
    # Remove the folder after test
    os.rmdir(folder_name)

@pytest.mark.parametrize("browser", ["chrome", "safari", "firefox"])
@pytest.mark.parametrize("test_url", ["https://www.google.com/"])
def test_get_driver(browser,test_url):
    '''
        This function is used to test the get_driver() function and 
        return value is compared with the expected value.
    '''

    # Test the method by passing browser name and asserting 
    # the return value with the expected value.
    driver = ws.get_driver(test_url, browser)
    if browser == "chrome":
        assert True == isinstance(driver, webdriver.Chrome)
        driver.close()
    elif browser == "firefox":
        assert True == isinstance(driver, webdriver.Firefox)
        driver.close()
    else:           
        assert True == isinstance(driver, webdriver.Safari)
        driver.close()

test_url = "https://www.zoopla.co.uk/"
browser = "chrome"
property_test_data = {
    "Property ID": "0000000",
    "Timestamp": "2022-11-11 00:00:00",
    "Property Images": [
        "https://lid.zoocdn.com/u/2400/1800/c5a70908b088053d271794fc503b8da67b698250.jpg"
    ],
    "Price": "000,000",
    "Address": "Coventry",
    "Bedrooms": "0 beds",
    "Bathroom": "0 baths",
    "Reception": "0 reception",
    "Description": " Test Description"
    }


@pytest.mark.parametrize("browser", ["chrome"])
@pytest.mark.parametrize("test_url", ["https://www.zoopla.co.uk/"])
def test_disable_popups(browser,test_url):
    '''
        This function is used to test disable_popups method
        by taking screenshot of the webpage before and after 
        pops are disabled.
    '''
    # Save the screenshot of webpage before disable_popups is called
    web_scraper = ws.Scraper(test_url, browser)
    web_scraper.driver.get_screenshot_as_file('./test_data/before_popup_disable_screenshot.png')
    time.sleep(1)
    # Call the method for unit testing
    web_scraper.disable_popups()
    time.sleep(1)
    # Save the screenshot of webpage after disable_popups is called
    web_scraper.driver.get_screenshot_as_file('./test_data/after_popup_disable_screenshot.png')
    web_scraper.driver.close()

@pytest.mark.parametrize("browser", ["chrome"])
@pytest.mark.parametrize("test_url", ["https://www.zoopla.co.uk/"])
def test_save_json_data(browser,test_url):
    '''
        This function is used to test save_json_data() method.
        Predifined dict is appended to the property_list and the data.json 
        file is compared with the expected value for unt testing.
    '''
    web_scraper = ws.Scraper(test_url, browser)
    #  Append the property_list with expected value.
    web_scraper.property_list.append(property_test_data)
    web_scraper.data_folder = "test_data/actual"
    # Call save_json_data() method for unit testing
    web_scraper.save_json_data()
    # Check the presence of folder after method call
    assert os.path.exists(f"{web_scraper.data_folder}/0000000/data.json") == True
    with open(f"{web_scraper.data_folder}/0000000/data.json", 'r') as file:
        actual_output = json.load(file)
    with open(f"test_data/expected/data.json", 'r') as file:
        expected_output = json.load(file)
    # Assert the expected value with the data from json 
    # file created for new property
    assert expected_output == actual_output
    web_scraper.driver.close()

@pytest.mark.parametrize("browser", ["chrome"])
@pytest.mark.parametrize("test_url", ["https://www.zoopla.co.uk/"])
def test_download_property_images(browser,test_url):
    '''
        This function is used to test download_property_images() method.
        Predifined url is used to test the download feature of the method
        and the bytearray is compared with the expected output.
    '''
    web_scraper = ws.Scraper(test_url, browser)

    # assert os.path.exists("test_data/actual/0000000/images") == False
    if os.path.exists('test_data/actual/0000000/images'):
        # Check the presence of folder before unit testing
        shutil.rmtree("./test_data/actual/0000000/images")

    os.makedirs('test_data/actual/0000000/images')
    # Appended expected output to the property_list
    web_scraper.property_list.append(property_test_data)
    web_scraper.data_folder = "test_data/actual"

    # Get the bytearray of image 
    for image in range(len(property_test_data['Property Images'])):
        reponse = requests.get(property_test_data['Property Images'][image])
        if reponse.status_code == 200:
            with open(f"./test_data/expected/test_image{image}.jpg","wb") as file:
                file.write(reponse.content)
            with open(f"./test_data/expected/test_image{image}.jpg", "rb") as img:
                f = img.read()
                b_expected = bytearray(f)
    
    # Call method for unit testing
    web_scraper.download_property_images()
    # Get the bytearray of the image downloaded during method call
    infile = os.listdir("test_data/actual/0000000/images/")
    path = os.path.join("test_data/actual/0000000/images/", str(infile[0]))
    with open(path, "rb") as img_output:
        f = img_output.read()
        b_output = bytearray(f)
    # Assert bytearray of test and downloaded image
    assert os.path.exists("test_data/actual/0000000/images") == True
    assert b_expected == b_output

    web_scraper.driver.close()

@pytest.mark.parametrize("browser", ["chrome"])
@pytest.mark.parametrize("test_url", ["https://www.zoopla.co.uk/"])
def test_generate_data(browser,test_url):
    '''
        This function is used to test generate_data().
        The length of property_list and property_url_list is compared 
        with expected value to test the method call.
    '''
    web_scraper = ws.Scraper(test_url, browser)

    web_scraper.generate_data()
    # Get the length of property_list and property_url_list
    len_of_list = len(web_scraper.property_list)
    len_of_url_list = len(web_scraper.property_url_list)
    # Assert the length after method call
    assert len_of_url_list > 0
    assert len_of_list > 0

    web_scraper.driver.close()

