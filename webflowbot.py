from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
from pprint import pprint
import json


class WebFlowBot:
    
    def __init__(self, headless=False):

        self.poll_frequency = 10
        self.task = "-t"
        self.delay = 2
        self.long_delay = 10
        self.follow_url = None
        self.hire_url = None
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.data = []
        if (headless):
            #To run script headless -- no browser output seen
            self.browser = webdriver.Chrome(executable_path="./chromedriver",chrome_options=self.options)
        else:
            #To run script while monitoring the changes
            self.browser = webdriver.Chrome(executable_path="./chromedriver")
        self.browser.set_page_load_timeout(30)
    
    def define_task(self,task):
        self.task = task
    
    def init_webflow(self, username, password):
        self.browser.get("https://webflow.com/dashboard/login?r=%2Fdashboard")
        userinput = WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.NAME, 'username')))
        pswdinput = WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.NAME, 'password')))
        userinput.send_keys(username)
        pswdinput.send_keys(password)
        pswdinput.submit()
        sleep(self.delay)
        print("#Bot: Waiting...")
        WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        print("#Bot: " + self.browser.current_url)        
        if (self.browser.current_url == "https://webflow.com/dashboard"):
            return True
        return False       

    def follow(self, url):
        self.follow_url = url
        self.browser.get(self.follow_url)
        print("#Bot: Started following...")
        self.define_task("-f")
        while(True):
            try:
                WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-link')))
                links = self.browser.find_elements_by_class_name('profile-link')
            except:
                print("#Bot Error: Timeout while waiting for page load." + self.browser.current_url)
            else:
                for i in range(0,len(links)):
                    links[i].click()
                    WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                    print("#Bot: Follow " + self.browser.current_url)
                    try:
                        follow = WebDriverWait(self.browser, self.long_delay, poll_frequency=self.poll_frequency).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.follower')))
                        sleep(self.delay)
                    except:
                        print("#Bot Error: Problem While finding the element on the page")
                    else:
                        if(follow.text == "Follow"):
                            follow.click()
                            print("#Bot: Followed " + self.browser.current_url)
                        else:
                            print("#Bot: Already Following " + self.browser.current_url)
                    sleep(self.delay)
                    self.browser.back()
                    sleep(self.delay)
                    try:
                        WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-link')))
                        links = self.browser.find_elements_by_class_name('profile-link')
                    except:
                        print("#Bot Error: Updating stale links...")
            nextBtn = WebDriverWait(self.browser, self.long_delay, self.poll_frequency).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[ng-show='hasNextPage()']")))
            nextBtn.click()
            # try:
            #     #nextBtn = self.browser.find_element_by_css_selector("a[ng-show='hasNextPage()']")
            #     nextBtn = WebDriverWait(browser, self.long_delay, self.poll_frequency).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[ng-show='hasNextPage()']")))
            # except:
            #     print("#Bot Error: Next Button is not found. Bot may shutdown now!")
            # else:
            #     sleep(self.delay)
            #     nextBtn.click()
        print("#Bot: Task accomplihsed!")

    def hire(self, url, subject, body):
        self.hire_url = url
        print("#Bot: Started Hiring now...")
        try:
            print("#Bot: Reading previous data for hirings...")
            with  open('data.json', 'r') as file:
                self.data = json.load(file)
                print("#Bot: Reading Finished!")
        except EnvironmentError:
            pass
        self.browser.get(url)
        self.define_task("-h")
        while (True):
            try:
                WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-link')))
                links = self.browser.find_elements_by_class_name('profile-link')
            except:
                print("Connection Slow. Waiting for 10 seconds....")
                WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-link')))
                links = self.browser.find_elements_by_class_name('profile-link')
            
            for i in range(0,len(links)):
                links[i].click()
                visted = False
                for link in self.data:
                    if(link == self.browser.current_url):
                        visted = True
                        print("#Bot: Already sent a hiring message to " + self.browser.current_url)
                if (not visted):
                    self.data.append(self.browser.current_url)
                    print("#Bot: Hiring " + self.browser.current_url)
                    try:
                        hire = WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.CLSS_SELECTOR, "a[ng-click='hire()']")))
                    except:
                        hire = WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.CLSS_SELECTOR, "a[ng-click='hire()']")))
                    hire.click()
                    subjectInput = WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.NAME, "subject")))
                    messageInput = WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.NAME, "body")))
                    submitBtn = self.browser.find_element_by_css_selector("button.button.pull-right[ng-click='message(subject, body)']")
                    subjectInput.send_keys(subject)
                    messageInput.send_keys(body)
                    submitBtn.click()
                    cancelBtn = self.browser.find_element_by_css_selector("button[ng-click='cancel()']")
                    cancelBtn.click()
                    sleep(self.sleep)
                    print("#Bot: Hiring message sent to " + self.browser.current_url)
                    
                self.browser.back()
                sleep(self.sleep)
                self.hire_url = self.browser.current_url
                try:
                    WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-link')))
                    links = self.browser.find_elements_by_class_name('profile-link')
                except:
                    print("Waiting to load page... Connection is slow")
                    WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-link')))
                    links = self.browser.find_elements_by_class_name('profile-link')
            try:
                nextBtn = self.browser.find_element_by_css_selector("a[ng-show='hasNextPage()']")
                nextBtn.click()
                sleep(self.sleep)
            except:
                break
        print("#Bot: Task Accomplished!")

    def save_follow_url(self):
        print("#Bot: Updating Follow link in 'conf.json'")
        temp = None
        try:
            print("#Bot: Reading previous data...")
            with  open('config.json', 'r') as file:
                temp = json.load(file)
                print("#Bot: Reading Finished!")
            temp['follow_url'] = self.follow_url
            with open("config.json","w") as file:
                json.dump(temp, file)
                print("#Bot: Successful!")
        except EnvironmentError:
            print("#Bot: Error Opening 'config.json'")

    def save_hire_data(self):
        print("#Bot: Saving State. Refresh state by deleting 'data.json' and 'config.json'") 
        with open("data.json","w") as file:
            json.dump(self.data, file)
        temp = None
        try:
            print("#Bot: Reading previous data...")
            with  open('config.json', 'r') as file:
                temp = json.load(file)
                print("#Bot: Reading Finished!")
            temp['hire_url'] = self.hire_url
            with open("config.json","w") as file:
                json.dump(temp, file)
                print("#Bot: Successful!")
        except EnvironmentError:
            print("#Bot: Error Opening 'config.json'")
    def __del__(self):
        if(self.task == "-f"):
            self.save_follow_url()
        elif(self.task == "-h"):
            self.save_hire_data()
        else:
            pass
        print("#Bot: Bye!")
        self.browser.quit()