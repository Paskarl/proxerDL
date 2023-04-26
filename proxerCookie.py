from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager


#TODO: Implement auto. cookie grab
browser = webdriver.Edge(EdgeChromiumDriverManager().install())

browser.get("https://proxer.me/login")



username = browser.find_element(by=By.NAME, value="username")
username.send_keys

password = browser.find_element('name','password')
password.send_keys('Ihr Passwort')


submit_button = browser.find_element('xpath','//button[@type="submit"]')
submit_button.click()

cookies = browser.get_cookies()

for cookie in cookies:
    print(cookie)
    
input()