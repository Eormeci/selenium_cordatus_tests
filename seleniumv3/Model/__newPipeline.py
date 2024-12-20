from functions import *


# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.login()
    automation.navigate_to_AIWorkflow()
    automation.create_pipeline()
    time.sleep(5)
    automation.drag_and_drop_pipeline()
    automation.close_browser()
