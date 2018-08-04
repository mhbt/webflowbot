#Bot To Automate Webflow
#Required plugins and softwares

- Python 3.5
- pip
- Selenium
- Chrome Browser
- Chrome Browser Driver - 

#Understading Files

- config.json : File that contains all the configration for user, like login information, message to be sent an default settings, links record to start bot from (auto save). Reset links to start from 1st page again
- data.json : This files stores all the persons profile links who have been sent message for hiring. Delete the data to re-start from page 1
- bot.py : The script you need to run (Bot controller)

#Setting up and installing bot

- Make sure you have installed python 3.5 on your system. If not installed install it from https://www.python.org/downloads/.
- Make sure you have installed pip (software installer for python scripts)
- If pip is not installed follow these steps:
Install Homebrew if not installed. 
In terminal copy this command :(ruby...) and paste and run it. Export path to path variable
--> ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
--> export PATH=/usr/local/bin:/usr/local/sbin:$PATH
--> brew install python
This will take a minute or two the run
--> pip install selenium
Now every thing is setup except you didn't place chrome driver into your path
So place the file included in the delivery to a path like
/opt/bin
and add that path to 
export PATH=$PATH:~/opt/

Now everything is setup

#Running the bot
Open terminal and go to the directory by using command 'cd'
for example if you have placed bot in ~/Desktop
cd Desktop/Webflow

#Running mandates
Mandate 1: (Hire)
--> python3 bot.py -h
Mandate 3: (Follow)
--> python3 bot.py -f

