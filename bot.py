from info import *
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os.path
from os import path
import schedule
from datetime import datetime
import datetime
from selenium.webdriver.common.action_chains import ActionChains
import discord_webhook


#PATH = r"C:\Users\Administrator\Desktop\RUAS-Bot\chromedriver.exe"

#put your webDriver path here
PATH = ""
opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })

driver = None
#URL = "https://teams.microsoft.com"

#put your teams credentials here
CREDS = {'email' : '','passwd':''}

days = datetime.datetime.today().weekday()



def login():
	global driver
	#login required
	print("logging in")
	emailField = driver.find_element_by_xpath('//*[@id="i0116"]')
	emailField.click()
	emailField.send_keys(CREDS['email'])
	driver.find_element_by_xpath('//*[@id="idSIButton9"]').click() #Next button
	time.sleep(5)
	passwordField = driver.find_element_by_xpath('//*[@id="i0118"]')
	passwordField.click()
	passwordField.send_keys(CREDS['passwd'])
	driver.find_element_by_xpath('//*[@id="idSIButton9"]').click() #Sign in button
	time.sleep(5)
	# return driver



def joinclass(class_name,start_time,end_time,link):

	now = datetime.datetime.now()
	current_time = now.strftime("%H:%M")	

	WebDriverWait(driver,10000).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
	

	class_running_time = datetime.datetime.strptime(end_time,"%H:%M") - datetime.datetime.strptime(current_time,"%H:%M")


	try:
		print("Fetching join button")
		time.sleep(5)

		joinbtn = driver.find_element_by_class_name("ts-calling-join-button")
		joinbtn.click()

		print("Button clicked")

		time.sleep(4)
		webcam = driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button/span[1]')
		if(webcam.get_attribute('title')=='Turn camera off'):
			webcam.click()
		time.sleep(1)

		microphone = driver.find_element_by_xpath('//*[@id="preJoinAudioButton"]/div/button/span[1]')
		if(microphone.get_attribute('title')=='Mute microphone'):
			microphone.click()

		time.sleep(1)
		joinnowbtn = driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button')
		joinnowbtn.click()

		discord_webhook.send_msg(class_name=class_name,status="joined",current_time=current_time,start_time=start_time,end_time=end_time)
	
		#now schedule leaving class
		
		print("Waiting Time : {}".format(class_running_time))
		time.sleep(class_running_time.seconds)

		driver.find_element_by_class_name("ts-calling-screen").click()


		driver.find_element_by_xpath('//*[@id="teams-app-bar"]/ul/li[3]').click() #come back to homepage
		time.sleep(1)

		driver.find_element_by_xpath('//*[@id="hangup-button"]').click()
		print("Class left")
		discord_webhook.send_msg(class_name=class_name,status="left",current_time=current_time,start_time=start_time,end_time=end_time)

	except:

		now2 = datetime.datetime.now()
		current_time2 = now2.strftime("%H:%M")

		atmpt = ((class_running_time.seconds/60) - 7)

		if current_time2 < end_time:

			#join button not found
			#refresh every minute until found
			while True:
				print("Join button not found, trying again")
				print("Time left {} minutes...".format(int(atmpt)))
				time.sleep(60)
				driver.refresh()
				joinclass(class_name,start_time,end_time,link)

			print("Seems like there is no class today.")
			discord_webhook.send_msg(class_name=class_name,status="noclass",current_time=current_time2,start_time=start_time,end_time=end_time)


	print("Schedule Ended!")
	driver.quit()


def browser(class_name,start_time,end_time,link):

	#start the browser
	print("Opening Browser")
	global driver
	driver = webdriver.Chrome(executable_path=PATH,chrome_options=opt,service_log_path='NUL') 

	driver.get(link)

	WebDriverWait(driver,10000).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))

	driver.find_element_by_xpath('//*[@id="openTeamsClientInBrowser"]').click()#click on "Use the web app instead" button
	time.sleep(5)

	if("login.microsoftonline.com" in driver.current_url):
		login() #login if needed..

	print("URL found")
	print("Scheduling {}!".format(class_name))
	
	joinclass(class_name,start_time,end_time,link)


def monday():
    schedule.every().monday.at(CS1).do(browser,ci,CS1,CS2,monCI)
    schedule.every().monday.at(CS3).do(browser,cv,CS3,CE3,monCV)
    schedule.every().monday.at(CS4).do(browser,dm,CS4,CE5,monDM)
    schedule.every().monday.at(CS6).do(browser,cv,CS6,CE8,monCV2)
    while True:
    	schedule.run_pending()
    	# Checks whether a scheduled task
    	# is pending to run or not
    	time.sleep(1)#seconds (monday)
    
def tuesday():
    schedule.every().tuesday.at(CS2).do(browser,cv,CS2,CE2,tueCV)
    schedule.every().tuesday.at(CS3).do(browser,ci,CS3,CE5,tueCI)
    schedule.every().tuesday.at(CS6).do(browser,dm,CS6,CE6,tueDM)
    schedule.every().tuesday.at(CS7).do(browser,wa,CS7,CE7,tueWA)
    schedule.every().tuesday.at(CS8).do(browser,ci,CS8,CE8,tueCI2)
    while True:
    	schedule.run_pending()
    	# Checks whether a scheduled task
    	# is pending to run or not
    	time.sleep(1)#seconds (tuesday)

def wednesday():
    schedule.every().wednesday.at(CS1).do(browser,cv,CS1,CE1,wedCV)
    #schedule.every().wednesday.at(CS2).do(browser,wa,CS2,CE2,wedWA)
    schedule.every().wednesday.at(CS3).do(browser,dm,CS3,CE4,wedDM)
    schedule.every().wednesday.at(CS5).do(browser,ci,CS5,CE5,wedCI)
    schedule.every().wednesday.at(CS6).do(browser,wa,CS6,CE7,wedWA2)
    schedule.every().wednesday.at(CS8).do(browser,cv,CS8,CE8,wedCV2)
    while True:
    	schedule.run_pending()
    	# Checks whether a scheduled task
    	# is pending to run or not
    	time.sleep(1)#seconds (wednesday)

def thursday():
    schedule.every().thursday.at(CS5).do(browser,ci,CS5,CE5,thuCI)
    schedule.every().thursday.at(CS6).do(browser,wa,CS6,CE8,thuWA)
    while True:
    	schedule.run_pending()
    	# Checks whether a scheduled task
    	# is pending to run or not
    	time.sleep(1)#seconds (thursday)
    
def friday():
    schedule.every().friday.at(CS6).do(browser,wa,CS6,CE8,friWA)
    while True:
    	schedule.run_pending()
    	# Checks whether a scheduled task
    	# is pending to run or not
    	time.sleep(1)#seconds (friday)
    
def saturday():
	discord_webhook.send_msg(class_name="No class scheduled today",status="saturday",current_time="00:00",start_time="00:00",end_time="23:59")

def sunday():
	discord_webhook.send_msg(class_name="No class scheduled today",status="sunday",current_time="00:00",start_time="00:00",end_time="23:59")
	

if __name__=="__main__":
	#select day...
	if days==0:
		print("Scheduling Monday")
		monday()
		
	if days==1:
		print("Scheduling Tuesday")
		tuesday()
					
	if days==2:
		print("Scheduling Wednesday")
		wednesday()
		
	if days==3:
		print("Scheduling Thursday")
		thursday()
		
	if days==4:
		print("Scheduling Friday")
		friday()
		
	if days==5:
		print("Scheduling Saturday")
		saturday()
		
	if days==6:
		print("Scheduling Sunday")
		sunday()