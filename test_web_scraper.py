import os
import time
import json
import shutil
import unittest 
import pytest
import requests
import webscraper_property_sales as ws
from selenium import webdriver
from unittest.mock import patch, mock_open



def test_create_data_folder():
    '''
        This function is used to test the create_data_folder and 
        assert functionality is used to validate the presence of 
        directory before and after.
    '''
    # Create a temporary folder
    folder_name = "temp"
    # Check if the folder is present
    is_exist = os.path.exists(folder_name)
    assert False == is_exist
    # Call the method to create a folder
    ws.create_data_folder(folder_name)
    is_exist = os.path.exists(folder_name)
    assert True == is_exist
    # Remove the folder after test
    os.rmdir(folder_name)

def test_get_driver():
    '''
        This function is used to test the get_driver() function and 
        return value is compared with the expected value.
    '''
    # Pass a default webpage to test driver 
    test_url = "https://www.google.com/"
    browsers = ["chrome", "firefox", "safari"]
    # Test the method by passing different browser and asserting 
    # the return value with the expected value.
    for browser in browsers:
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
web_scrap = ws.Scraper(test_url, browser)
expected_output = {
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



def test_disable_popups():
    '''
        This function is used to test disable_popups method
        by taking screenshot of the webpage before and after 
        pops are disabled.
    '''
    # Save the screenshot of webpage before disable_popups is called
    web_scrap.driver.get_screenshot_as_file('./test_data/before popup disable_screenshot.png')
    time.sleep(1)
    # Call the method for unit testing
    web_scrap.disable_popups()
    time.sleep(1)
    # Save the screenshot of webpage after disable_popups is called
    web_scrap.driver.get_screenshot_as_file('./test_data/after popup disable_screenshot.png')
    #web_scrap.driver.close()

def test_save_json_data():
    '''
        This function is used to test save_json_data() method.
        Predifined dict is appended to the property_list and the data.json 
        file is compared with the expected value for unt testing.
    '''
    # Check the presence of folder before unit test
    assert os.path.exists("raw_data/0000000/data.json") == False
    #  Append the property_list with expected value.
    web_scrap.property_list.append(expected_output)
    # Call save_json_data() method for unit testing
    web_scrap.save_json_data()
    # Check the presence of folder after method call
    assert os.path.exists("raw_data/0000000/data.json") == True
    with open('./raw_data/0000000/data.json', 'r') as file:
        actual_output = json.load(file)
    # Assert the expected value with the data from json 
    # file created for new property
    assert expected_output == actual_output
    # Delete the folder created
    shutil.rmtree('./raw_data/0000000')
    # Remove the data added to the property_list for unit testing
    web_scrap.property_list.pop()
    #web_scrap.driver.close()

def test_download_property_images():
    '''
        This function is used to test download_property_images() method.
        Predifined url is used to test the download feature of the method
        and the bytearray is compared with the expected output.
    '''
    # Check the presence of folder before unit testing
    assert os.path.exists("raw_data/0000000/images") == False
    if not os.path.exists('raw_data/0000000/'):
        os.mkdir('raw_data/0000000/')
    # Appended expected output to the property_list
    web_scrap.property_list.append(expected_output)

    # TODO: multiple image download option needed?

    # Get the bytearray of image 
    for image in range(len(expected_output['Property Images'])):
        reponse = requests.get(expected_output['Property Images'][image])
        if reponse.status_code == 200:
            with open(f"./test_data/test_image{image}.jpg","wb") as file:
                file.write(reponse.content)
            with open(f"./test_data/test_image{image}.jpg", "rb") as img:
                f = img.read()
                b_expected = bytearray(f)
    
    # Call method for unit testing
    web_scrap.download_property_images()
    # Get the bytearray of the image downloaded during method call
    infile = os.listdir("raw_data/0000000/images/")
    path = os.path.join("raw_data/0000000/images/", str(infile[0]))
    with open(path, "rb") as img_output:
        f = img_output.read()
        b_output = bytearray(f)
    # Assert bytearray of test and downloaded image
    assert os.path.exists("raw_data/0000000/images") == True
    assert b_expected == b_output
    # Delete the folder created
    shutil.rmtree('./raw_data/0000000')
    # Remove the data added to property_list for testing
    web_scrap.property_list.pop()
    #web_scrap.driver.close()


def test_generate_data():
    '''
        This function is used to test generate_data().
        The length of property_list and property_url_list is compared 
        with expected value to test the method call.
    '''
    #  Get the length of property_list and property_url_list
    before_len_of_list = len(web_scrap.property_list)
    print(before_len_of_list)

    before_len_of_url_list = len(web_scrap.property_url_list)
    print(before_len_of_url_list)
    # Assert the length before method call
    assert before_len_of_url_list == 0
    assert before_len_of_list == 0
    # Call method for unit testing
    web_scrap.generate_data()
    # Get the length of property_list and property_url_list
    after_len_of_list = len(web_scrap.property_list)
    print(after_len_of_list)
    
    after_len_of_url_list = len(web_scrap.property_url_list)
    print(after_len_of_url_list)
    # Assert the length after method call
    assert after_len_of_url_list == 50
    assert after_len_of_list == 50

    web_scrap.driver.close()


class TestWebscraper(unittest.TestCase):
    # Initialize the scenario for your test
    def setUp(self):
        test_url = "https://www.zoopla.co.uk/"
        browser = "chrome"
        web_scrap = ws.Scraper(test_url, browser)
        expected_output = {
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

    # Finish 
    def tearDown(self):
        web_scrap.driver.close()