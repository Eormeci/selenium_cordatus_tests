from functions import *

# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.login()
    automation.navigate_to_cameras()
    automation.click_add_new_camera_button()
    automation.camera_type_open_attach_dropdown()
    automation.select_physical_option()
    time.sleep(2)
    #automation.click_save_camera()

