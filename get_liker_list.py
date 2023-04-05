from selenium import webdriver
import pickle
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time, sys

from config import USERNAME, PASSWORD

browser = None
print('args = ', len(sys.argv))
print ('Argument List:', str(sys.argv))
if(len(sys.argv) != 2):
    print("Something's wrong with post link")
    exit(0)

post_link = 'https://www.linkedin.com/posts/incentius_what-are-the-features-of-ruby-on-rails-activity-7047168083425136640-ZrBD?utm_source=share&utm_medium=member_desktop'
post_link = sys.argv[1]

def main():
    setupBrowser()
    getLikesOfPosts()
    
    pickle.dump(browser.get_cookies(), open("cookies_for_scripts.pkl", "wb"))

def setupBrowser():
    global browser
    global is_first_time
    options = Options()
    options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(options=options)
    browser.get("https://www.linkedin.com/")
    try:
        cookies = pickle.load(open("cookies_for_scripts.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
    except FileNotFoundError:
        print("cookies not found")
        login(USERNAME, PASSWORD)

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
            show_more_results()
            wait(5)
    except NoSuchElementException:
        print("list loading finished, Hopefully .")
        collect_elements()
        pass
    except Exception as e:
        print('EXCEPTION aosjdfsjd')
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
