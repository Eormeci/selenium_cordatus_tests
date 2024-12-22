from functions import *


# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.login()
    automation.navigate_to_settings()
    automation.scroll_down()
    automation.enter_current_password()
    automation.type_new_passwords("Test123.")
    automation.update_password_button()
    time.sleep(2)
    automation.close_browser()
