"""
python script to automate boring process of applying to a lot of job/internship postings
it searches linkedin for job postings, then for each url opens the webpage and fills in every field it knows, plus upload cv + cover letter and apply automatically 
This file deals with signing in to linkedin, gathering the job postings, and looping through them
It is in the ApplyToJobPosting.py file that each job posting is either applied to and added to file postingsAppliedTo.txt or not applied to unless user manually does it
"""
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from enum import Enum

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from getpass import getpass
import os

from PARAMS import *
from ApplyToJobPosting import *

linkedInPassword = getpass("Input LinkedIn password: ")#input("Input LinkedIn password:")

#signIn url which redirected to linkedin job postings url
signIn = "https://www.linkedin.com/login?emailAddress=&fromSignIn=&fromSignIn=true&session_redirect=https%3A%2F%2Fwww.linkedin.com%2Fjobs%2Fsearch%2F%3Ff_TPR%3D"+datePosted.value+"%26keywords%3D"+keywords+"%26location%3D"+location+"%26origin%3DJOB_SEARCH_PAGE_JOB_FILTER%26refresh%3Dtrue&trk=public_jobs_nav-header-signin"

#print(signIn)
#print(url)
# Configure Chrome options
chrome_options = webdriver.ChromeOptions()

# Enable incognito mode so no caching etc
chrome_options.add_argument("--incognito")

# Initialize Chrome driver with ChromeOptions
driver = webdriver.Chrome(options=chrome_options)
#driver = webdriver.Chrome()


####################FOR TESTING inputed fields not on screen and scrollDown  WORKS
driver.get("https://boards.greenhouse.io/verkada/jobs/4135597007?gh_src=cda0ce657us&source=LinkedIn")#"https://boards.greenhouse.io/verkada/jobs/4135597007?gh_src=cda0ce657us&source=LinkedIn")
sleep(2)
#inputField(driver, "job_application_answers_attributes_0_text_value", "linkedinvicrtor", By.ID)#WORKS
#scroll_element = driver.find_element(By.XPATH, "//html")

#while not inputField(driver, "first_name", "VICTO12", By.ID):
#scrollDown(500, scroll_element)#WORKS
#    sleep(1)
#    print(".")
#print("INputed first name successfully")
tryApplyingAutomatically(driver)
print("DONE")
sleep(20)
exit(1)
#########################3



#driver = webdriver.Safari()
try:
    # Open the webpage
    driver.get(signIn)
    #print(jobPostingsURL)
    #driver.get(jobPostingsURL)
except WebDriverException as e:
    # Handle the exception
    print("An error occurred:", e)
    exit(1)


#sign in to LinkedIn

inputField(driver, "username", linkedInEmailAddress, By.ID)
# Locate the email text field by its ID
#email_field = driver.find_element(By.ID, "username")

# Input the email using send_keys()
#email_field.send_keys(linkedInEmailAddress)
inputField(driver, "password", linkedInPassword, By.ID)
# Locate the password text field by its ID
#password_field = driver.find_element(By.ID, "password")

# Input the password using send_keys()
#password_field.send_keys(linkedInPassword)

# Find the button element by XPath
button = driver.find_element(By.XPATH, "//button[@class='btn__primary--large from__button--floating' and @data-litms-control-urn='login-submit']")
# Click the button (LOG IN)
button.click()

# here the browser will ask the user to prove he is not a robot
# must wait until the user has passed the not a robot test
# all we have to do is wait until the current url is linkedin.com/jobs, which will mean user has passed the test
passedTest = False
c = 0
dots = ["", ".", "..", "..."]
while not passedTest: 
    try:
        print("Waiting for user to pass \"not a robot\" test", end='')
        while "/jobs/" not in driver.current_url:
            #print(".", end="", flush=True)
            #print("Waiting for user to pass \"not a robot\" test"+"."*(c+1), end='', flush=True) 
            #waiting_message = "Waiting" + dots[c % len(dots)]
            print(".", end='', flush=True)
            #print("\033[K", end='\r')
            #print("\r", end='', flush=True)
            sleep(1)
            c+=1
            if c==3:
                c = 0
                print('\b \b'*3, end='', flush=True)
        passedTest = True
    except Exception as e:
        print(e)
