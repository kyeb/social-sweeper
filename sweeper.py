import time
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()
url = "https://facebook.com"
browser.get(url)

username = browser.find_elements_by_css_selector("input[name=email]")
username[0].send_keys('social.sweeper.91@gmail.com')

# Find the password field and enter the password password.
password = browser.find_elements_by_css_selector("input[name=pass]")
password[0].send_keys('FLXJwaPN6CLopu')

# Find the login button and click it.
loginButton = browser.find_elements_by_css_selector("input[type=submit]")
loginButton[0].click()

# Click around randomly some?

df = pd.read_csv("data/voters_test100_names.csv")

for index, row in df.iterrows():
    name = row["name_first"] + " " + row["name_last"]
    # Find the search bar
    searchBar = browser.find_elements_by_css_selector("input[type=text]")
    searchBar[0].send_keys(name)
    searchBar[0].send_keys(Keys.ENTER)

    # Find link tags that correspond to person's name
    time.sleep(1)
    links = browser.find_elements_by_css_selector("a")
    for link in links:
        if fuzz.ratio(link.get_attribute("textContent"), name) >= 85:
            print(link.get_attribute("href"))
            break


time.sleep(10)

browser.close()

