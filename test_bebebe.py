from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class OpenBMCTest(unittest.TestCase):

    def setUp(self):
        
        firefox_options = Options()

        # firefox_options.add_argument('--headless')
        
        firefox_options.add_argument('--no-sandbox')
        #какая то песочница линукс
        firefox_options.add_argument('--disable-dev-shm-usage')
        #так типо память стабильнее
        firefox_options.add_argument('--width=1200')
        firefox_options.add_argument('--height=800')
        
        # что б фаерфокс с sll работал 
        firefox_options.set_preference('accept_insecure_certs', True)
        firefox_options.set_preference('webdriver_accept_untrusted_certs', True)
        firefox_options.set_preference('webdriver_assume_untrusted_issuer', True)
        
        # время ожидания что б страницы не блочило 
        firefox_options.set_preference('dom.max_script_run_time', 30)
        firefox_options.set_preference('dom.max_chrome_script_run_time', 30)
        
        geckodriver_path = os.path.join(os.path.expanduser('~'), 'Рабочий стол', 'AquariusTesting', 'geckodriver')

       
        if not os.path.exists(geckodriver_path):
            print(f"ОШИБКА: Файл {geckodriver_path} не найден!")
            raise FileNotFoundError(f"GeckoDriver не найден по пути: {geckodriver_path}")
        
        #сервис для управления драйвером
        service = Service(executable_path=geckodriver_path)
        
        try:
            self.driver = webdriver.Firefox(service=service, options=firefox_options)
            #обект браузера
        except Exception as e:
            print(f"Ошибка при запуске Firefox: {e}")
            raise
        
        self.driver.implicitly_wait(20)
        self.base_url = "https://localhost:2443"
        self.wait = WebDriverWait(self.driver, 30)
        
        self.driver.set_window_size(1200, 800)

    def tearDown(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()


    def accept_ssl_certificate(self):
        try:
            advanced_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "advancedButton"))
            )
            advanced_button.click()
            time.sleep(2)
            
            accept_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "exceptionDialogButton"))
            )
            accept_button.click()
            time.sleep(3)
        except Exception as e:
            print(f"SSL предупреждение не появилось : {e}")

    def login(self, username, password):
        self.driver.get(self.base_url)
        time.sleep(3)
        
        try:
            username_field = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[class='form-control'], input[id='username']"))
            )
            password_field = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[class='form-control form-control-with-button'], input[id='password']"))
            )
            
            username_field.send_keys(username)
            password_field.send_keys(password)
            
            password_field.send_keys(Keys.RETURN)
            
            
        except Exception as e:
            print(f"Ошибка при вводе логина: {e}")
            
            raise
            
        time.sleep(5)
        

    def test_1_successful_login(self):

        self.login("root", "0penBmc")
        self.assertNotEqual(self.driver.current_url, '{self.base_url}/#/login')
    
    def test_2_fyfyfy_login(self):
       self.login("root", "fyfyfy")
       #time.sleep(10)
       #юрл специально такой стремненький, не первая попытка войти
       self.assertEqual(self.driver.current_url, 'https://localhost:2443/?next=/login#/login')

    def test_3_out_session(self):
        self.login("root", "0penBmc")
        try:
            user_dropdown_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "app-header-user__BV_toggle_"))
            )
            user_dropdown_button.click()
            time.sleep(2)
            logout_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-test-id='appHeader-link-logout']"))
            )
            logout_button.click()
            time.sleep(3)
            current_url = self.driver.current_url
            print(current_url)
            self.assertEqual(current_url, 'https://localhost:2443/#/login')
            
        except Exception as e:
            print(f"Ошибка при открытии списка: {e}")
            raise

    def test_4_power_status(self):
        self.login("root", "0penBmc")
        try:
            link_power = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#/operations/server-power-operations']"))
            )
            link_power.click()
            time.sleep(3)
            server_status_element = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test-id='powerServerOps-text-hostStatus']"))
            )
            server_status = server_status_element.text
            self.assertEqual(server_status, "Off")
            
        except Exception as e:
            print(f"Ошибка при поиске статуса сервиса {e}")
            raise

    def test_5_status_kvm(self):
        self.login("root", "0penBmc")
        try:
            aside_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test-id='nav-button-operations']"))
            )
            aside_button.click()
            time.sleep(2)
            link_kvm = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#/operations/kvm']"))
            )
            link_kvm.click()
            time.sleep(3)
            kvm_status_element = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span[class='d-none d-md-inline']"))
            )
            server_status = kvm_status_element.text
            self.assertEqual(server_status, "Disconnected")
            
        except Exception as e:
            print(f"Ошибка при поиске статуса сервиса {e}")
            raise

if __name__ == "__main__":
    # Запуск теста через unittest
    unittest.main()