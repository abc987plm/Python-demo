from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def message(emailaddr, text):
    browser = webdriver.Firefox()
    browser.get('https://email.163.com/')
    time.sleep(2)

    iframe = browser.find_element_by_tag_name('iframe')
    browser.switch_to_frame(iframe)
    login = browser.find_element_by_name('email')
    print(login.tag_name, login.text)
    login.send_keys('your_email', Keys.TAB, 'password')
    land = browser.find_element_by_id('dologin').click()
    time.sleep(2)

    browser.switch_to.default_content()  # 退出frame，没有这一句后续的元素定位会出错
    writhe = browser.find_element_by_id('_mail_component_59_59')
    writhe.click()

    writher = browser.find_element_by_xpath(
        '/html/body/div[2]/div[1]/div[2]/div[1]/section/header/div[1]/div[1]/div/div[2]/div/input')
    writher.send_keys(emailAddr, Keys.TAB, 'Mail_theme', Keys.TAB, text)
    time.sleep(2)
    setd = browser.find_element_by_xpath('//*[@id="_mail_button_9_223"]').click()


emailAddr = input("Recipient's mailbox address: ")
text = input('Mail content :')

message(emailAddr, text)