#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from random import randint
import time, os, pytz
import random
import dotenv
from dotenv import load_dotenv
from datetime import datetime
from send_emails import *

#load variables set in your .env file
NIKE_URL= 'https://www.nike.com/launch/t/jordan-ma2-future-beginnings'
NIKE_TEST_URL='https://www.nike.com/launch/t/air-force-1-07-craft-mantra-orange'


WAIT_TIME =5

class nike_bot:
    def __init__(self,new_username,new_password):
        #Initilizes bot with class-wide variables
        profile = webdriver.FirefoxProfile() 
        opts=Options()
        opts.add_argument("--headless")
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", "198.50.163.192")
        profile.set_preference("network.proxy.http_port", 3129)
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.update_preferences() 
        self.driver = webdriver.Firefox(firefox_profile=profile,executable_path=os.getcwd()+"/geckodriver")
        self.username=new_username
        self.password=new_password
    #Sign into site with product
    def signIn(self):
        """ Sign into site with product"""
        driver = self.driver       #Navigate to URL
        #enter username
        time.sleep(random.randint(int(WAIT_TIME/2),WAIT_TIME))
        username_elem = driver.find_element_by_xpath('//*[@name="emailAddress"]')
        username_elem.clear()
        username_elem.send_keys(self.username)
        
        time.sleep(random.randint(int(WAIT_TIME/2),WAIT_TIME))
        
        #enter password 

        password_elem = driver.find_element_by_xpath('//*[@name="password"]')
        password_elem.clear()
        password_elem.send_keys(self.password)
        time.sleep(random.randint(int(WAIT_TIME/2),WAIT_TIME))
        password_elem.send_keys(Keys.RETURN)
    
    def findProduct(self):
        try:
            driver = self.driver
            driver.get(NIKE_TEST_URL)
            driver.set_window_position(0, 0)
            driver.set_window_size(1024, 1920)
            
            time.sleep(random.randint(int(WAIT_TIME/2),WAIT_TIME))

           
            
            #check availability
            dateTimeObj = datetime.now(pytz.timezone('US/Pacific'))
            if self.isProductAvailable() == 0:
                print("Item currently unavailable...", dateTimeObj)
                self.closeBrowser()
                return False
            else:
                print("Item is available....")
        

                #collect available shoe sizes 
                available_list = []
                sizes = driver.find_elements_by_xpath('//*[@data-qa="size-available"]')
                #print (len(sizes))
                for items in sizes:
                    available_list.append(items.text)


                #click random 
                print (available_list)
                size=available_list[random.randint(0,len(available_list)-1)]

                desired_size= "M 10.5 / W 12"
                desired_size2="M 11 / W 12.5"
                if desired_size in available_list: 
                    size = desired_size 
                elif desired_size2 in available_list:
                    size=desired_size2
                else:
                    print(desired_size," not available, choosing random")

                #click size 

                size_click = driver.find_element_by_xpath("//*[contains(text(),'%s')]" % size).click()
                time.sleep(1)
                #click add to cart
                print("Adding to cart...")
                WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(), 'Add to Cart') or contains(text(),'Buy')]"))).click()
                time.sleep(random.randint(int(WAIT_TIME/2),WAIT_TIME))
                print ("Clicked add to cart")

                #In case of sign-in pop-up
                try:
                    self.signIn()
                    print("....Signed In Succesfully")
                except:
                    pass
                #proceed to checkout 
                print ("Checking out...")
                try:
                    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(), 'Checkout')]"))).click()
                    time.sleep(random.randint(int(WAIT_TIME/2),WAIT_TIME))
                except:
                    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//a[@href="https://www.nike.com/us/en/cart"]'))).click()
                    time.sleep(random.randint(int(WAIT_TIME/2),WAIT_TIME))
                    WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(), 'Checkout')]"))).click()

                #In case of sign-in pop-up
                try:
                    self.signIn()
                    print("....Signed In Succesfully")
                    time.sleep(random.randint(int(WAIT_TIME/2),WAIT_TIME))
                except:
                    pass

                #in case of cart pop-up
                try:
                    iframe = driver.find_element_by_xpath('//iframe[@title="creditCardIframeForm"]')
                    driver.switch_to.frame(iframe)
                    cvv = driver.find_element_by_id('cvNumber')
                    cvv.clear()
                    cvv.send_keys(str(os.getenv('CVV')))
                    time.sleep(1)
                    temp= driver.find_element_by_xpath("//button[contains(text(), 'Save')]").click()
                    time.sleep(1)
                    order= driver.find_element_by_id().click()
                    WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(), 'Order') or contains(text(),'order')]"))).click()
                except:
                    pass
                try:
                    #Wait for page to load and enter cvv
                    print("Placing order...")
                    time.sleep(random.randint(int((WAIT_TIME+3)/2),WAIT_TIME+3))
                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//iframe[@title="Credit Card CVV Form"]')))
                    iframe = driver.find_element_by_xpath('//iframe[@title="Credit Card CVV Form"]')
                    driver.switch_to.frame(iframe)
                    time.sleep(1)
                    cvv = driver.find_element_by_id('cvNumber')
                    cvv.clear()
                    cvv.send_keys(str(os.getenv('CVV')))
                    print("Entered CVV...")
                    #clicking continue to order review
                    print("Continuing to order review...")
                    time.sleep(1)
                    driver.switch_to.default_content()
                    print("switching to default content frame...")
                    time.sleep(random.randint(int(WAIT_TIME/2),WAIT_TIME))
                    """button = driver.find_element_by_xpath("//button[contains(text(), 'Continue To Order Rev')][@data-attr='continueToOrderReviewBtn']")
                    button.click()"""
                    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(), 'Continue To Order Rev')][@data-attr='continueToOrderReviewBtn']"))).click()
                    print("clicked Continue to Order Review...")
                    dateTimeObj = datetime.now()
                    time.sleep(random.randint(int(WAIT_TIME/2),WAIT_TIME))
                    #WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(), 'Place Order')]"))).click()
                    print("clicked Place Order")
                    #button = driver.find_element_by_xpath("//button[contains(text(), 'Place Order')]")
                    #print(button.text)
                except:
                    pass
                print("Order placed on ", dateTimeObj)
                time.sleep(random.randint(int(WAIT_TIME/2),WAIT_TIME))
                self.closeBrowser()
                return True 
        except Exception as e:
            print ("Error...", str(e))
            now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            driver.get_screenshot_as_file('image_error_log/error_screenshot-%s.png' % now)
            self.closeBrowser()
            return False
    def isProductAvailable(self):
        """Checks if product is available"""
        webdriver = self.driver
        try:
            WebDriverWait(webdriver,20).until(EC.visibility_of_element_located((By.XPATH,"//*[@class='buttoncount-1'] | //button[contains(text(), 'Add to Cart')]")))
            btn = webdriver.find_element_by_xpath("//*[@class='buttoncount-1'] | //button[contains(text(), 'Add to Cart')]")
            if btn.text == "Add to Cart" or "Buy" in btn.text:
                return True
            else:
                print(btn.text)
                return False
        except Exception as e :
            print ("Error...", str(e) )
            now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            webdriver.get_screenshot_as_file('image_error_log/error_screenshot-%s.png' % now)
            return False
        return True
    def closeBrowser(self):
        """Closes browser"""
        self.driver.close()
"""
if __name__ == '__main__':
    load_dotenv()
    notification= email_client("Alex",str(os.getenv('SENDER_EMAIL')),str(os.getenv('EMAIL_PASSWORD')))
    new_user = nike_bot(str(os.getenv('NIKE_EMAIL')),str(os.getenv('NIKE_PASSWORD')))
    if new_user.findProduct() == 1:
        notification.send_email("Nike shoe order placed, check your email")
  

"""

