from functions import *


# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.login()
    automation.navigate_to_devices()
    automation.edit_groups()
    time.sleep(3)
    automation.click_parent()
    time.sleep(3)
    automation.drag_and_drop()
    time.sleep(3)
    automation.save_device_to_group()
    time.sleep(3)
    #automation.close_browser()
