from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

import csv
import creds

class BcScraper:

    def __init__(self) -> None:
        self.SOHList        = []
        self.driver         = self.login()

    def login(self)->webdriver:
        '''Logs into bikecorp'''
        username    = creds.get_username()
        password    = creds.get_password()
        loginURL    = creds.get_login_url()

        # Disable images in window
        options = EdgeOptions()
        options.use_chromium = True
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            'profile.managed_default_content_settings.stylesheets': 2,
            'profile.managed_default_content_settings.plugins': 2,
            'profile.managed_default_content_settings.geolocation': 2,
            }
        options.add_experimental_option("prefs", prefs)

        driver = Edge(executable_path=r"C:\\Program Files (x86)\\Microsoft\\msedgedriver.exe",options=options)

        driver.get(loginURL)

        # Enter credentials into form
        driver.find_element(By.CLASS_NAME, 'form-email').send_keys(username)
        driver.find_element(By.CLASS_NAME, 'form-password').send_keys(password)
        driver.find_element(By.CLASS_NAME, 'cv-log-in').click()

        return driver

    def scrape_stock_from_category(self, catPath:str)-> None:
        '''Scrapes SOH and SKU from given cat name'''
        domain = creds.get_domain()
        params = creds.get_params()

        i = 0
        while True:
            i += 1
            self.driver.get(f'{domain}{catPath}{params}{i}')

            page = self.driver.page_source
            soup = BeautifulSoup(page, features="html.parser")
            products = soup.find_all('div', class_='product')

            if len(products) == 0:
                break

            for product in products:
                sku = product.find('span', class_='widget-productlist-code').text
                soh = product.find('span', class_='widget-productlist-availability').text.split()

                # Checks if oos or in stock. 
                if len(soh) == 3:
                    soh = soh[2]
                else:
                    soh = soh[3]

                self.SOHList.append([sku, soh])
        

    def write_to_csv(self):
        with open('D:/User/Desktop/bikecorp_soh.csv', 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
            for row in self.SOHList:
                wr.writerow(row)
        self.driver.quit()