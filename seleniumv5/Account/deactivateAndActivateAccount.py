from functions import *

# Email işlemlerinden sonra test_login'i çalıştır.

# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.test_login()
    automation.navigate_to_settings()
    automation.scroll_down()
    automation.deactivate_account()
    automation.type_deactivate("DEACTIVATE")
    automation.click_ok()
    #automation.test_login()
    time.sleep(4)
    automation.close_browser()
