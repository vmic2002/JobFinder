"""
python script to automate boring process of applying to a lot of job/internship postings
it could search linkedin for job postings and store the postings' urls in a list, then for each url open the webpage and fill in every field it knows, plus upload cv + cover letter
for fields that are different for each site, it could prompt the user to respond
"""

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from enum import Enum


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from bs4 import BeautifulSoup
from getpass import getpass

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
datePosted = DatePosted.PAST_MONTH
keywords ="software engineering intern"
location = "California, United States" 
desiredWorkPeriod1 = "summer-2024"#this will be in the url of the linkedin job posting
desiredWorkPeriod2 = "Summer 2024"#this will be in the name of the linkedin job posting
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

# Locate the email text field by its ID
email_field = driver.find_element(By.ID, "username")

# Input the email using send_keys()
email_field.send_keys(linkedInEmailAddress)

# Locate the password text field by its ID
password_field = driver.find_element(By.ID, "password")

# Input the password using send_keys()
password_field.send_keys(linkedInPassword)

# Find the button element by XPath
button = driver.find_element(By.XPATH, "//button[@class='btn__primary--large from__button--floating' and @data-litms-control-urn='login-submit']")

# Click the button (LOG IN)
button.click()
#sleep(5)

# here the browser will ask the user to prove he is not a robot
# must wait until the user has passed the not a robot test
# all we have to do is wait until the current url is linkedin.com/jobs, which will mean user has passed the test
while "/jobs/" not in driver.current_url:
    print("Waiting for user to pass not a robot test...")
    sleep(1)
print("Reached LinkedIn job postings site.")
print("Searching for job postings...")
#sleep(5)

# Now loop through list of job postings on this site
# Get the page source
page_source = driver.page_source

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# For example, find all 'a' elements with a specific class
target_links1 = soup.find_all('a', class_='base-card__full-link')

# maybe just find all a elements with href field? for now doing method 1 and 2

# Find all <a> tags with the specified class
target_links2 = soup.find_all('a', class_='disabled ember-view job-card-container__link job-card-list__title job-card-list__title--link')

# Extract href attributes from the found <a> tags
linkedInJobPostingsLinks2 = ["https://linkedin.com"+link.get('href') for link in target_links2 if desiredWorkPeriod2 in link.get('aria-label')] #if desiredWorkPeriod in link.get('href')]
print("Found "+str(len(linkedInJobPostingsLinks2))+" using targetlink2")
#for x in linkedInJobPostingsLinks2:
 #   print(x)

#SOMETIMES IT WOKRS FOR TARGETLINK2 SOMETIMES FOR THE 1

linkedInJobPostingsLinks1 = []
for link in target_links1:
    if desiredWorkPeriod1 in link.get('href'):
        linkedInJobPostingsLinks1.append(link.get('href'))

# TODO Now need to loop through linkedInJobPostingsLinks and one by one:
# - open new tab with this url
# - click on apply button or get url for job posting
# - fill fields (resume, age, ...)
# - click on apply
# - delete tab
# - continue loop
i = 0
print("Found "+str(len(linkedInJobPostingsLinks1))+" using targetlink1")
linkedInJobPostingsLinks = linkedInJobPostingsLinks1 if len(linkedInJobPostingsLinks1)>len(linkedInJobPostingsLinks2) else linkedInJobPostingsLinks2

for l in linkedInJobPostingsLinks:
    print(i)
    print("\tNavigating to LinkedIn job posting: "+l) 
    driver.get(l)
    #TODO NEED TO CLICK ON APPLY BUTTON, that will redirect to site where we can uplaod resume etc
    # Wait for the div element to be present
    div_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "jobs-apply-button--top-card"))
    )

    # Find the button element inside the div
    apply_button = div_element.find_element(By.TAG_NAME, "button")

    # Click the button
    apply_button.click()
    #works! button is found and clicked
    sleep(5)
    i+=1

print("DONE")
sleep(1000)#TODO remove sleep at the end so it is fast
driver.close()
