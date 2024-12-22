from functions import *


# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.login()
    automation.navigate_to_cameras()
    automation.click_add_new_camera_button()
    automation.fill_camera_source_url("http://85.93.233.159:8080/mjpg/video.mjpg")
    automation.attach_to_device()
    automation.open_device_dropdown()
    automation.select_device_option("NVIDIA Jetson Orin NX (16GB ram)")
    automation.add_camera_label("Deneme IP Kamera Device Attached")
    time.sleep(2)
    automation.click_save_camera()

