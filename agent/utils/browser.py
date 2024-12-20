import time
import requests
import json
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


class Browser:
    def __init__(self) -> None:
        self.browser = self.initBrowser()

    def initBrowser(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        #chrome_options.add_argument("--disable-gpu")  # Disable GPU (optional for headless mode)
        chrome_options.add_argument("--remote-debugging-port=9222")  # Enable debugging
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--proxy-server=socks5://localhost:9050")

        #chrome_options.add_argument("--disable-gpu")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    def GetCaptaImage(self):
        try:
            element = self.browser.find_element(By.ID, "captcha_img")
            filename = f"{uuid.uuid4()}.png"
            element.screenshot(filename)
            return filename
        except Exception as e:
            print(e)
            exit(1)
            pass

    def completeCapta(self,endpoint):
        fileName = self.GetCaptaImage()
        with open(fileName,"rb") as img:
            files = {'file': img}
            response = requests.post(endpoint, files=files)
            print(response.content)
            value = json.loads(response.content).get("text","NUL")
            if value == "NUL":
                print("Need to retry---------")
                #self.captaRetry()
            else:
                self.fillCapta(value)
    def fillCapta(self, captaText):
        try:
            element = self.browser.find_element(By.ID, "imagestring")
            element.send_keys(captaText.lower().replace(" ",""))
        except Exception as e:
            print(e)
            pass
    def loginSubmit(self):
        try:
            element = self.browser.find_element(By.NAME, "submit")
            element.click()
        except Exception as e:
            print(e)
            pass
    def loginStatus(self):
        try:
            element = self.browser.find_element(By.ID, "forums")
            return True
        except Exception as e:
            return False

    def fillCreds(self, user, pas):
        try:
            element = self.browser.find_element(By.NAME, "username")
            element.send_keys(user)
            element = self.browser.find_element(By.NAME, "password")
            element.send_keys(pas)
        except Exception as e:
            print(e)
            pass
    def breachFormLogin(self, user, password, endpoint):
        self.browser.get("https://breachforums.st/member.php?action=login")
        self.fillCreds(user, password)
        self.completeCapta(endpoint)
        self.loginSubmit()
        return self.loginStatus()
        
        pass

