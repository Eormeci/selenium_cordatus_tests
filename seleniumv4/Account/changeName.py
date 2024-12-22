from functions import *


# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.login()
    automation.navigate_to_settings()
    automation.change_acc_name("test")
    automation.save_changes()
    time.sleep(4)
    automation.close_browser()
