from functions import *


# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.login()
    automation.navigate_to_cameras()
    automation.create_device_group_child("child","child des","camera test parent")
    time.sleep(5)
    automation.close_browser()