print("\nReached LinkedIn job postings site.")
print("Searching for job postings...")

# Now loop through list of job postings on this site

linkedInJobPostingsLinks = set()

# Define the class name of the 'a' elements you want to find
class_name = 'disabled ember-view job-card-container__link job-card-list__title job-card-list__title--link'
# Find the div element we want to scroll down
div_element = driver.find_element(By.XPATH, """//div[@class='jobs-search-results-list
          
          ']""")

scroll_amount = 0.8*driver.execute_script("return arguments[0].scrollHeight;", div_element)        

# Get the initial scroll height
last_height = driver.execute_script("return arguments[0].scrollHeight;", div_element)
# Start the loop to find 'a' elements and scroll down
while True:
    # Get the page source
    page_source = driver.page_source

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    target_elements = soup.find_all('a', class_=class_name)
    
    #to make ensure no duplicate job postings are added (same job id but different end of urls) -> trim off end of urls
    currLinkedInJobPostingsLinks = ["https://linkedin.com"+element.get('href')[:element.get('href').find("/", 11)] 
        for element in target_elements
            if desiredWorkPeriod in element.get('aria-label')]   
    
    # Append the found links to the list
    linkedInJobPostingsLinks.update(currLinkedInJobPostingsLinks)      
    # Scroll down to load more content
    # Scroll the specific element (div_element) by a specific amount
    # need to scroll down and fetch elements again because they are dynamically loaded when user scrolls (or bot :)) 
    scrollDown(driver, scroll_amount, div_element)
    
    # Wait for some time for new content to load
    sleep(1)  # Adjust the sleep time as needed COULD make it DEPEND ON NETWORK SPEED
    
    # Get the new scroll height
    new_height = driver.execute_script("return arguments[0].scrollHeight;", div_element)
    
    # Check if scroll height has not changed (indicating scrolled to the bottom)
    if new_height == last_height:
        #print("Scrolled to bottom of job postings div.")
        break
    
    # Update last height
    last_height = new_height

print("Found total of "+str(len(linkedInJobPostingsLinks))+" job postings")

# TODO Now need to loop through linkedInJobPostingsLinks and one by one:
# - open new tab with this url DONE
# - click on apply button DONE
# - fill fields (resume, age, ...) IN PROGRESS
# - click on apply
# - delete tab
# - continue loop

i = 0 #must start at 0
print("-"*37)
for l in linkedInJobPostingsLinks:
    print("Navigating to LinkedIn job posting "+str(i)+":")
    print("\t"+l)
    driver.switch_to.window(driver.window_handles[0])
    driver.get(l)
    try:
        # CLICK ON APPLY BUTTON, that will redirect to site where we can uplaod resume etc
        # Wait for the div element to be present
        div_element = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jobs-apply-button--top-card"))
        )
        # Find the button element inside the div
        apply_button = div_element.find_element(By.TAG_NAME, "button")
        # Click the button
        #print(driver.current_url)
        apply_button.click() 
        sleep(1)

        # Switch to the new tab THIS IS WHAT WAS CAUSING ALL BUGS RELATING TO SCROLLING AND INPUT FIELDS NOT WORKING
        driver.switch_to.window(driver.window_handles[i+1])#i+1 because order of window_handles is chronological (earliest opened tab first), so going to i+1 window means going to last job posting website tab
        #important to driver.switch_to.window after clicking button because even though new tab is opened after clicking button, the driver is focused on the previous tab (with the button). so must switch_to.window so driver focuses on tab that was just recently opened
        sleep(1)
        #print(driver.current_url)
        
        #########################################
        tryApplyingAutomatically(driver)
        #####################################
    except TimeoutException as e1:
        print("Did not find \"Apply\" button for job posting: "+l)
        print("Could NOT apply to job posting")
    except NoSuchElementException as e2:
        print(e2)
        print("Could NOT apply to job posting")
    i+=1
    print("-"*37)

print("Done")
os.system("say Done")
sleep(1000)#TODO remove sleep at the end so it is fast
driver.close()

