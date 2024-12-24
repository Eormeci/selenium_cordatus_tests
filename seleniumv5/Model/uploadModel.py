from functions import *


# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.login()
    automation.navigate_to_AIWorkflow()
    automation.upload_model("test")
    time.sleep(2)
    automation.select_channel_order()
    time.sleep(2)
    automation.set_channel_dimensions(224,224)
    time.sleep(2)
    automation.upload_model_files()
    automation.upload_label_file()
    time.sleep(2)
    automation.save_and_upload()
    time.sleep(4)
    automation.close_browser()
