from functions import *


# Ana calisma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.login()
    automation.navigate_to_devices()
    automation.add_new_device()
    automation.add_single_device()
    automation.enter_device_name()
    automation.click_licence_checkbox()
    automation.click_port_checkbox()
    automation.save_device()
    automation.copy_and_save_token()
    automation.close_browser()
