from functions import *

if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()
    automation.login()
    automation.navigate_to_devices()
    automation.device_connection_online()
    time.sleep(5)
    automation.click_device_actions(0)
    automation.restart_cordatus()
    time.sleep(20)
    automation.close_browser()
