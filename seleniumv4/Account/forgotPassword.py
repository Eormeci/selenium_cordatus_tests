from functions import *

# Email işlemlerinden sonra test_login'i çalıştır.

# Ana çalışma
if __name__ == "__main__":
    automation = DeviceAutomation()
    automation.open_login_page()
    automation.driver.maximize_window()  # Tarayıcıyı tam ekranda aç
    automation.forgot_password()
    automation.enter_email()
    automation.reset_password_button()
    time.sleep(4)
    automation.close_browser()
