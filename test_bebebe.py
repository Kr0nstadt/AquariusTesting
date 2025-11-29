import datetime
import logging
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
        logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
        self.logger = logging.getLogger(self.__class__.__name__)
        
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
            self.logger.error(f"Файл {geckodriver_path} не найден!")
            raise FileNotFoundError(f"GeckoDriver не найден по пути: {geckodriver_path}")
        
        #сервис для управления драйвером
        service = Service(executable_path=geckodriver_path)
        
        try:
            self.driver = webdriver.Firefox(service=service, options=firefox_options)
            #обект браузера
        except Exception as e:
            self.logger.error(f"Ошибка при запуске Firefox: {e}")
            raise
        
        self.driver.implicitly_wait(20)
        self.base_url = "https://localhost:2443"
        self.wait = WebDriverWait(self.driver, 30)
        self.logger.info(f"Браузер запущен: {datetime.datetime.now().time()}, URL: {self.base_url}")
        self.driver.set_window_size(1200, 800)

    def tearDown(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
            self.logger.info("Браузер закрыт")


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
            self.logger.info("SSL сертификат принят")
        except Exception as e:
            self.logger.info(f"SSL предупреждение не появилось: {e}")

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
            self.logger.info(f"Попытка входа пользователя: {username}")
            
        except Exception as e:
            self.logger.error(f"Ошибка при вводе логина: {e}")
            raise
            
        time.sleep(5)
        

    def test_1_successful_login(self):
        self.logger.info("Запуск теста: Успешный вход")
        self.login("root", "0penBmc")
        self.assertNotEqual(self.driver.current_url, f'{self.base_url}/#/login')
        self.logger.info("Тест успешного входа пройден")
    
    def test_2_fyfyfy_login(self):
        self.logger.info("Запуск теста: Неуспешный вход с неверным паролем")
        self.login("root", "fyfyfy")
        #time.sleep(10)
        #юрл специально такой стремненький, не первая попытка войти
        self.assertEqual(self.driver.current_url, 'https://localhost:2443/?next=/login#/login')
        self.logger.info("Тест неуспешного входа пройден")

    def test_3_out_session(self):
        self.logger.info("Запуск теста: Выход из сессии")
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
            self.logger.info(f"Текущий URL после выхода: {current_url}")
            self.assertEqual(current_url, 'https://localhost:2443/#/login')
            self.logger.info("Тест выхода из сессии пройден")
            
        except Exception as e:
            self.logger.error(f"Ошибка при выходе из сессии: {e}")
            raise

    def test_4_power_status(self):
        self.logger.info("Запуск теста: Проверка статуса питания")
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
            self.logger.info(f"Статус сервера: {server_status}")
            self.assertEqual(server_status, "Off")
            self.logger.info("Тест проверки статуса питания пройден")
            
        except Exception as e:
            self.logger.error(f"Ошибка при поиске статуса сервера: {e}")
            raise

    def test_5_status_kvm(self):
        self.logger.info("Запуск теста: Проверка статуса KVM")
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
            self.logger.info(f"Статус KVM: {server_status}")
            self.assertEqual(server_status, "Disconnected")
            self.logger.info("Тест проверки статуса KVM пройден")
            
        except Exception as e:
            self.logger.error(f"Ошибка при поиске статуса KVM: {e}")
            raise

if __name__ == "__main__":
    # Запуск теста через unittest
    unittest.main()