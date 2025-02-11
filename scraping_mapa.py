from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pyotp
import time

# Configuración del navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://auth.metaenterprise.com/login")
wait = WebDriverWait(driver, 20) 

# Iniciar sesión
email = wait.until(EC.presence_of_element_located((By.ID, 'js_0')))
email.send_keys("joaquin.furlan@claro.com.ar")

continue_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//*[@role='button']")))
continue_button.click()
print("Botón 'Continuar' clickeado.")

# Lee la contraseña
with open("pw.txt", "r") as file:
    password_str = file.read().strip()

# Ingresar contraseña
password = wait.until(EC.presence_of_element_located((By.ID, 'js_g')))
password.send_keys(password_str)

login_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[@role='button' and .//div[text()='Continuar']])[1]")))
login_button.click()
print("Botón de inicio de sesión clickeado.")

# Seleccionar Autenticación
authentication_button = wait.until(
    EC.element_to_be_clickable((By.ID, 'js_s')))
authentication_button.click()
print("Botón de autenticación clickeado.")

# Hacer clic en el botón de continuar
continuar_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[@role='button' and .//div[text()='Continuar']])[2]")))
continuar_button.click()
print("Botón de continuar clickeado.")

# Manejar posible StaleElementReferenceException al ubicar el campo de autenticación
for attempt in range(3):
    try:
        authField = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']//input[@aria-disabled='false']")))
        if authField:
            # Obtener el token de Google Authenticator
            secret = "RUTSAV7SDAHMJVIS" 
            totp = pyotp.TOTP(secret)
            token = totp.now()
            print("Token Generado:", token)

            # Ingresar el token en el campo 2FA
            authField.send_keys(token)
            print("Token ingresado.")
            break
    except StaleElementReferenceException:
        print(f"Intento {attempt + 1}: Elemento no válido, reintentando...")
        time.sleep(1)  # Espera un segundo antes de intentar nuevamente
else:
    print("No se pudo encontrar o interactuar con el campo de autenticación después de varios intentos.")
    
continuar_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "(//div[@role='button' and .//div[text()='Confirmar']])")))
continuar_button.click()
print("Botón de continuar clickeado.")
time.sleep(10)

# Hacer clic en el botón de inicio de sesión con ActionChains
insight_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//*[@role='link' and .//*[text()='Abrir solicitud']]")))
insight_button.click()
print("Botón insight clickeado.")


 # Hacer clic en el botón de inicio de sesión con ActionChains
informes_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='listitem' and .//div[text()='Network']]")))
informes_button.click()
print("Botón de Informes")
time.sleep(5)

# Hacer clic en el botón del combobox primero
pais_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, "//div[@role='combobox']"))
)
pais_button.click()
print("Combobox abierto.")

# Esperar a que aparezca la opción 'Claro (AR)' en el menú desplegable y hacer clic
claro_option = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Claro (AR)')]"))
)
claro_option.click()
print("Opción 'Claro (AR)' seleccionada.")
 
 # Hacer clic en el botón de inicio de sesión con ActionChains
informes_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='listitem' and .//div[text()='Network']]")))
informes_button.click()
print("Botón Network")
time.sleep(5)

 # Hacer clic en el botón de inicio de sesión con ActionChains
informes_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='listitem' and .//div[text()='Rendimiento']]")))
informes_button.click()
print("Botón Rendimiento")
time.sleep(3)

# Navega directamente a la URL
driver.get("https://partners.metaenterprise.com/actionable_insights/network_insights/ni_subcity?locale=es_LA&partner_id=24694741174")

# Mensaje de confirmación
print("Navegador a Mapas.")
time.sleep(5)

xpath_zoom = "//div[@id='XMPPInsights']/div/div/div/div[2]/div/div/div/div/div/div[2]/span/div/div[2]/div/span/div/div[2]/div/div"
filtro_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, xpath_zoom))
)
filtro_button.click()
print("Botón de filtro.")

xpath_zoom = "//div[4]/div/div/div/div/div[2]/div/div"
filtro1_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, xpath_zoom))
)
filtro1_button.click()
print("Botón de filtro1.")

xpath_zoom = "//div[4]/div/div/div/div/div[2]/div/div"
filtro1_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, xpath_zoom))
)
filtro1_button.click()
print("Botón de filtro1.")

id_locator = "//*[@id='torrent-scanner-popup']"
filtro2_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, id_locator))
)
filtro2_button.click()
print("Botón de filtro2.")

# Esperar hasta que el elemento con el ID 'js_4g' esté presente y se pueda hacer clic
buscador = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH,"//div[@id='vizContent']/div/div/div/div[6]/div/div/div/div[2]/div/div/div/div/div[2]/div/div/input")))
buscador.click()
# Escribir "Centro histórico de Córdoba" en el campo de entrada
buscador.send_keys("Centro histórico de Córdoba")
time.sleep(2)
buscador.send_keys(Keys.ARROW_DOWN,Keys.ENTER)
time.sleep(5)

xpath_zoom = "//div[2]/div[2]/div/span/div/div[2]/div/div"
zoom_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, xpath_zoom))
)
zoom_button.click()
print("Botón de zoom atrás clickeado.")

xpath_zoom = "//div[2]/div[2]/div/span/div/div[2]/div/div"
zoom1_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, xpath_zoom))
)
zoom1_button.click()
print("Botón de zoom1 atrás clickeado.")

xpath_zoom = "//div[2]/div[2]/div/span/div/div[2]/div/div"
zoom2_button = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, xpath_zoom))
)
zoom2_button.click()
print("Botón de zoom2 atrás clickeado.")

time.sleep(20)
# Cerrar el navegador
driver.quit()