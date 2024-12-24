from functions import *


# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.login()
    automation.navigate_to_devices()
    automation.device_connection_online()
    time.sleep(3)
    automation.navigate_to_applications()
    time.sleep(3)
    automation.click_details()
    automation.start_application()
    automation.click_checkbox()
    automation.click_continue()
    time.sleep(1)
    automation.select_version()
    automation.click_second_continue()
    time.sleep(2)
    automation.set_env_name("test env")
    time.sleep(2)
    automation.tick_jupyter()
    time.sleep(2)
    automation.add_port(8080,"test port")
    time.sleep(5)
    automation.start_env()
    time.sleep(10)
    automation.close_browser()
