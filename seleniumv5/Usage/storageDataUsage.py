from functions import *


# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.login()
    automation.navigate_to_settings()
    automation.storage_data_usage()
    automation.private_storage_logs()
    time.sleep(2)
    automation.close_browser()
