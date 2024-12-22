from functions import *


# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.login()
    automation.navigate_to_devices()
    automation.device_connection_online()
    time.sleep(3)
    automation.device_connection_offline()
    time.sleep(3)
    automation.device_connection_online()
    time.sleep(3)
    automation.device_connection_offline()
    time.sleep(3)
    automation.close_browser()