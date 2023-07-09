from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pickle
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from difflib import SequenceMatcher

def wait(seconds=5):
    time.sleep(seconds)
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

all_liker = []

def main():
    options = Options()
    driver = webdriver.Chrome(options=options)
    global all_liker
    post_link = "https://www.linkedin.com/feed/update/urn:li:activity:7080539660438913024?utm_source=share&utm_medium=member_desktop"
    driver.get(post_link)
    wait()

    try:
        cookies = pickle.load(open("cookies_for_scripts.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
    except FileNotFoundError:
        print("cookies not found")



    wait()
    # driver.get(post_link)
    print("opening post")
    driver.get(post_link)
    wait()
    print("finding likes count button")
    likes_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "social-details-social-counts__reactions-count")))
    print("found likes count button")
    likes_button.click()
    print("clicked the like button")
    wait()

    all_liker = []

    while 1:
        people = driver.find_elements(By.XPATH, "//ul[contains(@class,'artdeco-list')]/li")
        if not people:
            print('list "people" is empty')
            break
        show_more_btn = driver.find_elements(By.XPATH, '//div[@id="artdeco-modal-outlet"]//button[contains(@class,"load-button")]')
        try:
            if show_more_btn:
                # show_more_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id="artdeco-modal-outlet"]//button[contains(@class,"load-button")]')))
                print(show_more_btn)
                show_more_btn[0].click()
        except Exception as e:
            # print(e)
            pass
        for person in people:
            name = person.find_element(By.XPATH, './/div[contains(@class,"artdeco-entity-lockup__title")]').text.split('\n')[0]
            # job = person.find_element(By.XPATH, './/div[contains(@class,"artdeco-entity-lockup__caption")]').text
            # print(name)
            all_liker.append(name)
            wait(1)
            driver.execute_script('var element = arguments[0]; element.remove();', person)

# main()
print(len(all_liker),"LOG 1")


path_xl_emp = "EMP.xlsx"
path_xl_out = "OUT.xlsx"

employee_list = []

df = pd.read_excel(path_xl_emp)
for index, row in df.iterrows():
    employee_list.append(row[1])

employees_who_liked = []

employees_who_liked = ['Dheeraj Bharambe', 'Kartik Puri', 'Rutuja Ghanwat', 'Shubham Khobragade', 'Pruthviraj Kakade', 'Srikanth Gubba', 'Akash Mhatre', 'Deepika Pariyani', 'Samrudhi Patil', 'Manav Bajaj', 'Chetan Patel', 'Rabi Jaiswal', 'Raj Dwivedi', 'Dipak Patil', 'Prathamesh Kathavate', 'Manupriya Rana', 'Neha Malik', 'Abhishek Khilari', 'Abhinav Watve', 'Shubhanshu Jain', 'Permendra Pandey']
all_liker = ['Abhishek Khilari', 'Prathamesh Kathavate', 'Rabi Jaiswal', 'Akshay Dadhich', 'Akash Mhatre', 'Nitesh Kumar', 'Deepika Pariyani', 'Samrudhi Patil', 'Hemant Singh', 'Shubham Khobragade', 'Rutuja Ghanwat', 'Shubhanshu Jain', 'Manupriya Rana', 'Dheeraj Bharambe', 'Mazhar Ansari', 'Chetan Patel', 'Srikanth G.', 'Manav Bajaj', 'Permendra Kumar Pandey', 'Raj Dwivedi', 'Abhinav Watve', 'Neelesh Kanyal', 'Guruprasad S G', 'Uma Mangal', 'Incentivate Solutions', 'Pruthviraj Kakade', 'Amit Jain', 'Deepak Patil', 'Kartik Puri', 'Neha Malik', 'Aryan .']

for i in employee_list:
    print(i)
    for j in all_liker:
        print(j,similar(i,j))
        if(similar(i,j) > 0.70):
            # employees_who_liked.append(i)
            print("-----")
            print("-----")
            print("-----")
            print("-----")
    print()
    print()
    print()



print(sorted(employees_who_liked))

# print()
# print(sorted(all_liker))
# print()
# print(sorted(employee_list))
# print()
# print(sorted(list(set(employee_list) - set(employees_who_liked))))

