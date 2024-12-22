from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# Geckodriver yolu
geckodriver_path = "C:/Users/ormec/Downloads/geckodriver-v0.35.0-win32/geckodriver.exe"

# Firefox tarayıcı ayarları
firefox_options = Options()
firefox_options.binary_location = "C:/Program Files/Mozilla Firefox/firefox.exe"  # Firefox'un doğru yolunu belirtin
firefox_options.headless = False  # Tarayıcıyı görünür başlatmak için

# Geckodriver servisini başlat
service = Service(executable_path=geckodriver_path)

# WebDriver'ı başlat
driver = webdriver.Firefox(service=service, options=firefox_options)

# Bir web sayfasına git
driver.get("https://www.google.com")

# Sayfanın başlığını yazdır
print("Sayfa başlığı:", driver.title)

# Tarayıcıyı kapat
driver.quit()
