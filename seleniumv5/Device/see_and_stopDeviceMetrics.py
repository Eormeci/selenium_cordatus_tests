from functions import *

# Jtop kapalı ise startJtop.py dosyasını çalıştırın.

# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.login()
    automation.navigate_to_devices()
    automation.device_connection_online()
    time.sleep(3)
    automation.see_device_metrics()
    time.sleep(5)
    automation.stop_jtop_service()
    time.sleep(5)
    automation.close_browser()
