import pandas as pd
from preprocessor import Preprocessor
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import random

df = pd.read_csv('./universities.csv')
preprocessor = Preprocessor(df)

print("Please complete this informations:")
user_input_fullname = input("What is your full name? ")
user_input_destination_university = input("What university are you applying for? ")
user_input_destination_major = input("What major are you applying for? ")
user_input_gpa = input("What is your GPA: ")
user_input_source_university = input("What is your current university name? ")
user_input_source_major = input("What is your current major? ")

extracted_keywords = preprocessor.get_extracted_keywords(user_input_destination_university).split(",")

user_keywords = [
  f'My Fullname: {user_input_fullname}',
  f'Destination University: {user_input_destination_university}',
  f'Destination Major: {user_input_destination_major}',
  f'My GPA: {user_input_gpa}',
  f'Current University: {user_input_source_university}',
  f'Current Major: {user_input_source_major}',
]

all_keywords = extracted_keywords + user_keywords

print(all_keywords)

chromedriver_path = ".//chromedriver.exe"
chrome_profile_path = "C:\\Users\\Amirreza Zarkesh\\AppData\\Local\\Google\\Chrome\\User Data"

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={chrome_profile_path}\\Selenium Test")
options.page_load_strategy = 'normal'
page = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=options)

def dummy_send_keys(element, word):    
  random_numbers_list = [0.1, 0.2]
  for c in word:
    element.send_keys(c)
    random_number = random.choice(random_numbers_list)
    sleep(random_number)

def find_element_by_xpath(xpath):
  return WebDriverWait(page, 50).until(EC.presence_of_element_located((By.XPATH, xpath)))

page.get('https://app.gomoonbeam.com/headstart/template?collection=student')

try:
  essayButton = find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/div/div/div[2]/div/button[1]')
  sleep(1)
  essayButton.click()

  essayTitle = find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div/div[1]/div[2]/div/h1')
  dummy_send_keys(essayTitle, "Motivation Letter")

  essayAuthor = find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div/div[1]/div[3]/div/p')
  dummy_send_keys(essayAuthor, user_input_fullname)

  keywordsInput = find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div/div[1]/div[4]/div')
  for keyword in all_keywords:
    dummy_send_keys(keywordsInput, keyword)
    dummy_send_keys(keywordsInput, Keys.ENTER)

  submitButton = find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div/div[2]/button')
  sleep(1)
  submitButton.click()

  generatedContent = find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div/div[1]/div')
  print("*******************************************\n")
  print(generatedContent.get_attribute('innerText'))

except TimeoutException:
  print("Loading took too much time!")

sleep(200)
