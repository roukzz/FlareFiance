from asyncio.windows_events import NULL
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
nests_xpath= '//*[@id="root"]/div[3]/div/div/div/div[2]/div/div[3]/div/div[5]/p'
nest=""

opt = Options()
opt.add_experimental_option("debuggerAddress","localhost:8989")
driver = webdriver.Chrome(PATH,chrome_options=opt)
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
    
    try:
        # nests_present=EC.presence_of_element_located((By.XPATH, nests_xpath))
        # WebDriverWait(driver, 5).until(nests_present)
        time.sleep(3)
        nests = driver.find_element_by_xpath(nests_xpath).text
        print("text nests :",nests)
        nests_integer= int(nests)
        print("integer nest: ",nests_integer)
       
    except Exception as exception:
        print(exception)
        print("could not find nests")

    
    
    
    if (nests) :    
        for x in range(5,(nests_integer+1)):
            i = str(x)
            
            liquidate_xpath = '//*[@id="root"]/div[3]/div/div/div/div[2]/div/div[1]/div/div/div[2]/div['+i+']/div[4]/button'
            # print(liquidate_xpath)
            try : 
                # wait to find the liquidate buttons
                element_present = EC.presence_of_element_located((By.XPATH, liquidate_xpath))
                WebDriverWait(driver, 40).until(element_present)
                driver.find_element_by_xpath(liquidate_xpath).click()
                print("button : ", x, " clicked ", " TIME: ",datetime.now())
                if (x%nests_integer) == 0:
                    try:
                        # metamask
                        driver.switch_to.window(cId[1])
                        print("metamask window: ", x)
                        try:
                            confirm_element_present = EC.presence_of_element_located((By.XPATH, confirm_xpath))
                            WebDriverWait(driver,0.2).until(confirm_element_present)
                        except Exception as exception:
                            # print(exception)
                            print("CONFIRM button not found at first sight, refresh MetaMask wallet")
                            driver.refresh()
                        
                        confirm_element_present = EC.presence_of_element_located((By.XPATH, confirm_xpath))
                        WebDriverWait(driver, 2).until(confirm_element_present)
                        
                        if (confirm_element_present) :
                            driver.find_element_by_xpath(confirm_xpath).click()
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
                print("counld not find liquidate elements")



