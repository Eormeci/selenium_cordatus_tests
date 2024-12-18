from functions import *

# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.login()
    automation.navigate_to_devices()
    automation.rename_device("new name")
    time.sleep(3)
    automation.refresh_device()
    time.sleep(5)
    automation.close_browser()
