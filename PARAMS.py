from enum import Enum
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
#Params to input at job posting website
firstName = "Victor"
lastName = "Micha"
emailAddress = "victor.micha@mail.mcgill.ca" # job posting will send confirmation at this email
phoneNumber = "6504600726"
linkedInProfile = "https://www.linkedin.com/in/victor-micha/"
website = "https://github.com/vmic2002"
resumeFilePath = "/Users/victormicha/Victor_Micha_Resume.pdf"

#Params to find job postings on LinkedIn
datePosted = DatePosted.PAST_MONTH
keywords ="software engineering intern"
location = "California, United States"
#desiredWorkPeriod1 = "summer-2024"#this will be in the url of the linkedin job posting
desiredWorkPeriod = "Summer 2024"#this will be in the name of the linkedin job posting
linkedInEmailAddress = "michavictor@gmail.com" #TODO input("Input LinkedIn email address:")
##########################

#DONT MODIFY BELOW

keywords = keywords.replace(" ", "%2520")
location = location.replace(" ", "%2520")
location = location.replace(",", "%252C")
