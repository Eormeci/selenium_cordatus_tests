from functions import *


# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.login()
    automation.navigate_to_repositories()
    automation.create_repository()
    automation.enter_repository_name("test12")
    time.sleep(1)
    automation.enter_repository_desc("test desc")
    automation.press_create()
    automation.press_close()
    time.sleep(2)
    automation.close_browser()
