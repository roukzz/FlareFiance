from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import datetime
from pynput.keyboard import Key, Controller

PATH ='C:\Program Files (x86)\chromedriver.exe'
EXTENTION_PATH='C:\metamask_ext\metamask.crx'
confirm_xpath = '//*[@id="app-content"]/div/div[3]/div/div[4]/div[3]/footer/button[2]'

opt = Options()
opt.add_experimental_option("debuggerAddress","localhost:8989")
driver = webdriver.Chrome(PATH,chrome_options=opt)
# driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#")
# print('metamask Launched')
# confirm button : //*[@id="app-content"]/div/div[2]/div/div[4]/div[3]/footer/button[2]
print('launch flare finance')
driver.get("https://xfl.flr.finance/wsgb/liquidations")
pId= driver.current_window_handle
print("parent ID: ",pId)
print("you have 15 sec to lauch metamask tab")
time.sleep(15)
print("15 sec after sleep")
cId= driver.window_handles
print("child ID: ", cId)

driver.switch_to.window(pId)
while True:
    driver.refresh()
    path='//*[@id="root"]/div[3]/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/div[1]/div[1]'

    for x in range(1,31):
        i = str(x)
        xpath = '//*[@id="root"]/div[3]/div/div/div/div[2]/div/div[1]/div/div/div[2]/div['+i+']/div[4]/button'
        print(xpath)
        try : 
            element_present = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(driver, 30).until(element_present)
            driver.find_element_by_xpath('//*[@id="root"]/div[3]/div/div/div[3]/div[2]/div[2]/div[2]/div['+ i+ ']/div[4]/button').click()
            print("button : ", x, " clicked ", " TIME: ",datetime.now())
            if (x%6) == 0:
                try:
                    # metamask
                    driver.switch_to.window(cId[1])
                    print("metamask window: ", x)
                    confirm_element_present = EC.presence_of_element_located((By.XPATH, confirm_xpath))
                    WebDriverWait(driver, 0.5).until(confirm_element_present)
                    if (confirm_element_present) :
                        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[4]/div[3]/footer/button[2]').click()
                        print("**********************************")
                        print("confirm button clicked")
                        print("TIME: ", datetime.now())
                        print("**********************************")
                        time.sleep(20)
                        print("waiting for 20 sec") 
                    driver.refresh()
                    driver.switch_to.window(pId)
                except Exception as exception:
                    driver.refresh()
                    driver.switch_to.window(pId)
                    print("confirm button not found")

        except Exception as exception:
            driver.refresh()
            print("counld not find element")



