from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import random
import os

class InstaBot:

    with open('hashtags') as f:
        hashtags = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    hashtags = [x.strip() for x in hashtags]

    def __init__(self):
        executable = GeckoDriverManager().install()
        options = Options()
        options.headless = True
        username = os.environ['USERNAME']
        password = os.environ['PASSWORD']
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox(executable_path=executable, options=options)
        
        
    def login(self):
        bot = self.bot
        bot.get('https://instagram.com/')
        time.sleep(9)
        
        email = bot.find_element_by_name('username')
        password = bot.find_element_by_name('password')
        
        email.clear()
        password.clear()
        
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(8)

        try:
            bot.find_element_by_xpath('//button[text()="Not Now"]').click()
            time.sleep(5)
        except Exception as ex:
            time.sleep(60)
        try:
            bot.find_element_by_xpath('//button[text()="Not Now"]').click()
            time.sleep(5)
        except Exception as ex:
            time.sleep(60)

    def like_post(self):
        bot = self.bot
        time.sleep(6)
        for hashtag in self.hashtags:
            bot.get('https://www.instagram.com/explore/tags/'+hashtag+'/')
            print('Working on #'+hashtag+'.')
            time.sleep(12)
            links = set()
            for i in range(1):
                bot.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(8)
                posts = bot.find_elements_by_class_name('v1Nh3')
                posts = posts[:9]
                [links.add(elem.find_element_by_css_selector('a').get_attribute('href')) for elem in posts ]
                for link in links:
                    n = random.randint(9, 36)
                    bot.get(link)
                    print(link)
                    time.sleep(6)
                    try:
                        bot.find_element_by_css_selector("[aria-label='Like']").click()
                        print('Liked.')
                        time.sleep(n)
                    except Exception as ex:
                        print('Nothing to Like here.')
                        time.sleep(60)
    
    def close_browser(self):
        bot = self.bot
        bot.quit()
                
followers = InstaBot()

followers.login()

followers.like_post()

followers.close_browser()