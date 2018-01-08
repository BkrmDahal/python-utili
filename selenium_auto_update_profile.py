"""update booking.com profile using selenium"""

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


''' Open Fire box'''
driver = webdriver.Firefox()
driver.maximize_window()


''' Open booking_com'''
base_url = "https://secure.booking.com/"
driver.get(base_url)


'''Login'''
WebDriverWait(driver, 30).until(
     EC.presence_of_element_located((By.XPATH,"(//li[@id='current_account']/a/div/span)[2]"))).click()
driver.find_element_by_name("username").clear()
driver.find_element_by_name("username").send_keys("bkrm.dahal@gmail.com")
driver.find_element_by_name("password").clear()
temp = driver.find_element_by_name("password")
temp.send_keys("*******")
temp.send_keys(Keys.ENTER)
time.sleep(10)


'''Edit the profile'''
driver.find_element_by_link_text("Edit your settings").click()
driver.find_element_by_xpath("//button[@type='button']").click()


# upload picture
driver.find_element_by_id("avatar-upload-file").clear()
driver.find_element_by_id("avatar-upload-file").send_keys("C:\\Users\\bikram.dahal\\Downloads\\2016-01-06 02.05.49.jpg")
driver.find_element_by_xpath("//body[@id='b2mysettingsPage']/div[10]/div/div[4]/span").click()

# add nickname
WebDriverWait(driver, 30).until(
     EC.presence_of_element_located((By.ID,"nickname"))).clear()
driver.find_element_by_id("nickname").send_keys("bikramdahal")

# Choose the age
Select(driver.find_element_by_name("b_age_group")).select_by_value("45_to_54")

# Choose from country
Select(driver.find_element_by_name("country_code")).select_by_visible_text("Nepal")

# choose the email fequency
driver.find_element_by_xpath("(//input[@name='frequency_bkrm.dahal@gmail.com'])[3]").click()
    

print("job done!!!!!")


'''Bikram Dahal'''
