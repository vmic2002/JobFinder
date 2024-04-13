"""
this script deals with applying to job posting once we are already on the job posting's website
"""
from PARAMS import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep

def scrollDown(driver, scroll_amount, div_element):
    #this func might be in the wrong file, no need to scroll down once on job posting site
    driver.execute_script("arguments[0].scrollTop += "+str(scroll_amount)+";", div_element)

def inputFieldFromOptions(driver, sol, by, possibleElementIds):
    for elementId in possibleElementIds:
        if inputField(driver, elementId, sol, by):
            #print("\tInput field successfully...")
            return True
    return False

def inputField(driver, elementId, sol, by):
    timeout = 0.5 # in seconds
    try:
        # Wait for the element to appear
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, elementId))
        )
        # If the element appears within timeout seconds, perform further actions
        # For example, send keys to the input field
        element.send_keys(sol)
        return True
    except TimeoutException as e:
        print("Element '"+elementId+"' did not appear within "+str(timeout)+" seconds. Moving on.")
        return False

def uploadResume(driver):
    # Find and click on the attach button based on aria-describedby attribute
    #old_window_ = driver.current_window_handle
    attach_button = driver.find_element(By.XPATH, "//button[@aria-describedby='resume-allowable-file-types']")
    attach_button.click()
    #once clicked, maybe will have to wait for user to click on resume and hit enter
    #attach_button.send_keys(resumeFilePath)#TODO NOT WORKING
    # Wait for a few seconds for the file dialog box to appear
    sleep(2)  # Adjust the delay as needed


def tryApplyingAutomatically(driver):
    #print("URL JOB POSTING"+driver.current_url)
    #TODO COULD GET JOB POSTINGS FROM ZIPRECRUITER, INDEED ETC (for now using only linkedin to get job postings) DOESNT MATTER HOW THE JOB POSTING IS RETRIEVED THIS FUNCTION WILL WORK AS LONG AS JOB POSTING FOLLOWS STANDARD
    possibleFieldIdFirstName = ["first_name","job_application[first_name]","field-first_name"]
    possibleFieldIdLastName = ["last_name"]
    possibleFieldIdEmailAddress = ["email"]
    possibleFieldIdPhoneNumber = ["phone"]
    possibleFieldIdLinkedInProfile = ["job_application_answers_attributes_0_text_value"]
    possibleFieldIdWebsite = ["job_application_answers_attributes_1_text_value"]
    #need to input fields, dont actually need to scroll down but should work
    print("input fields")
    #TODO ACTUALLY INPUT FIELDS (or move on to next job posting if fields not found), NOW IT WORKS DONT NEED TO SCROLL DOWN TO INPUT FIELDS SCROLL DOWN WAS JUST WAY OF MAKING SURE THAT DRIVER IS ON THE CORRECT WINDOW
    if inputFieldFromOptions(driver, firstName, By.ID, possibleFieldIdFirstName):
        print("Inputted first name successfully...")
    if inputFieldFromOptions(driver, lastName, By.ID, possibleFieldIdLastName):
        print("Inputted last name successfully...")
    if inputFieldFromOptions(driver, emailAddress, By.ID, possibleFieldIdEmailAddress):
        print("Inputted email address successfully...")


    if inputFieldFromOptions(driver, phoneNumber, By.ID, possibleFieldIdPhoneNumber):
        print("Inputted phone number successfully...")
        
    if inputFieldFromOptions(driver, linkedInProfile, By.ID, possibleFieldIdLinkedInProfile):
        print("Inputted LinkedIn profile successfully...")
   
    if inputFieldFromOptions(driver, website, By.ID, possibleFieldIdWebsite):
        print("Inputted website successfully...")

    
    uploadResume(driver)
         
    sleep(10) 
    
    #scroll_element = driver.find_element(By.XPATH, "//html")
    #scrollDown(500, scroll_element)
    # IF REACH HERE THEN ALL OR MOST OF THE FIELDS HAVE BEEN FILLED BY THE SCRIPT AND SHOULD CLICK ON APPLY BUTTON TO SEND APPLICATION
    #TODO if application successfully submitted need to append driver.current_url to postingsAppliedTo.txt, make sure to truncate end of url after job id
