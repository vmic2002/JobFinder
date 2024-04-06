"""
python script to automate boring process of applying to a lot of job/internship postings
it could search linkedin for job postings and store the postings' urls in a list, then for each url open the webpage and fill in every field it knows, plus upload cv + cover letter
for fields that are different for each site, it could prompt the user to respond
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

def scrollDown(scroll_amount, div_element):
    driver.execute_script("arguments[0].scrollTop += "+str(scroll_amount)+";", div_element)

def inputField(driver, elementId, sol, by):
    timeout = 2 # in seconds 
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


class DatePosted(Enum):
    # linked in has 4 options to look for job positions within a range of time
    # each of the 4 options is passed as a URL parameter f_TPR, which is what the .value of DatePosted will be
    # ANY_TIME should be a param but we dont use it because we only want recent job postings
    PAST_MONTH = "r2592000"
    PAST_WEEK = "r604800"
    PAST_24_HRS = "r86400" # because of f_TPR in url =r86400 is for past 24hours


###### Params to modify ###########
#TODO COULD ALSO MODIGY PARAM "keywords" to other values than software engineering intern
#so that this script could automate the job application process for any field
firstName = "Victor"
lastName = "Micha"
datePosted = DatePosted.PAST_WEEK
keywords ="software engineering intern"
location = "California, United States" 
#desiredWorkPeriod1 = "summer-2024"#this will be in the url of the linkedin job posting
desiredWorkPeriod = "Summer 2024"#this will be in the name of the linkedin job posting
linkedInEmailAddress = "michavictor@gmail.com" #TODO input("Input LinkedIn email address:")
linkedInPassword = getpass("Input LinkedIn password: ")#input("Input LinkedIn password:")

##########################


#linked in url where list of job postings will be 
#jobPostingsURL = "https://www.linkedin.com/jobs/search/?f_TPR="+datePosted.value+"&keywords="+keywords.replace(" ", "%20")+"&location="+location.replace(" ", "%20")+"&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true"



keywords = keywords.replace(" ", "%2520")
location = location.replace(" ", "%2520")
location = location.replace(",", "%252C")

#signIn url which redirected to linkedin job postings url
signIn = "https://www.linkedin.com/login?emailAddress=&fromSignIn=&fromSignIn=true&session_redirect=https%3A%2F%2Fwww.linkedin.com%2Fjobs%2Fsearch%2F%3Ff_TPR%3D"+datePosted.value+"%26keywords%3D"+keywords+"%26location%3D"+location+"%26origin%3DJOB_SEARCH_PAGE_JOB_FILTER%26refresh%3Dtrue&trk=public_jobs_nav-header-signin"

#print(signIn)
#print(url)
# Configure Chrome options

driver = webdriver.Chrome()
#driver = webdriver.Safari()
try:
    # Open the webpage
    driver.get(signIn)
    #print(jobPostingsURL)
    #driver.get(jobPostingsURL)
except WebDriverException as e:
    # Handle the exception
    print("An error occurred:", e)


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
#sleep(5)

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
#sleep(100)
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
    scrollDown(scroll_amount, div_element)
    
    # Wait for some time for new content to load
    sleep(2)  # Adjust the sleep time as needed COULD make it DEPEND ON NETWORK SPEED
    
    # Get the new scroll height
    new_height = driver.execute_script("return arguments[0].scrollHeight;", div_element)
    
    # Check if scroll height has not changed (indicating scrolled to the bottom)
    if new_height == last_height:
        #print("Scrolled to bottom of job postings div.")
        break
    
    # Update last height
    last_height = new_height


#for x in linkedInJobPostingsLinks:
#    print("\t"+x)
print("Found total of "+str(len(linkedInJobPostingsLinks))+" job postings")

# TODO Now need to loop through linkedInJobPostingsLinks and one by one:
# - open new tab with this url
# - click on apply button
# - fill fields (resume, age, ...)
# - click on apply
# - delete tab
# - continue loop

i = 0
print("-"*37)
for l in linkedInJobPostingsLinks:
    print("Navigating to LinkedIn job posting "+str(i)+":")
    print("\t"+l)
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
        apply_button.click()
        #works! button is found and clicked
        # TODO ON JOB POSTING PAGE, SO CAN MAYBE UPLOAD RESUME ETC
        #sleep(2)
        # things above this work, but TODO input first name and last name, upload resume etc not yet working
        # THE BUG IS PROBABLY BECAUSE YOU HAVE TO SCROLL DOWN IN ORDER TO HAVE ACCESS TO THE FIRST NAME, LAST NAME, ETC 
        # PROBABLY YOU CANNOT INPUT A FIELD VALUE IF YOU CANT SEE IT ON THE SCREEN BECAUSE IT IS DYNAMICALLY LOADED
        # WILL NEED TO CALL SCROLLDOWN FUNC
        possibleFieldIdFirstName = ["first_name","job_application[first_name]","field-first_name"]
        possibleFieldIdLastName = ["last_name"]
        for elementId in possibleFieldIdFirstName:
            if inputField(driver, elementId, firstName, By.ID): #or inputField(driver, elementId, firstName, By.NAME):
                print("\tFirst name done...")
                break
        
        for elementId in possibleFieldIdLastName:
            if inputField(driver, elementId, lastName, By.ID): # or inputField(driver, "field-last_name", lastName, By.ID):
                print("\tLast name done...")
                break
               
        # TODO when done applying for a job posting, delete the tab so that the only tabs remaining at the end are the tabs that have not automatically been applied to by the script, could prompt user at end to manually apply to the remaining job postings
     
        sleep(2)
    except TimeoutException as e:
        print("Did not find \"Apply\" button for job posting: "+l)
    i+=1
    print("-"*37)

print("Done")
sleep(1000)#TODO remove sleep at the end so it is fast
driver.close()
