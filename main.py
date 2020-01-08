from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import static_data_file as cfg
import pandas as pd
import pyfiglet
import time
import json
import os


class InstagramScraper:
    print(pyfiglet.figlet_format("SMO", font="isometric1"))
    print("\t\t- Social Media Observatory -\n")

    def __init__(self, email, password):
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("intl.accept_languages", "en-us")
        firefox_profile.update_preferences()
        options = Options()
        options.headless = False
        self.driver = webdriver.Firefox(options=options, firefox_profile=firefox_profile)
        self.email = email
        self.password = password

    def login(self):
        self.driver.get(cfg.loginUrl)
        try:
            email_input = WebDriverWait(self.driver, cfg.secondsToWait).until(
                ec.presence_of_element_located((By.NAME, cfg.usernameInputElementNameToLookFor))
            )
            email_input.send_keys(self.email)
            password_input = WebDriverWait(self.driver, cfg.secondsToWait).until(
                ec.presence_of_element_located((By.NAME, cfg.emailInputElementNameToLookFor))
            )
            password_input.send_keys(self.password)
            password_input.send_keys(Keys.ENTER)
        finally:
            time.sleep(cfg.secondsToWait)

    @staticmethod
    def get_info_for_start_user_and_loop_through_followers():
        bot.get_first_info(cfg.scraperStartProfileUrl)
        time.sleep(5)
        followers = bot.followers()
        bot.followings()
        for follower in followers:
            time.sleep(cfg.secondsToWait)
            cfg.privateAccount = False
            bot.get_first_info(follower)
            if not cfg.privateAccount:
                if cfg.followersAmount > 0:
                    bot.followers()
                if cfg.followingsAmount > 0:
                    bot.followings()

    def get_first_info(self, scraper_profile_url):
        self.driver.get(scraper_profile_url)
        time.sleep(cfg.secondsToWait)
        soup = BeautifulSoup(self.driver.page_source, cfg.pythonParserUsedByBS4)
        user_data = soup.find_all(cfg.metaTagName, attrs={cfg.propertyKeyName: cfg.propertyValueName})
        text = user_data[0].get(cfg.contentPropertyName).split()  # print(', '.join(str(user_data)))
        script_tag_list = soup.find_all(cfg.scriptTagName)
        script_tag_inner_html = ''
        for tag in script_tag_list:
            if str(tag).__contains__(cfg.userIdStringToLookFor):
                script_tag_inner_html = tag
        user_id_end_index = str(script_tag_inner_html).split(cfg.userIdStringToLookFor, 1)[1].find('","')
        user_id = str(script_tag_inner_html).split(cfg.userIdStringToLookFor, 1)[1][0:user_id_end_index]
        cfg.username = '%s %s %s' % (text[-3], text[-2], text[-1])
        print('processing ' + cfg.username)
        if str(text[0]).__contains__('See') or str(text[0]).__contains__('Follow') or \
                str(text[0]).__contains__('videos') or str(text[0]).__contains__('from') or \
                str(user_data).__contains__('Private') or str(user_data).__contains__('privat'):
            print("\naccount is private - seen from user info\n")
            cfg.privateAccount = True
            return
        else:  # TODO: find (better) way to see if acc is private here
            i = 0
            while i < 3:
                if text[i].endswith('m'):
                    text[i] = str(text[i]).replace(".", "").replace("m", "00000")
                if text[i].endswith('k'):
                    text[i] = str(text[i]).replace(".", "").replace("k", "00")
                if str(text[i]).__contains__(","):
                    text[i] = str(text[i]).replace(",", "")
                i = i + 2
            cfg.followersAmount = int(text[0])
            cfg.followingsAmount = int(text[2])
        if not cfg.privateAccount:
            # self.print_findings(cfg.username, text[0], text[2], text[4], user_id)
            path_to_json = os.getcwd() + '/Outputs/' + cfg.username + '.json'
            if not os.path.exists(path_to_json):
                os.makedirs(os.path.dirname(path_to_json), exist_ok=True)
            f = open(file=path_to_json, mode='w+', encoding="utf-8")
            f.write('{\n\t\"Username\": \"' + cfg.username + '\",\n\t\"Number of Followers\": ' + text[0] +
                    ',\n\t\"Number of Followings\": ' + text[2] + ',\n\t\"Total number of Posts\": ' + text[4] +
                    ',\n\t\"User ID\": ' + user_id + ',\n')
            f.close()

    def followers(self):
        followers_link = self.driver.find_element_by_css_selector('ul li a')
        followers_link.click()
        self.driver.switch_to.default_content()
        try:
            WebDriverWait(self.driver, 60).until(ec.presence_of_element_located((By.CSS_SELECTOR, cfg.listElement)))
        except TimeoutException:
            print("\naccount is private - seen from followers")
            return
        followers_list = self.driver.find_element_by_css_selector(cfg.listElement)
        followers_list.click()
        self.driver.switch_to.default_content()
        time.sleep(10)
        try:
            WebDriverWait(self.driver, 60).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'li')))
            number_of_followers_in_list = len(followers_list.find_elements_by_css_selector('li'))
        except StaleElementReferenceException:
            print("test - " + str(cfg.followersAmount))
            number_of_followers_in_list = cfg.followersAmount
            pass
        action_chain = webdriver.ActionChains(self.driver)
        if cfg.followersAmount >= cfg.maximumFollowerToLookAt:
            cfg.followersAmount = cfg.maximumFollowerToLookAt
        if cfg.followersAmount <= cfg.maximumFollowerToLookAt:
            cfg.maximumFollowerToLookAt = cfg.followersAmount
        i = 0
        while number_of_followers_in_list < cfg.maximumFollowerToLookAt:
            action_chain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            i = i + 1
            time.sleep(cfg.secondsToWait)
            if number_of_followers_in_list == len(followers_list.find_elements_by_css_selector('li')):
                break
            else:
                number_of_followers_in_list = len(followers_list.find_elements_by_css_selector('li'))
        followers = []
        self.driver.switch_to.default_content()
        try:
            WebDriverWait(self.driver, 60).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'li')))
        except StaleElementReferenceException:
            print("\nERROR finding li element - element not found - (╯°□°）╯︵ ┻━┻")
            return
        list_element = followers_list.find_elements_by_css_selector('li')
        for user in list_element:
            user_link = user.find_element_by_css_selector('a').get_attribute('href')
            followers.append(user_link)
        panda_data_frame = pd.DataFrame(followers)  # TODO: format panda dataFrame
        path_to_json = os.getcwd() + '/Outputs/' + cfg.username + '.json'
        if os.path.exists(path_to_json):
            f = open(file=path_to_json, mode='a+', encoding="utf-8")
            json_str = json.dumps(json.loads(panda_data_frame.to_json()), indent=8, sort_keys=True)
            f.write('\t\"followers\": \n\t' + json_str + '\t,\n')
            f.close()
        # self.print_follower_links(followers)
        find_x_button = self.driver.find_element_by_css_selector('div button svg')
        find_x_button.click()
        return followers

    def followings(self):
        followings_link = self.driver.find_elements_by_css_selector('ul li a')[1]
        followings_link.click()
        self.driver.switch_to.default_content()
        time.sleep(cfg.secondsToWait)
        try:
            WebDriverWait(self.driver, 60).until(ec.presence_of_element_located((By.CSS_SELECTOR, cfg.listElement)))
        except TimeoutException:
            print("account is private - seen from followings\n\n")
            return
        followings_list = self.driver.find_element_by_css_selector(cfg.listElement)
        followings_list.click()
        time.sleep(15)
        followings = []
        self.driver.switch_to.default_content()
        try:
            WebDriverWait(self.driver, 60).until(ec.presence_of_element_located((By.CSS_SELECTOR, 'li')))
        except StaleElementReferenceException:
            print("\nERROR finding li element - element not found - (╯°□°）╯︵ ┻━┻")
            return
        list_element = followings_list.find_elements_by_css_selector('li')
        for user in list_element:
            followers_link = user.find_element_by_css_selector('a').get_attribute('href')
            followings.append(followers_link)
        panda_data_frame = pd.DataFrame(followings)  # TODO: format panda dataFrame
        path_to_json = os.getcwd() + '/Outputs/' + cfg.username + '.json'
        if os.path.exists(path_to_json):
            f = open(file=path_to_json, mode='a+', encoding="utf-8")
            json_str = json.dumps(json.loads(panda_data_frame.to_json()), indent=8, sort_keys=True)
            f.write('\t\"followings\": \n\t' + json_str + '\t\n}')
            f.close()
        # self.print_followings_links(followings)
        close_followings = self.driver.find_element_by_css_selector('div button svg')
        close_followings.click()

    @staticmethod
    def print_findings(user, followers, following, number_of_posts, user_id):
        print('Username: ' + user)
        print('Number of Followers: ' + followers)
        print('Number of Followings: ' + following)
        print('Total number of Posts: ' + number_of_posts)
        print('User ID: ' + user_id)

    @staticmethod
    def print_follower_links(followers):
        print('\n' + cfg.username + '\'s followers: ' + str(followers))

    @staticmethod
    def print_followings_links(followings):
        print('\n' + cfg.username + '\' followings: ' + str(followings) + '\n\n')

    def quit(self):
        self.driver.quit()


bot = InstagramScraper(cfg.loginUser, cfg.loginPassword)
bot.login()
bot.get_info_for_start_user_and_loop_through_followers()
bot.quit()
