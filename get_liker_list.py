from selenium import webdriver
import pickle
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
import time, sys
import pandas as pd


path_xl_emp = "EMP.xlsx"
path_xl_out = "OUT.xlsx"

employee_list = []

# df = pd.read_excel(path_xl_emp)
# for index, row in df.iterrows():
#     employee_list.append(row[1])
# liker_list = []
# print(employee_list)
from config import USERNAME, PASSWORD

browser = None
# if(len(sys.argv) != 2):
#     print("Something's wrong with post link")
#     exit(0)

post_link = 'https://www.linkedin.com/feed/update/urn:li:activity:7080539660438913024?utm_source=share&utm_medium=member_desktop'
# post_link = sys.argv[1]

def main():
    print("Opening and setting up browser ...")
    setupBrowser()
    print("Browser opened")
    getLikesOfPosts()
    toExcel()
    pickle.dump(browser.get_cookies(), open("cookies_for_scripts.pkl", "wb"))
    
    # browser.quit()

def toExcel():
    print("I got the data. Now I will write it to excel.")
    print(liker_list)
    print(employee_list)

def setupBrowser():
    global browser
    global is_first_time
    options = Options()
    # options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(options=options)
    browser.get(post_link)
    try:
        cookies = pickle.load(open("cookies_for_scripts.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
    except FileNotFoundError:
        print("cookies not found")
        # login(USERNAME, PASSWORD)

def login(username, password):
    global browser
    browser.get('https://www.linkedin.com/login')
    input_username = browser.find_element(by=By.NAME, value='session_key')
    input_username.send_keys(username)
    input_password = browser.find_element(by=By.NAME, value='session_password')
    input_password.send_keys(password)
    button_login = browser.find_element(by=By.CLASS_NAME, value='btn__primary--large')
    button_login.click()

def wait(seconds):
    time.sleep(seconds)

def getLikesOfPosts():
    global browser
    print("opening post")
    browser.get(post_link)
    wait(5)
    print("finding likes count button")
    likes_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "social-details-social-counts__reactions-count")))
    print("found likes count button")
    likes_button.click()
    print("clicked the like button")
    wait(5)
    try:
        while True:
            # wait(5)
            show_more_results()
            wait(5)
    except NoSuchElementException:
        print("list loading finished, Hopefully .")
        collect_elements()
        pass
    except Exception as e:
        print('EXCEPTION aosjdfsjd')
        try:
            print("finding likes count button")
            wait(5)
            likes_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "social-details-social-counts__reactions-count")))
            print("found likes count button")
            likes_button.click()
            print("clicked the like button")
        except ElementClickInterceptedException as e:
            print("finding likes count div")
            wait(5)
            likes_button = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "ember149")))
            print("found likes count div")
            likes_button.click()
            print("clicked the like div")
            print(e)
    

def collect_elements():
    print("collecting likers")
    li_class= "social-details-reactors-tab-body-list-item"
    right_div_class="artdeco-entity-lockup__content"
    title_div_class= "artdeco-entity-lockup__title"
    content =  browser.find_elements(by=By.XPATH, value="//li[contains(@class, \""+li_class+"\")]//div[contains(@class, \""+right_div_class+"\")]//div[contains(@class, \""+title_div_class+"\")]//span")
    count = 0
    likers_names = []
    for i in content:
        if('View' not in i.text and 'profile' not in i.text and i.text not in likers_names):
            likers_names.append(i.text)
            count+=1
    print(likers_names)
    global liker_list
    liker_list = likers_names
    print("collect complete , total count is ",count)
    

def show_more_results():
    print('showing more results')
    global browser
    button_id = 'ember216'
    button_xpath = "artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button"
    print('will try to find button')
    button =  browser.find_element(by=By.CLASS_NAME, value='scaffold-finite-scroll__load-button')
    print('Found button')
    button.click()
    print('showed.')
    

main()
