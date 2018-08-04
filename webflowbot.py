from selenium import webdriver
from time import sleep
from pprint import pprint
import json


class WebFlowBot:
    
    def __init__(self):
        self.task = "-t"
        self.sleep = 2
        self.long_wait = 2
        self.follow_url = None
        self.hire_url = None
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        #To run script headless -- no browser output seen
        self.browser = webdriver.Chrome(chrome_options=self.options)
        #To run script while monitoring the changes
        #self.browser = webdriver.Chrome()
        self.data = []
    
    def define_task(self,task):
        self.task = task
    
    def init_webflow(self, username, password):
        self.browser.get("https://webflow.com/dashboard/login?r=%2Fdashboard")
        userinput = self.browser.find_element_by_name("username")
        pswdinput = self.browser.find_element_by_name("password")
        userinput.send_keys(username)
        pswdinput.send_keys(password)
        pswdinput.submit()
        print("#Bot: Waiting...")
        sleep(self.long_wait)
        print("#Bot: " + self.browser.current_url)        
        if (self.browser.current_url == "https://webflow.com/dashboard"):
            return True
        return False       

    def follow(self, url):
        self.browser.get(url)
        print("#Bot: Started following...")
        sleep(self.sleep)
        while(True):
            links = self.browser.find_elements_by_class_name('profile-link')
            for i in range(0,len(links)):
                links[i].click()
                sleep(self.sleep)
                print("#Bot: Follow " + self.browser.current_url)
                follow = self.browser.find_element_by_css_selector("a.follower")
                followText = self.browser.find_element_by_css_selector("a.follower span span")
                if(followText.text == "Follow"):
                    follow.click()
                    print("#Bot: Followed " + self.browser.current_url)
                else:
                    print("#Bot: Already Following " + self.browser.current_url)
                sleep(self.sleep)
                self.browser.back()
                sleep(self.sleep)
                self.follow_url = self.browser.current_url
                try:
                    links = self.browser.find_elements_by_class_name('profile-link')
                except:
                    print("Waiting to load page... Connection is slow")
                    sleep(self.long_wait)
                    links = self.browser.find_elements_by_class_name('profile-link')

            try:
                nextBtn = self.browser.find_element_by_css_selector("a[ng-show='hasNextPage()']")
                nextBtn.click()
                sleep(self.sleep)
            except:
                break
        print("#Bot: Task accomplihsed!")

    def hire(self, url, subject, body):
        print("#Bot: Started Hiring now...")
        try:
            print("#Bot: Reading previous data for hirings...")
            with  open('data.json', 'r') as file:
                self.data = json.load(file)
                print("#Bot: Reading Finished!")
        except EnvironmentError:
            print("#Bot: No previous data for hired persons found. Hired data will be recorded to avoid resends.")
        self.browser.get(url)
        sleep(self.sleep)
        while (True):
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
                    sleep(self.sleep)
                    print("#Bot: Hiring " + self.browser.current_url)
                    hire = self.browser.find_element_by_css_selector("a[ng-click='hire()']")
                    hire.click()
                    sleep(self.sleep)
                    subjectInput = self.browser.find_element_by_name("subject")
                    messageInput = self.browser.find_element_by_name("body")
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
                    links = self.browser.find_elements_by_class_name('profile-link')
                except:
                    print("Waiting to load page... Connection is slow")
                    sleep(2)
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