from functions import *


# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.login()
    automation.click_device_actions(1)
    automation.remove_device()
    automation.continue_action()
    automation.enter_delete_text()
    time.sleep(1)
    automation.click_delete_button()
    time.sleep(2)
    automation.close_browser()
