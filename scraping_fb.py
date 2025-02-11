from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pyotp
import time

def wait_and_click(driver, by, locator, timeout=60, retries=3, sleep_time=10):
    """Waits for an element to be clickable and clicks it."""
    wait = WebDriverWait(driver, timeout)
    for attempt in range(retries):
        try:
            element = wait.until(EC.visibility_of_element_located((by, locator)))
            element = wait.until(EC.element_to_be_clickable((by, locator)))
            element.click()
            return
        except (StaleElementReferenceException, TimeoutException) as e:
            print(f"Intento {attempt + 1}: {str(e)}, reintentando...")
            time.sleep(sleep_time)
    print(f"Error: No se pudo hacer clic en el elemento después de {retries} intentos.")
    return None

def main():
    # Configuración del navegador
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://auth.metaenterprise.com/login")
    wait = WebDriverWait(driver, 20)
    
    # Iniciar sesión
    email = wait.until(EC.presence_of_element_located((By.ID, 'js_0')))
    email.send_keys("joaquin.furlan@claro.com.ar")
    wait_and_click(driver, By.XPATH, "//*[@role='button']")
    print("Botón 'Usuario' clickeado.")

    # Leer la contraseña
    with open("pw.txt", "r") as file:
        password_str = file.read().strip()

    # Ingresar contraseña
    password = wait.until(EC.presence_of_element_located((By.ID, 'js_f')))
    password.send_keys(password_str)
    wait_and_click(driver, By.XPATH, "(//div[@role='button' and .//div[text()='Continuar']])[1]")
    print("Botón de inicio de sesión clickeado.")

    # Seleccionar Autenticación
    wait_and_click(driver, By.ID, 'js_q')
    print("Botón de autenticación clickeado.")
    
    wait_and_click(driver, By.XPATH, "(//div[@role='button' and .//div[text()='Continuar']])[2]")
    print("Botón de continuar clickeado.")

    # Manejar la autenticación 2FA
    authField = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//div[@role='dialog']//input[@aria-disabled='false']")))
    
    if authField:
        # Obtener el token de Google Authenticator
        secret = "T234HEP775RIRJXP" 
        totp = pyotp.TOTP(secret)
        token = totp.now()
        print("Token Generado:", token)

        # Ingresar el token en el campo 2FA
        authField.send_keys(token)
        print("Token ingresado.")

    wait_and_click(driver, By.XPATH, "(//div[@role='button' and .//div[text()='Confirmar']])")
    print("Botón de confirmar clickeado.")

    # Navegar a Insight
    wait_and_click(driver, By.XPATH, "//*[@role='link' and .//*[text()='Abrir solicitud']]")
    print("Botón 'Abrir solicitud' clickeado.")
    
    driver.get('https://partners.metaenterprise.com/actionable_insights/global/report_builder')
    
    # Navegar a Data
    wait_and_click(driver, By.XPATH, "//a[.//*[text()='Data']]")
    print("Botón Data clickeado.")
    time.sleep(15)  # Esperar que se cargue la página

    # Ejecutar acciones y exportar datos
    wait_and_click(driver, By.XPATH, "//div[@role='button' and .//div[text()='Acciones']]")
    print("Botón de Acción clickeado.")
    
    wait_and_click(driver, By.XPATH, "//div[@role='menuitem' and .//div[text()='Exportar']]")
    print("Botón Exportar clickeado.")
    
    wait_and_click(driver, By.XPATH, "//div[@role='button' and .//div[text()='Descargar']]")
    print("Botón Descargar clickeado.")
    time.sleep(5)

    # Cerrar el navegador
    driver.quit()

if __name__ == "__main__":
    main()
