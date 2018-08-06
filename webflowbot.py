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

        self.poll_frequency = 20
        self.task = "-t"
        self.delay = 2
        self.long_delay = 60
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
        self.browser.set_page_load_timeout(60)
    
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
                    try:
                        links[i].click()
                    except:
                        print("#Bot Error: Element referred is not existing on the page " + self.browser.current_url)
                        sleep(self.delay)
                        try:
                            WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-link')))
                            links = self.browser.find_elements_by_class_name('profile-link')
                            sleep(self.delay)
                            links[i].click()
                        except:
                            continue
                        finally:
                            sleep(self.delay)
                    WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                    print("#Bot: Follow " + self.browser.current_url)
                    try:
                        sleep(self.delay)
                        follow = WebDriverWait(self.browser, self.long_delay, poll_frequency=self.poll_frequency).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.follower')))
                    except:
                        print("#Bot Error: Problem While finding the element on the page")
                        sleep(self.delay)
                    else:
                        try:
                            WebDriverWait(self.browser,self.long_delay, poll_frequency = self.poll_frequency).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'a.follower')))
                        except:
                            print("#Bot Error: Failed to follow " + self.browser.current_url )
                        else:
                            if(follow.text == "Follow"):
                                follow.click()
                                print("#Bot: Followed " + self.browser.current_url)
                            elif(follow.text == "Following"):
                                print("#Bot: Already Following " + self.browser.current_url)
                    finally:
                        sleep(self.delay)
                        self.browser.back()
                        sleep(self.delay)
                    try:
                        WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-link')))
                    except:
                        print("#Bot Error: Updating stale links...")
                    else:
                        links = self.browser.find_elements_by_class_name('profile-link')
                    finally:
                        pass
            
            self.click_next_follow()
        print("#Bot: Task accomplihsed!")

    def click_next_follow(self):
        try:
            nextBtn = WebDriverWait(self.browser, self.long_delay, self.poll_frequency).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[ng-show='hasNextPage()']")))
        except:
            print("#Bot Error: Next Button is not found. Bot may shutdown now!")
            exit()
        else:
            nextBtn.click()
            print("#Bot: Page covered. Next page " + self.browser.current_url +". Moving to next page. Please wait...")
        finally:
            sleep(5)
            self.follow_url = self.browser.current_url    
    def click_next_hire(self):
        try:
            nextBtn = WebDriverWait(self.browser, self.long_delay, self.poll_frequency).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[ng-show='hasNextPage()']")))
        except:
            print("#Bot Error: Next Button is not found. Bot may shutdown now!")
            exit()
        else:
            nextBtn.click()
            print("#Bot: Page covered. Next page " + self.browser.current_url +". Moving to next page. Please wait...")
        finally:
            sleep(5)
            self.follow_url = self.browser.current_url
    
    def hire(self, url, subject, body):
        self.hire_url = url
        self.browser.get(self.hire_url)
        print("#Bot: Started mandate...")
        self.define_task("-h")
        while(True):
            try:
                WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-link')))
                links = self.browser.find_elements_by_class_name('profile-link')
            except:
                print("#Bot Error: Timeout while waiting for page load." + self.browser.current_url)
            else:
                for i in range(0,len(links)):
                    try:
                        links[i].click()
                    except:
                        print("#Bot Error: Element referred is not existing on the page " + self.browser.current_url)
                        sleep(self.delay)
                        try:
                            WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-link')))
                            links = self.browser.find_elements_by_class_name('profile-link')
                            sleep(self.delay)
                            links[i].click()
                        except:
                            continue
                        finally:
                            sleep(self.delay)
                    WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                    print("#Bot: Sending hire message to " + self.browser.current_url)
                    try:
                        sleep(self.delay)
                        hire = WebDriverWait(self.browser, self.long_delay, poll_frequency=self.poll_frequency).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[ng-click="hire()"]')))
                    except:
                        print("#Bot Error: Problem While finding the element on the page")
                        sleep(self.delay)
                    else:
                        try:
                            WebDriverWait(self.browser,self.long_delay, poll_frequency = self.poll_frequency).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'a[ng-click="hire()"]')))
                        except:
                            print("#Bot Error: Failed to send message " + self.browser.current_url )
                        else:
                            hire.click()
                            sleep(self.delay)
                            subjectInput = WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.NAME, "subject")))
                            messageInput = WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.NAME, "body")))
                            submitBtn = self.browser.find_element_by_css_selector("button.button.pull-right[ng-click='message(subject, body)']")
                            cancelBtn = self.browser.find_element_by_css_selector("button[ng-click='cancel()']")
                            subjectInput.send_keys(subject)
                            messageInput.send_keys(body)
                            submitBtn.click()
                            cancelBtn.click()
                            print("#Bot: Message sent...")

                    finally:
                        sleep(self.delay)
                        self.browser.back()
                        sleep(self.delay)
                    try:
                        WebDriverWait(self.browser, self.long_delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile-link')))
                    except:
                        print("#Bot Error: Updating stale links...")
                    else:
                        links = self.browser.find_elements_by_class_name('profile-link')
                    finally:
                        pass
            
            self.click_next_hire()
        print("#Bot: Task accomplihsed!")

    def save_follow_url(self):
        print("#Bot: Updating follow link in 'config.json'")
        temp = None
        try:
            print("#Bot: Reading previous data...")
            with open('config.json', 'r') as file:
                temp = json.load(file)
                print("#Bot: Reading Finished!")
            temp['follow_url'] = self.follow_url
            with open("config.json","w") as file:
                json.dump(temp, file)
                print("#Bot: Successful!")
        except EnvironmentError:
            print("#Bot: Error Opening 'config.json'")
            
    def save_hire_url(self):
        print("#Bot: Updating hire link in 'config.json'")
        temp = None
        try:
            print("#Bot: Reading previous data...")
            with open('config.json', 'r') as file:
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
            self.save_hire_url()
        else:
            pass
        print("#Bot: Bye!")
        self.browser.quit()