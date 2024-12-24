from functions import *


# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.login()
    automation.navigate_to_devices()
    automation.device_connection_online()
    time.sleep(1)
    automation.navigate_to_jobs()
    automation.start_new_job()
    automation.select_trafficcamnet()
    automation.give_job_name("test")
    time.sleep(1)
    automation.click_camera_checkbox()
    time.sleep(1)
    automation.click_device_checkbox()
    time.sleep(1)
    automation.start_now()
    time.sleep(60)