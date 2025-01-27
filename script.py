from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time

#opciones de Chrome
options = Options()
user_agents = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
options.add_argument(f"user-agent={user_agents}")
options.add_argument("--disable-web-security")
options.add_argument("--disable-notifications")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--allow-insecure-localhost")
options.add_argument("--no-sandbox")
options.add_argument("--log-level=3")
options.add_argument("--no-default-browser-check")
options.add_argument("--no-first-run")
options.add_argument("--disable-blink-features=AutomationControlled")

#parametros para omitir al inicio de chromedriver
exp_opt = [
    "enable-automation",
    "ignore-certificate-errors",
    "enable-logging"
]
options.add_experimental_option("excludeSwitches", exp_opt)
prefs = {
    "profile.default_content_setting_values.notifications": 2,
    "intl.accept_languages": ["es-ES", "es"],
    "credentials_enable_service": False
}
options.add_experimental_option("prefs", prefs)


# Configuración de credenciales y URL
fortigate_url = "https://172.23.0.250/login"
username = ""
password = ""
users_to_filter = ["u62061", "u62699", "u61622"]

# Configuración del WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Definir WebDriverWait antes de usarlo
wait = WebDriverWait(driver, 10)




try:
    # Navegar al sitio e iniciar sesión
    driver.get(fortigate_url)

    try:
           advanced_button = wait.until(EC.presence_of_element_located((By.ID, "details-button")))  # "Configuración avanzada"
           advanced_button.click()
           proceed_link = wait.until(EC.presence_of_element_located((By.ID, "proceed-link")))  # "Ir a 172.23.0.250"
           proceed_link.click()
    except Exception as e:
           print("No se encontró la página de advertencia o ya se ha pasado.")


    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login_button").click()

    # Ir a Log & Report > System Events
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Log & Report"))).click()
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "System Events"))).click()

    # Cambiar el filtro a "VPN Events"
    event_filter = wait.until(EC.presence_of_element_located((By.ID, "event_filter_dropdown")))
    event_filter.click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//option[text()='VPN Events']"))).click()

    # Configurar el filtro de fecha al día anterior
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    date_filter_start = driver.find_element(By.ID, "start_date_input")  # Cambia ID según corresponda
    date_filter_start.clear()
    date_filter_start.send_keys(f"{yesterday} 00:00:00")

    date_filter_end = driver.find_element(By.ID, "end_date_input")  # Cambia ID según corresponda
    date_filter_end.clear()
    date_filter_end.send_keys(f"{yesterday} 23:59:59")

    # Filtrar por cada usuario y descargar logs
    for user in users_to_filter:
        user_filter = driver.find_element(By.ID, "user_filter_input")  # Cambia ID según corresponda
        user_filter.clear()
        user_filter.send_keys(user)
        user_filter.send_keys(Keys.RETURN)

        # Descargar logs
        download_button = wait.until(EC.element_to_be_clickable((By.ID, "download_button")))  # Ajusta el ID
        download_button.click()

        time.sleep(5)  # Esperar la descarga

finally:
    driver.quit()
