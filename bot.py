from webflowbot import WebFlowBot
from pprint import pprint
import json
from time import sleep
import sys
def main():
    task = "-t"
    config = None
    headless = False
    try:
        try:
            print("#Bot: Reading Configrations...")
            print("#Bot: Reading Login Details...")
            print("#Bot: (If you need to change login details use 'config.json').")
            with open("config.json", "r") as configrations:
                config = json.load(configrations)
                print("#Bot: Reading Successfull!")
        except EnvironmentError:
            print("#Bot Error: Error Opening File 'config.json'. Bot needs this file to run properly.")
            exit(-1)

        if(len(sys.argv)> 1):
            task = sys.argv[1]
        else:
            task = config["task"]
        if(len(sys.argv) > 2):
            headless = sys.argv[2]
        else:
            headless = False

        try: 
            print("#Bot: Opening Browser...")
            bot = WebFlowBot(headless)
            print("#Bot: Success!")
        except:
            print("#Bot Error: Chrome Webdriver failed to load or don't exsit.")
            print("#Bot Error: Download Chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads")
            exit(-1)

        try:
            print("#Bot: Trying to login...")
            if (not bot.init_webflow(config['username'],config['password'])):
                raise IOError
            print("#Bot: Login Successful, Redirecting to start the job!")
        except:
            print("#Bot Error: Login Failed. Please Check your credentials in 'config.json' file or there is poor connection...")
            exit(-1)


        if (task == "-f"):
            bot.follow(config["follow_url"])
        elif (task == "-h"):
            bot.hire(config["hire_url"], config["subject"], config["message"])
        else:
            print("#Bot Error: Exitting... Undefined task. Use '-f' to Follow and '-h' to Hire.")
    except:
        print("#Bot: Session closed by user or forced closed!")
    sleep(2)
    
if __name__ == "__main__":
    main()
else:
    print ("This script is required to run as main")
