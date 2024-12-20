from functions import *


# Ana calisma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.login()
    automation.navigate_to_devices()
    automation.click_device_actions(0)
    time.sleep(3)
    automation.download_logs()
    time.sleep(3)
    automation.close_browser()
