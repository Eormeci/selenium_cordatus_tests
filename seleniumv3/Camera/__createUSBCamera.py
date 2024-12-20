from functions import *

# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.login()
    automation.navigate_to_cameras()
    automation.click_add_new_camera_button()
    time.sleep(2)
    automation.select_physical()
    #automation.click_save_camera()

