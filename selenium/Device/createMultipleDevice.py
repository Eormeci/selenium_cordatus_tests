from functions import *

# Kod yazılırken lisans ile sadece 1 device ekleniyordu dolayısıyla sadece lisanssız yazıldı.

# Ana calisma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.login()
    automation.navigate_to_devices()
    automation.add_new_device()
    automation.add_multiple_devices("test2",2)
    time.sleep(3)
    automation.close_browser()
