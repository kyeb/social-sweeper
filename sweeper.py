import time
import selenium
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def main():
    url = "https://facebook.com"
    email = "social.sweeper.91@gmail.com"
    pw = "FLXJwaPN6CLopu"
    voterfile = "data/voters_test100_names.csv"
    output = "data/results.csv"

    browser = webdriver.Firefox()
    browser.get(url)

    login(browser, email, pw)

    df = pd.read_csv(voterfile)

    for index, row in df.iterrows():
        time.sleep(1)
        name = row["name_first"] + " " + row["name_last"]

        search_for(browser, name)

        try:
            profile_url = find_profile_url(browser, name)
            print(profile_url)
            df.at[index, "facebook_url"] = profile_url
        except Exception as e:
            print(e)
            break

    df.to_csv(output)

    browser.close()

def login(browser, email, pw):
    # TODO: use xpath for more fine-grained finding
    username_box = browser.find_elements_by_css_selector("input[name=email]")[0]
    username_box.send_keys(email)

    # Find the password field and enter the password password.
    # TODO: use xpath for more fine-grained finding
    password_box = browser.find_elements_by_css_selector("input[name=pass]")[0]
    password_box.send_keys(pw)

    # Find the login button and click it.
    # TODO: use xpath for more fine-grained finding
    login_button = browser.find_elements_by_css_selector("input[type=submit]")[0]
    login_button.click()

    # TODO: click around randomly some?

def search_for(browser, name):
    # Since Facebook's code is very JS heavy, we need to re-find the search
    #   bar constantly, even between clicking and typing, or we get stale
    #   element exceptions from selenium.
    def search_bar():
        return browser.find_element_by_xpath("//input[@type='text' and @placeholder='Search']")

    time.sleep(1)
    search_bar().click()
    search_bar().send_keys(name)
    search_bar().send_keys(Keys.ENTER)
    return

def find_profile_url(browser, name):
    # Find link tags that correspond to person's name
    # TODO: maybe use xpath and narrow down more initially
    time.sleep(1)
    links = browser.find_elements_by_css_selector("a")
    for link in links:
        try:
            if fuzz.ratio(link.get_attribute("textContent"), name) >= 85:
                return link.get_attribute("href")
        except selenium.common.exceptions.StaleElementReferenceException:
            continue

if __name__ == "__main__":
    main()

