# The purpose of this code is to automate taking in values from an excel file and mimic human user input to constantly input false information on
# a scammers website to keep them busy using .

from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd

# read the excel file fron the specific location using pandas
# read an exel file from a absolute location
base = pd.read_excel('C:/Test/testing/tests/Autobots/List.xlsx', converters={'Email':str,'Password':str})
print(base)

# Grabs information from specific
url = 'https://www.testwebsite.com/login.php'
web_form = get(url).content
soup = BeautifulSoup(web_form, 'html.parser')

# Paramaters needed for selenium to work. 
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)

# This will test if everything is reading/setting right.
def test(email, password):
    input_customer_email = driver.find_element(by=By.NAME, value='email_address')
    input_customer_password = driver.find_element(by=By.NAME, value='password')
    submit = driver.find_element(by=By.XPATH, value='//*[@id="bodyContent"]/div/div/div/div/div/div[1]/form/button')
    
    #input the values and hold a bit for the next action
    input_customer_email.send_keys(email)
    time.sleep(1)
    input_customer_password.send_keys(password)
    time.sleep(1)
    submit.click()
    time.sleep(7)

# creating a list to hold any entries should them result in error
failed_attempts = []

# creating a loop to do the procedure and append failed cases to the list
for user in base.index:
    # print(base)
    try:
        test(base['Email'][user], base['Password'][user])
    except:
        failed_attempts.append(base['Email'])
        pass

# Close the browser after you're done using it.
driver.quit()

if len(failed_attempts) > 0:
    # txt = 
    print("{} cases have failed".format(len(failed_attempts)))

print("Procedure concluded")