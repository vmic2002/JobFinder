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


from bs4 import BeautifulSoup


class DatePosted(Enum):
    # linked in has 4 options to look for job positions within a range of time
    # each of the 4 options is passed as a URL parameter f_TPR, which is what the .value of DatePosted will be
    # ANY_TIME should be a param but we dont use it because we only want recent job postings
    PAST_MONTH = "r2592000"
    PAST_WEEK = "r604800"
    PAST_24_HRS = "r86400" # because of f_TPR in url =r86400 is for past 24hours


# Params to modify
datePosted = DatePosted.PAST_WEEK
keywords = "software%20engineering%20intern"
location = "California%2C%20United%20States"
desiredWorkPeriod = "summer-2024"#this will be in the url of the linkedin job posting
#TODO COULD ALSO MODIGY PARAM "keywords" to other values than software engineering intern
#so that this script could automate the job application process for any field

#linked in url where list of job postings will be 
url = "https://www.linkedin.com/jobs/search/?f_TPR="+datePosted.value+"&keywords="+keywords+"&location="+location+"&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true"

#print(url)

# Configure Chrome options
chrome_options = Options()
chrome_options.headless = False  # Make the browser window visible

# Open a Chrome browser with configured options
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the webpage
    driver.get(url)
except WebDriverException as e:
    # Handle the exception
    print("An error occurred:", e)

# Now loop through list of job postings on this site

# Get the page source
page_source = driver.page_source

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# For example, find all 'a' elements with a specific class
target_links = soup.find_all('a', class_='base-card__full-link')

linkedInJobPostingsLinks = []
for link in target_links:
    if desiredWorkPeriod in link.get('href'):
        linkedInJobPostingsLinks.append(link.get('href'))

# TODO Now need to loop through linkedInJobPostingsLinks and one by one:
# - open new tab with this url
# - click on apply button or get url for job posting
# - fill fields (resume, age, ...)
# - click on apply
# - delete tab
# - continue loop
i = 0
print("Gathered a total of "+str(len(linkedInJobPostingsLinks))+" LinkedIn job postings...")
for l in linkedInJobPostingsLinks:
    print(i)
    print("\tNavigating to LinkedIn job posting: "+l)
    driver.get(l)
    #TODO BUG WHERE SOMETIMES GOES TO LINKEDIN JOB POSTING AND SOMETIMES ASKS USER TO LOG IN TO LINKEDIN
    sleep(2)
    i+=1

print("DONE")
sleep(1000)#TODO remove sleep at the end so it is fast

