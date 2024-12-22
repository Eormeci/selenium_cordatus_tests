from functions import *

# SADECE KOPYALIYOR , TERMINALDEN DENEMEN GEREKIYOR.

if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()
    automation.login()
    automation.navigate_to_devices()
    automation.device_connection_online()
    time.sleep(2)
    automation.click_device_actions(0)
    automation.connect_via_ssh()
    time.sleep(1)
    automation.close_browser()
