from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
import pyperclip
import os
import time


class DeviceAutomation:
    def __init__(self):
        # .env dosyasini yukle
        load_dotenv()
        
        # Ortam degiskenlerinden email ve sifreyi al
        self.EMAIL = os.getenv("USER_EMAIL")
        self.PASSWORD = os.getenv("USER_PASSWORD")
        
        # Geckodriver yolu
        self.GECKODRIVER_PATH = "/usr/local/bin/geckodriver"
        
        # Firefox tarayici ayarlari
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.headless = False
        
        # Geckodriver servisi kullanarak Firefox'u baslat
        service = Service(executable_path=self.GECKODRIVER_PATH)
        self.driver = webdriver.Firefox(service=service, options=firefox_options)
        
        # WebDriverWait
        self.wait = WebDriverWait(self.driver, 10)

    def open_login_page(self):
        LOGIN_URL = "https://app.cordata.ai/#/dashboard"
        self.driver.get(LOGIN_URL)
        time.sleep(3)

    def login(self):
        email_input_field = self.driver.find_element(By.ID, "user-email")
        password_input_field = self.driver.find_element(By.ID, "user-password")
        
        email_input_field.send_keys(self.EMAIL)
        password_input_field.send_keys(self.PASSWORD)
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button.float-right.white--text.lato-bold.v-btn.primary")
        login_button.click()
        print("Giris butonuna basariyla tiklandi.")
        time.sleep(5)

    # NAVIGATE => SOL TARAFTAKI MENU

    def navigate_to_devices(self):
        # Devices bağlantısını seçmek için doğru XPath
        devices_button = self.driver.find_element(
            By.XPATH, '//a[@href="#/control-panel/devices" and contains(@class, "v-list-item")]'
        )
        devices_button.click()
        print("Devices bağlantısına başarıyla tıklandı.")
        time.sleep(3)

    def navigate_to_cameras(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            # Camera menüsü butonunu bulmak için güncellenmiş XPath
            camera_menu_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//i[@class="v-icon notranslate v-icon--left mdi mdi-camera theme--light"]')
            ))
            camera_menu_button.click()
            print("Camera menüsüne başarıyla gidildi.")
            time.sleep(3)
        except Exception as e:
            print(f"Camera menüsüne gidilirken hata oluştu: {str(e)}")

    def navigate_to_AIWorkflow(self):
            """
            AI Workflow sayfasına gitmek için Beyin ikonuna tıklar.
            """
            try:
                print("AI Workflow sayfasına yönlendirme başlatılıyor...")
                brain_icon = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "i.v-icon.notranslate.mdi.mdi-brain.theme--light"))
                )
                brain_icon.click()
                print("Beyin ikonuna tıklandı.")
            except Exception as e:
                print(f"Bir hata oluştu: {e}")

    def navigate_to_applications(self):
        """
        "Applications" sayfasına doğrudan gider.
        """
        print("Applications sayfasına gidiliyor...")
        self.driver.get("https://app.cordata.ai/#/applications")

    # DEVICE FONKSIYONLARI
    def add_new_device(self):
        """
        Device sekmesindeki + new device butonu.
        """
        new_device_button = self.driver.find_element(
            By.XPATH, '//*[@id="devicesTable"]/div[1]/div/div[3]/div/div[2]/button')
        new_device_button.click()
        print("Yeni cihaz butonuna basariyla tiklandi.")
        time.sleep(3)

    def attach_to_device(self):
        """
        Device'a attach ederken kullanılan fonksiyon .
        """
        try:
            # WebDriverWait nesnesi oluşturulur
            wait = WebDriverWait(self.driver, 10)

            # "Attach To" alanını içeren div elemanını bul ve tıkla
            attach_to_div = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__text.mt-4 > form > div > div:nth-child(3) > div > div.v-input__control > div")
            ))
            attach_to_div.click()
            print("Attach To dropdown menüsüne tıklandı.")

            # "Device" seçeneğini seç
            device_option = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.v-list-item__title")
            ))

            for option in device_option:
                if option.text.strip() == "Device":
                    option.click()
                    print("Device seçeneği seçildi.")
                    break

        except Exception as e:
            print(f"Attach To işlemi sırasında hata oluştu: {str(e)}")

    def add_single_device(self):
        """
        Device eklerken single/multiple kısmındaki fonksiyon.
        """
        add_single_device_button = self.driver.find_element(
            By.CSS_SELECTOR, ".v-btn.v-btn--block.v-btn--is-elevated.v-btn--has-bg.theme--light.elevation-2.v-size--x-large")
        add_single_device_button.click()
        print("Tek cihaz ekleme butonuna basariyla tiklandi.")
        time.sleep(2)
        
    def add_multiple_devices(self, group_label, device_quantity):
        """
        Birden fazla cihaz eklemek için gerekli alanları doldurur ve işlemi tamamlar.
        """
        try:
            # Add Multiple Devices Button
            add_multiple_devices_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[span[text()='Add Multiple Devices']]")
            ))
            self.driver.execute_script("arguments[0].click();", add_multiple_devices_button)
            print("Add Multiple Devices butonuna başarıyla tıklandı.")

            # Label of the Devices (Group Name)
            label_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//label[contains(text(), 'Label of the devices')]/following-sibling::input")
            ))
            label_input.clear()
            label_input.send_keys(group_label)
            print("Cihaz etiketleri başarıyla girildi.")

            # Quantity of the Devices
            quantity_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//label[contains(text(), 'Quantity of the devices')]/following-sibling::input")
            ))
            quantity_input.clear()
            quantity_input.send_keys(str(device_quantity))
            print("Cihaz sayısı başarıyla girildi.")

            # Check the checkbox to true
            checkbox = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//input[@role='checkbox' and @aria-checked='false']")
            ))
            self.driver.execute_script("arguments[0].click();", checkbox)
            print("Checkbox başarıyla işaretlendi.")

            # Save Without Licence Button
            save_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'v-btn') and .//span[contains(text(), 'Save Device Without Licence')]]")
            ))
            self.driver.execute_script("arguments[0].click();", save_button)
            print("Save Device Without Licence butonuna başarıyla tıklandı.")

        
        except Exception as e:
            print(f"Cihazlar eklenirken hata oluştu: {str(e)}")

    def enter_device_name(self):
        """
        Device adı giren fonksiyon..
        """
        device_name_input_field = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//label[text()="Device Name"]/following-sibling::input')))
        device_name_input_field.send_keys("test123")
        print("Cihaz ismi basariyla girildi.")
        time.sleep(3)

    def click_licence_checkbox(self):
        """
        Lisansı onaylayan checkbox'a tıklayan fonksiyon.
        """
        checkbox_element = self.driver.find_element(
            By.CSS_SELECTOR,
            "#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__text.pb-0 > form > div > div.pt-0.mt-0.mb-0.pb-0.col.col-12 > div > div > div.v-data-table__wrapper > table > tbody > tr > td.text-start > div > div > div")
        self.driver.execute_script("arguments[0].click();", checkbox_element)
        print("Ana checkbox'a tıklandı.")
    
    def click_port_checkbox(self):
        """
        Device eklerken ilk portu seçen fonksiyon.
        """
        port = self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, "#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__text.pb-0 > form > div > div:nth-child(3) > div > div.v-data-table__wrapper > table > tbody > tr:nth-child(1) > td.text-start > div > div > div")))
        port.click()
        print("Port checkbox'a başarıyla tıklandı.")

    def save_device(self):
        """
        Device eklemeyi tamamlayan fonksiyon.
        """
        save_button = self.wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(@class, 'v-btn') and .//span[text()=' Save Device ']]")))
        save_button.click()
        print("Save Device butonuna başarıyla tıklandı.")
        time.sleep(3)

    def copy_and_save_token(self):
        """
        Eklenen cihazın tokenini kaydedip txt'e yazan fonksiyon.
        """
        copy_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.v-btn.blue.darken-2")))
        copy_button.click()
        print("Copy butonuna tıklandı.")
        time.sleep(1)

        copied_key = pyperclip.paste()
        print("Kopyalanan Key:", copied_key)

        with open("copied_key.txt", "w") as file:
            file.write(copied_key)
            print("Key başarıyla 'copied_key.txt' dosyasına yazıldı.")

    def click_device_actions(self, index=1): 
        """
        Device sekmesindeki sağdaki 3 noktaya basan fonksiyon . 2 tane üstünde test edildiği için 2.'ye basar.
        """ 
        buttons = self.driver.find_elements(By.CSS_SELECTOR, ".v-icon.notranslate.mdi.mdi-dots-horizontal-circle-outline.theme--light")
        if index < len(buttons):
            self.driver.execute_script("arguments[0].click();", buttons[index])
            print(f"{index + 1}. butona başarıyla tıklandı.")
        else:
            print(f"Uyarı: {index + 1}. buton bulunamadı. Mevcut buton sayısı: {len(buttons)}")

    def remove_device(self):
        """
        Remove butonuna basar (çöp kutusuna).
        """
        try:
            remove_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".v-list-item--link .mdi-delete-outline")))
            self.driver.execute_script("arguments[0].click();", remove_button)
            print("Remove butonuna başarıyla tıklandı.")
        except Exception as e:
            print(f"Remove butonu bulunamadı: {str(e)}")

    def continue_action(self):
        """
        Continue butonuna basar.
        """
        try:
            continue_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.v-btn.v-btn--is-elevated.v-btn--has-bg.theme--light.v-size--default.red")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)  # Butonu görünür alana getir
            self.driver.execute_script("arguments[0].click();", continue_button)  # Click kullan
            print("Continue butonuna başarıyla tıklandı.")
        except Exception as e:
            print(f"Continue butonuna tıklanırken hata oluştu: {str(e)}")

    def enter_delete_text(self):
        """
        Text field'a DELETE yazar.
        """
        try:
            delete_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//div[@class="v-text-field__slot"]//input[contains(@placeholder, "Enter")]')))
            delete_input.send_keys("DELETE")
            print("DELETE yazısı başarıyla girildi.")
        except Exception as e:
            print(f"DELETE yazısı girilirken hata oluştu: {str(e)}")

    def click_delete_button(self):
        """
        DELETE yazdıktan sonra tuşa basar.
        """
        try:
            delete_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.v-btn.red--text .v-btn__content")))
            self.driver.execute_script("arguments[0].click();", delete_button)
            print("DELETE butonuna başarıyla tıklandı.")
        except Exception as e:
            print(f"DELETE butonuna tıklanırken hata oluştu: {str(e)}")    

    def see_device_metrics(self):
        """
        Cihaz metriklerini görüntülemek için ilgili ikona tıklar.
        """
        try:
            metrics_icon = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "i.v-icon.notranslate.mdi.mdi-chart-box-outline.theme--light")
            ))
            self.driver.execute_script("arguments[0].click();", metrics_icon)
            print("Cihaz metrik ikonuna başarıyla tıklandı.")
        except Exception as e:
            print(f"Cihaz metrik ikonuna tıklanırken hata oluştu: {str(e)}")
    
    def stop_jtop_service(self):
        """
        Stop Jtop Service butonuna tıklar.
        """
        try:
            stop_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.mt-4.v-btn.v-btn--is-elevated.v-btn--has-bg.theme--dark.v-size--default.red")
            ))
            self.driver.execute_script("arguments[0].click();", stop_button)
            print("Stop Jtop Service butonuna başarıyla tıklandı.")
        except Exception as e:
            print(f"Stop Jtop Service butonuna tıklanırken hata oluştu: {str(e)}")

    def start_jtop_service(self):
        """
        Start Jtop butonuna tıklar.
        """
        try:
            start_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.v-btn.v-btn--is-elevated.v-btn--has-bg.theme--light.v-size--default.primary")
            ))
            self.driver.execute_script("arguments[0].click();", start_button)
            print("Start Jtop butonuna başarıyla tıklandı.")
        except Exception as e:
            print(f"Start Jtop butonuna tıklanırken hata oluştu: {str(e)}")

    def device_connection_online(self):
        """
        Device'ı Online durumuna geçiren butona tıklar.
        """
        try:
            online_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.v-btn.v-btn--text.theme--light.v-size--small.success--text")
            ))
            self.driver.execute_script("arguments[0].click();", online_button)
            print("Online butonuna başarıyla tıklandı.")
        except Exception as e:
            print(f"Online butonuna tıklanırken hata oluştu: {str(e)}")

    def device_connection_offline(self):
        """
        Device'ı Offline durumuna geçiren butona tıklar.
        """
        try:
            offline_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.v-btn.v-btn--outlined.theme--light.v-size--small.green--text.ma-2.overline.elevation-1")
            ))
            self.driver.execute_script("arguments[0].click();", offline_button)
            print("Offline butonuna başarıyla tıklandı.")
        except Exception as e:
            print(f"Offline butonuna tıklanırken hata oluştu: {str(e)}")

    def create_device_group_parent(self, group_name, group_description):

        """
        Yeni bir cihaz grubu oluşturmak için ilgili alanları doldurur ve işlemi tamamlar.
        """
        try:
            # Add Group Button
            add_group_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "i.v-icon.notranslate.mdi.mdi-plus.theme--light")
            ))
            self.driver.execute_script("arguments[0].click();", add_group_button)
            print("Cihaz grubu oluşturma butonuna başarıyla tıklandı.")

            # Group Name Input
            group_name_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//label[contains(text(), 'Group Name')]/following-sibling::input")
            ))
            group_name_input.clear()
            group_name_input.send_keys(group_name)
            print("Grup ismi başarıyla girildi.")

            # Group Description Input
            group_description_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//label[contains(text(), 'Group Description')]/following-sibling::input")
            ))
            group_description_input.clear()
            group_description_input.send_keys(group_description)
            print("Grup açıklaması başarıyla girildi.")

            # Save Button
            save_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.v-btn.v-btn--is-elevated.v-btn--has-bg.theme--light.v-size--default.primary.accent-1")
            ))
            self.driver.execute_script("arguments[0].click();", save_button)
            print("Save butonuna başarıyla tıklandı.")
            
            
        except Exception as e:
            print(f"Cihaz grubu oluşturulurken hata oluştu: {str(e)}")


        """
        İstenen tab'a tıklar.
        """
        try:
            # WebDriverWait nesnesi oluşturulur
            wait = WebDriverWait(self.driver, 10)

            # İstenen tab'i seç
            tab_option = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.v-list-item__title")
            ))

            for option in tab_option:
                if option.text.strip() == tab_name:
                    option.click()
                    print(f"'{tab_name}' tab'ı başarıyla seçildi.")
                    break

        except Exception as e:
            print(f"Tab seçimi sırasında hata oluştu: {str(e)}")            

    def create_device_group_child(self, group_name, group_description, device_name):
        """
        Yeni bir cihaz grubu oluşturur, cihaz dropdown menüsünü açar ve belirtilen cihazı seçer.
        """
        try:
            # Add Group Button
            add_group_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "i.v-icon.notranslate.mdi.mdi-plus.theme--light")
            ))
            self.driver.execute_script("arguments[0].click();", add_group_button)
            print("Cihaz grubu oluşturma butonuna başarıyla tıklandı.")

            # Group Name Input
            group_name_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//label[contains(text(), 'Group Name')]/following-sibling::input")
            ))
            group_name_input.clear()
            group_name_input.send_keys(group_name)
            print("Grup ismi başarıyla girildi.")

            # Group Description Input
            group_description_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//label[contains(text(), 'Group Description')]/following-sibling::input")
            ))
            group_description_input.clear()
            group_description_input.send_keys(group_description)
            print("Grup açıklaması başarıyla girildi.")
            time.sleep(2)

            # Device Dropdown
            device_dropdown = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__text > form > div:nth-child(6) > div > div.v-input__slot > div.v-select__slot")
            ))
            self.driver.execute_script("arguments[0].click();", device_dropdown)
            print("Device dropdown menüsüne başarıyla tıklandı.")
            time.sleep(2)

            # Select Device Option
            device_options = self.wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.v-list-item__title")
            ))

            for option in device_options:
                if option.text.strip() == device_name:
                    self.driver.execute_script("arguments[0].click();", option)
                    print(f"'{device_name}' cihazı başarıyla seçildi.")
                    break

            time.sleep(2)        

                        
            # Save Button
            save_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.v-btn.v-btn--is-elevated.v-btn--has-bg.theme--light.v-size--default.primary.accent-1")
            ))
            self.driver.execute_script("arguments[0].click();", save_button)
            print("Save butonuna başarıyla tıklandı.")

        except Exception as e:
            print(f"İşlem sırasında hata oluştu: {str(e)}")

    def refresh_device(self):
        """
        Cihaz listesini yenilemek için refresh butonuna tıklar.
        """
        try:
            refresh_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#devicesTable > div.v-card__title.mx-0.px-0.mt-0.pt-0 > div > div.d-flex.align-center.col.col-auto > button > span > i")
            ))
            self.driver.execute_script("arguments[0].click();", refresh_button)
            print("Cihaz listesi başarıyla yenilendi.")
        except Exception as e:
            print(f"Cihaz yenileme sırasında hata oluştu: {str(e)}")

    def download_logs(self):
        """
        Download Logs butonuna tıklar ve logların indirilmesini başlatır.
        """
        try:
            # Locate the Download Logs button
            download_logs_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='menuitem' and .//div[contains(@class, 'v-list-item__title') and text()='Download Logs']]")
            ))
            self.driver.execute_script("arguments[0].click();", download_logs_button)
            print("Download Logs butonuna başarıyla tıklandı.")
        
        except Exception as e:
            print(f"Download Logs işleminde bir hata oluştu: {str(e)}")

    def restart_cordatus(self):
        """
        Restart Cordatus işlemini başlatır ve onay için Restart butonuna tıklar.
        """
        try:
            # Locate the Restart Cordatus menu item
            restart_menu_item = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='menuitem' and .//div[contains(@class, 'v-list-item__title') and text()='Restart Cordatus']]")
            ))
            self.driver.execute_script("arguments[0].click();", restart_menu_item)
            print("Restart Cordatus menü öğesine başarıyla tıklandı.")

            # Locate and click the Restart button in the confirmation dialog
            restart_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'v-btn') and .//span[text()='Restart']]")
            ))
            self.driver.execute_script("arguments[0].click();", restart_button)
            print("Restart onay butonuna başarıyla tıklandı.")
        
        except Exception as e:
            print(f"Restart Cordatus işleminde bir hata oluştu: {str(e)}")

    def connect_via_ssh(self, output_file="ssh_command.txt"):
        """
        Connect via SSH seçeneğine tıklar ve açılan sayfadan SSH komutunu alıp bir dosyaya kaydeder.
        
        Args:
            output_file (str): SSH komutunun kaydedileceği dosya adı.
        """
        try:
            # Locate the Connect via SSH menu item
            ssh_menu_item = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='menuitem' and .//div[contains(@class, 'v-list-item__title') and text()='Connect via SSH']]")
            ))
            self.driver.execute_script("arguments[0].click();", ssh_menu_item)
            print("Connect via SSH menü öğesine başarıyla tıklandı.")

            # Wait for the SSH command input field to appear
            ssh_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//input[@id='ssh-command' and @readonly='readonly']")
            ))

            # Get the SSH command text
            ssh_command = ssh_input.get_attribute("value")
            print(f"SSH komutu başarıyla alındı: {ssh_command}")

            # Save the SSH command to a text file
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(ssh_command)
            print(f"SSH komutu {output_file} dosyasına başarıyla kaydedildi.")
        
        except Exception as e:
            print(f"Connect via SSH işleminde bir hata oluştu: {str(e)}")

    def edit_groups(self):
        """
        Grup düzenleme ikonuna tıklar.
        """
        try:
            # Edit Group Button
            edit_group_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "i.v-icon.notranslate.mdi.mdi-pencil.theme--light")
            ))
            self.driver.execute_script("arguments[0].click();", edit_group_button)
            print("Grup düzenleme ikonuna başarıyla tıklandı.")

        except Exception as e:
            print(f"Grup düzenleme işleminde hata oluştu: {str(e)}")

    def click_parent(self, index=2):
        """
        Parent butonuna tıklar.
        :param index: Kaçıncı parent butonuna tıklanacağını belirtir (varsayılan: 2).
        """
        try:
            # Parent Buttons
            parent_buttons = self.wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".he-tree .tree-node > .tree-node-children > .tree-node > .tree-node-inner-back > .tree-node-inner > div > button")
            ))

            if index <= len(parent_buttons):
                parent_button = parent_buttons[index - 1]
                self.driver.execute_script("arguments[0].click();", parent_button)
                print(f"Parent butonuna başarıyla tıklandı. Index: {index}")
            else:
                print(f"Belirtilen index ({index}) mevcut değil. Toplam buton sayısı: {len(parent_buttons)}")

        except Exception as e:
            print(f"Parent butonuna tıklarken hata oluştu: {str(e)}")

    def drag_and_drop(self):
        """
        Belirtilen elementi sürükleyip hedef alana bırakır.
        """
        try:
            # Kaynak (drag edilen öğe)
            source_element = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#devicesTable > div.v-card__text.mb-0.pb-0.mx-0.px-0 > div > div.v-data-table__wrapper > table > tbody > tr:nth-child(1) > td:nth-child(2)")
            ))

            # Hedef (bırakılacak alan)
            target_element = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#app > div.v-application--wrap > div:nth-child(2) > main > div > div > div.row.row--dense > div.col-xl-8.col-12 > div > div.pl-1.col.col-6 > div > div.v-card__text.justify-center.d-flex > div > div.v-data-table__wrapper > table > tbody > th > h3")
            ))

            # Drag and Drop işlemi
            actions = ActionChains(self.driver)
            actions.drag_and_drop(source_element, target_element).perform()

            print("Element başarıyla sürüklenip hedefe bırakıldı.")

        except Exception as e:
            print(f"Drag and drop işlemi sırasında hata oluştu: {str(e)}")

    def save_device_to_group(self):
        """
        Save Group butonuna ve ardından onay için OK butonuna basar.
        """
        try:
            # Save Group Button
            save_group_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.v-btn.v-btn--is-elevated.v-btn--has-bg.theme--light.v-size--default.primary.darken-2")
            ))
            self.driver.execute_script("arguments[0].click();", save_group_button)
            print("Save Group butonuna başarıyla tıklandı.")

            time.sleep(3)
            # OK Button
            ok_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled")
            ))
            self.driver.execute_script("arguments[0].click();", ok_button)
            print("OK butonuna başarıyla tıklandı.")

        except Exception as e:
            print(f"Save device to group işlemi sırasında hata oluştu: {str(e)}")

    # CAMERA FONKSIYONLARI
    
    def rename_camera(self, new_name):
        """
        Kameranın ismini değiştiren fonksiyon.
        """
        try:
            # WebDriverWait nesnesi oluşturulur
            wait = WebDriverWait(self.driver, 10)

            # Ayarlar menüsüne bas
            settings_button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "i.mdi-dots-horizontal-circle-outline")
            ))
            self.driver.execute_script("arguments[0].click();", settings_button)
            print("Ayarlar menüsüne tıklandı.")
            time.sleep(1)

            # Edit tuşuna bas
            edit_button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "i.mdi-circle-edit-outline")
            ))
            self.driver.execute_script("arguments[0].click();", edit_button)
            print("Edit tuşuna tıklandı.")
            time.sleep(1)

            # Yeni ismi yaz
            name_input = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.v-text-field__slot > input")
            ))
            name_input.clear()
            name_input.send_keys(new_name)
            print(f"Yeni isim yazıldı: {new_name}")
            time.sleep(1)

            # Save Changes butonuna bas
            save_button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.v-btn.primary")
            ))
            self.driver.execute_script("arguments[0].click();", save_button)
            print("Save Changes butonuna tıklandı.")
            time.sleep(1)

            # OK tuşuna bas
            ok_button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.swal2-confirm")
            ))
            self.driver.execute_script("arguments[0].click();", ok_button)
            print("OK tuşuna tıklandı.")
            time.sleep(1)

        except Exception as e:
            print(f"Bir hata oluştu: {str(e)}")

    def change_res(self):
        """
        Webcam'i bulup tıklama işlemi gerçekleştiren fonksiyon.
        """
        try:
            # WebDriverWait nesnesi oluşturulur
            wait = WebDriverWait(self.driver, 10)

            # Webcam'i arayıp bul
            webcam_row = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//td[@class='text-left']//span[text()=' webcam ']/ancestor::tr")
            ))
            self.driver.execute_script("arguments[0].click();", webcam_row)
            print("Webcam'e tıklandı.")

            # 10 saniye bekle
            time.sleep(10)

        except Exception as e:
            print(f"Bir hata oluştu: {str(e)}")

    def click_add_new_camera_button(self):
        """
        Cameras sekmesinde (+) butonuna basar. İndex eklenmediği taktirde group'a basıyor.
        Aynı css.
        """
        try:
            # WebDriverWait nesnesi oluşturulur
            wait = WebDriverWait(self.driver, 10)

            # Tüm "Yeni Kamera Ekle" butonlarını bul
            add_camera_buttons = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".v-btn.v-btn--fab.v-btn--outlined.v-btn--round.theme--light.v-size--x-small.primary--text.text--darken-2[style='width: 1.5vw; height: 1.5vw;']")
            ))

            # İkinci butona tıkla
            if len(add_camera_buttons) > 1:
                add_camera_buttons[1].click()
                print("Yeni kamera ekleme butonuna tıklandı.")
            else:
                print("Yeterli sayıda buton bulunamadı.")

        except Exception as e:
            print(f"Yeni kamera ekleme butonuna tıklama sırasında hata oluştu: {str(e)}")

    def fill_camera_source_url(self, temp_url):
        """
        Camera URL'si.
        """
        try:
            # WebDriverWait nesnesi oluşturulur
            wait = WebDriverWait(self.driver, 10)

            # "Camera Source URL" alanını içeren div elemanını bul
            camera_source_divs = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.v-text-field__slot label")
            ))

            # "Camera Source URL" label'ına sahip div'in input alanını bul ve yaz
            for div in camera_source_divs:
                if "Camera Source URL" in div.text:
                    input_element = div.find_element(By.XPATH, "./following-sibling::input")
                    input_element.send_keys(temp_url)
                    print(f"URL '{temp_url}' alana yazıldı.")
                    break
            else:
                print("Camera Source URL alanı bulunamadı.")

            time.sleep(2)  # İşlemin tamamlanması için kısa bir bekleme

        except Exception as e:
            print(f"Kamera URL alanını doldurma sırasında hata oluştu: {str(e)}")

    def add_camera_label(self, label):
        """
        Camera label yazar . Parametre alır.
        """
        try:
            # WebDriverWait nesnesi oluşturulur
            wait = WebDriverWait(self.driver, 10)

            # "Camera Label" alanını içeren div elemanını bul
            camera_label_divs = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.v-text-field__slot label")
            ))

            # "Camera Label" label'ına sahip div'in input alanını bul ve yaz
            for div in camera_label_divs:
                if "Camera Label" in div.text:
                    input_element = div.find_element(By.XPATH, "./following-sibling::input")
                    input_element.send_keys(label)
                    print(f"Label '{label}' alana yazıldı.")
                    break
            else:
                print("Camera Label alanı bulunamadı.")

            time.sleep(2)  # İşlemin tamamlanması için kısa bir bekleme

        except Exception as e:
            print(f"Kamera Label alanını doldurma sırasında hata oluştu: {str(e)}")

    def click_save_camera(self):
        """
        Save.
        """
        try:
            # WebDriverWait nesnesi oluşturulur
            wait = WebDriverWait(self.driver, 10)

            # "Save" butonunu bul ve tıkla
            save_button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.white--text.v-btn.v-btn--outlined.theme--light.v-size--default.primary--text.text--accent-1")
            ))
            save_button.click()
            print("Save butonuna tıklandı.")

        except Exception as e:
            print(f"Save butonuna tıklama sırasında hata oluştu: {str(e)}")

    def open_device_dropdown(self):
        """
        Device dropdown açar. Camerayı device'a eşlemek için kullanılır.
        """
        try:
            # WebDriverWait nesnesi oluşturulur
            wait = WebDriverWait(self.driver, 10)

            # "Device" dropdown menüsünü bul ve tıkla
            device_dropdown = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__text.mt-4 > form > div > div:nth-child(4) > div > div > div")
            ))
            device_dropdown.click()
            print("Device dropdown menüsüne tıklandı.")

        except Exception as e:
            print(f"Device dropdown menüsü açılırken hata oluştu: {str(e)}")

    def select_physical(self):
        """
        "Physical" seçeneğini seçmek için kullanılan fonksiyon.
        """
        try:
            # WebDriverWait nesnesi oluşturulur
            wait = WebDriverWait(self.driver, 10)

            # Dropdown alanını içeren div elemanını bul ve tıkla
            dropdown_div = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__text.mt-4 > form > div > div:nth-child(1) > div > div.v-input__control > div")
            ))
            self.driver.execute_script("arguments[0].click();", dropdown_div)
            print("Dropdown menüsüne tıklandı.")

            # Menü seçeneklerini içeren elemanları bul
            menu_options = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.v-list-item__title")
            ))
            time.sleep(3)

            # İlk seçeneği seç
            if len(menu_options) > 0:
                self.driver.execute_script("arguments[0].click();", menu_options[0])
                print("İlk seçenek başarıyla seçildi.")
            else:
                print("Yeterli seçenek bulunamadı.")
                
            time.sleep(3)
        except Exception as e:
            print(f"Bir hata oluştu: {str(e)}")

    def select_device_option(self, device_name):
            """
            Cihazımızı seçiyoruz . Nvidia Origin gibi . Parametre alır !
            """
            try:
                # WebDriverWait nesnesi oluşturulur
                wait = WebDriverWait(self.driver, 10)

                # Belirtilen cihazı seç
                device_option = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.v-list-item__title")
                ))

                for option in device_option:
                    if option.text.strip() == device_name:
                        option.click()
                        print(f"'{device_name}' cihazı seçildi.")
                        break

            except Exception as e:
                print(f"Device seçimi sırasında hata oluştu: {str(e)}")        

    def close_browser(self):
        """
        Browser'ı kapatır.
        """
        print("Tarayici kapatiliyor...")
        self.driver.quit()

    # MODEL FONKSIYONLARI 
    def upload_model(self, model_name):
        """
        Bir modeli yükler.

        Args:
            model_name (str): Yüklenmek istenen modelin adı.
        """
        try:
            print("Model yükleme işlemi başlatılıyor...")
           
            # 2. Adım: 'Add Model' butonuna tıklama
            add_model_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.v-btn.v-btn--has-bg.theme--dark.v-size--default.purple.ml-0"))
            )
            add_model_button.click()
            print("'Add Model' butonuna tıklandı.")

            # 3. Adım: Model adını girme
            model_label_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[required][type='text']"))
            )
            model_label_input.send_keys(model_name)
            print(f"Model adı '{model_name}' olarak girildi.")

            # 4. Adım: TAO Toolkit'i seçme
            train_source_dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div.v-dialog__content.v-dialog__content--active > div > div > div > div > div:nth-child(3) > div > div.v-input.align-center.mb-6.v-input--hide-details.v-input--dense.theme--light.v-text-field.v-text-field--is-booted.v-text-field--enclosed.v-text-field--outlined.v-select > div > div"))
            )
            self.driver.execute_script("arguments[0].click();", train_source_dropdown)
            print("'Train Source' açılır menüsüne tıklandı.")

            # TAO Toolkit seçeneğini bul ve tıkla
            tao_toolkit_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='option' and span[contains(text(),'TAO Toolkit')]]"))
            )
            self.driver.execute_script("arguments[0].click();", tao_toolkit_tab)
            print("'TAO Toolkit' seçildi.")

            # 5. Adım :Nvidia Model adını yazma
            model_key_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.v-input__control input[name='model_key']"))
            )
            model_key_input.click()
            model_key_input.send_keys("nvidia_model")
            print("'Model Key' yazıldı.")

            print("Model yükleme işlemi tamamlandı.")

        except Exception as e:
            print(f"Bir hata oluştu: {e}")

    def select_channel_order(self):
        """
        Dropdown menüsünden 'NCHW' seçeneğini seçer.
        """
        try:
            print("Channel Order dropdown işlemi başlatılıyor...")

            # Dropdown menüsünü aç
            dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div.v-dialog__content.v-dialog__content--active > div > div > div > div > form > div:nth-child(1) > div:nth-child(2) > div > div > div.v-input__slot"))
            )
            self.driver.execute_script("arguments[0].click();", dropdown)
            print("Dropdown menüsü açıldı.")

            # 'NCHW' seçeneğini bul ve tıkla
            nchw_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='option' and .//div[@class='v-list-item__title' and text()='NCHW']]"))
            )
            self.driver.execute_script("arguments[0].click();", nchw_option)
            print("'NCHW' seçildi.")

        except Exception as e:
            print(f"Bir hata oluştu: {e}")

    def set_channel_dimensions(self, width, height):
        """
        Channel Width ve Channel Height alanlarına verilen değerleri girer.

        Args:
            width (str): Channel Width için girilecek değer.
            height (str): Channel Height için girilecek değer.
        """
        try:
            print("Channel Width ve Channel Height değerleri giriliyor...")

            # Channel Width input elementini bul ve değerini ayarla
            width_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.v-text-field__slot input[name='width']"))
            )
            width_input.click()
            width_input.send_keys(Keys.CONTROL + "a")  # Tüm metni seç
            width_input.send_keys(Keys.DELETE)  # Seçilen metni sil
            width_input.send_keys(width)
            print(f"Channel Width: {width} olarak ayarlandı.")

            # Channel Height input elementini bul ve değerini ayarla
            height_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.v-text-field__slot input[name='height']"))
            )
            height_input.click()
            height_input.send_keys(Keys.CONTROL + "a")  # Tüm metni seç
            height_input.send_keys(Keys.DELETE)  # Seçilen metni sil
            height_input.send_keys(height)
            print(f"Channel Height: {height} olarak ayarlandı.")

        except Exception as e:
            print(f"Bir hata oluştu: {e}")

    def upload_model_files(self):
        """
        Sabit bir dosya yolunu yükler.
        """
        try:
            print("Dosya yükleme işlemi başlatılıyor...")

            # Dosya yükleme input elementini bul
            file_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.v-input__slot input[type='file']"))
            )

            # Sabit dosya yolunu input elementine gönder
            file_path = "/home/openzeka/Desktop/files/files.zip"
            file_input.send_keys(file_path)
            print(f"Dosya başarıyla yüklendi: {file_path}")

        except Exception as e:
            print(f"Bir hata oluştu: {e}")

    def upload_label_file(self):
        """
        Sabit bir label dosyasını yükler.
        """
        try:
            print("Label dosyası yükleme işlemi başlatılıyor...")

            # Label dosyası input elementini bul
            label_file_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.v-input__slot input[accept='.txt']"))
            )

            # Sabit dosya yolunu input elementine gönder
            label_file_path = "/home/openzeka/Desktop/files/labels.txt"
            label_file_input.send_keys(label_file_path)
            print(f"Label dosyası başarıyla yüklendi: {label_file_path}")

        except Exception as e:
            print(f"Bir hata oluştu: {e}")

    def save_and_upload(self):
        """
        'Save and Upload' butonuna tıklar.
        """
        try:
            print("'Save and Upload' butonuna tıklama işlemi başlatılıyor...")

            # 'Save and Upload' butonunu bul ve tıkla
            save_upload_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'].v-btn--has-bg.success"))
            )
            self.driver.execute_script("arguments[0].click();", save_upload_button)
            print("'Save and Upload' butonuna başarıyla tıklandı.")

        except Exception as e:
            print(f"Bir hata oluştu: {e}")
    
    def create_pipeline(self):
        """
        Pipeline oluşturmak için gerekli adımları gerçekleştirir.
        """
        try:
            print("Pipeline oluşturma işlemi başlatılıyor...")

            # Pipeline sekmesine tıkla
            pipeline_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div.v-application--wrap > div:nth-child(2) > main > div > div > div.v-card.v-sheet.theme--light.elevation-0 > div.v-tabs.theme--light > div > div.v-slide-group__wrapper > div > div:nth-child(3)"))
            )
            self.driver.execute_script("arguments[0].click();", pipeline_tab)
            print("Pipeline sekmesine başarıyla tıklandı.")

            time.sleep(2)
            # New Pipeline butonuna tıkla
            new_pipeline_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#app > div.v-application--wrap > div:nth-child(2) > main > div > div > div.v-card.v-sheet.theme--light.elevation-0 > div.v-window.v-item-group.theme--light.v-tabs-items > div > div.v-window-item.v-window-item--active > div > div.elevation-0.v-card.v-sheet.theme--light > div.v-card__title.mt-0.pt-0 > div > div:nth-child(3) > div > div:nth-child(2) > button"))
            )
            self.driver.execute_script("arguments[0].click();", new_pipeline_button)
            print("New Pipeline butonuna başarıyla tıklandı.")

        except Exception as e:
            print(f"Bir hata oluştu: {e}")

    def drag_and_drop_pipeline(self):
        """
        PEOPLENET ve GENDERNET bileşenlerini sürükleyip bırakır.
        """
        try:
            print("Drag and Drop işlemi başlatılıyor...")

            # PEOPLENET butonunu bul
            print("PEOPLENET butonunu bulmaya çalışılıyor...")
            peoplenet_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[span[contains(text(),'PEOPLENET')]]"))
            )
            print("PEOPLENET butonu bulundu.")

            # Hedef alanı belirle (ekranın ortası)
            print("Hedef alanı bulmaya çalışılıyor...")
            target_area = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.target-drop-area"))
            )
            print("Hedef alan bulundu.")

            # PEOPLENET butonunu sürükle ve bırak
            print("PEOPLENET butonu sürükleniyor...")
            action = ActionChains(self.driver)
            action.click_and_hold(peoplenet_button).move_to_element(target_area).release().perform()
            print("PEOPLENET ekranın ortasına bırakıldı.")

            # GENDERNET butonunu bul
            print("GENDERNET butonunu bulmaya çalışılıyor...")
            gendernet_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[span[contains(text(),'GENDERNET')]]"))
            )
            print("GENDERNET butonu bulundu.")

            # GENDERNET'i ekranın biraz sağ tarafına bırak
            print("GENDERNET butonu sürükleniyor...")
            action.click_and_hold(gendernet_button).move_by_offset(150, 0).release().perform()
            print("GENDERNET ekranın sağ tarafına bırakıldı.")

        except Exception as e:
            print(f"Bir hata oluştu: {e}")

        finally:
            print("Drag and Drop işlemi tamamlandı.")

    def click_details(self):
        """
        "Details" butonuna tıklar.
        """
        print("Details butonuna tıklanıyor...")
        details_button = self.driver.find_element(By.CSS_SELECTOR, "a[href*='#/containers/details/100'].v-btn")
        details_button.click()

    def start_application(self):
        """
        'Start Application on Your Device' butonuna tıklar.
        """
        try:
            print("Uygulama başlatma işlemi başlatılıyor...")

            # Start Application butonunu bul ve tıkla
            start_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "start-on-your-device"))
            )
            self.driver.execute_script("arguments[0].click();", start_button)
            print("'Start Application on Your Device' butonuna başarıyla tıklandı.")

        except Exception as e:
            print(f"Bir hata oluştu: {e}")

    def click_checkbox(self):
        """
        Checkbox'a tıklar.
        """
        try:
            print("Checkbox tıklama işlemi başlatılıyor...")
            checkbox = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.v-input--selection-controls__ripple"))
            )
            self.driver.execute_script("arguments[0].click();", checkbox)
            print("Checkbox başarıyla tıklandı.")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")

    def click_continue(self):
        """
        'Continue' butonuna tıklar.
        """
        try:
            print("'Continue' butonuna tıklama işlemi başlatılıyor...")
            continue_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "first-step-continue"))
            )
            self.driver.execute_script("arguments[0].click();", continue_button)
            print("'Continue' butonuna başarıyla tıklandı.")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")

    def select_version(self):
        """
        'Select' butonuna tıklar.
        """
        try:
            print("'Select' butonuna tıklama işlemi başlatılıyor...")
            select_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.v-btn--outlined.theme--light.v-size--small.green--text.text--lighten-1"))
            )
            self.driver.execute_script("arguments[0].click();", select_button)
            print("'Select' butonuna başarıyla tıklandı.")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")

    def click_second_continue(self):
        """
        İkinci 'Continue' butonuna tıklar.
        """
        try:
            print("İkinci 'Continue' butonuna tıklama işlemi başlatılıyor...")
            second_continue_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='start-environment-dialog']/div/div/div[2]/div[2]/div/div/div[2]/button[2]"))
            )
            self.driver.execute_script("arguments[0].click();", second_continue_button)
            print("İkinci 'Continue' butonuna başarıyla tıklandı.")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")

    def tick_jupyter(self):
        """
        Jupyter seçeneğini işaretler.
        """
        try:
            print("Jupyter seçeneği işaretleniyor...")
            jupyter_tick = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "i.mdi-checkbox-blank-circle-outline"))
            )
            self.driver.execute_script("arguments[0].click();", jupyter_tick)
            print("Jupyter seçeneği başarıyla işaretlendi.")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")

    def set_env_name(self, name):
        """
        'Environment Name' alanına verilen ismi yazar.

        Args:
            name (str): Yazılacak çevre ismi.
        """
        try:
            print("Environment Name alanına isim yazılıyor...")
            env_name_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Environment Name (Optional)')]/following-sibling::input"))
            )
            env_name_input.click()
            env_name_input.clear()
            env_name_input.send_keys(name)
            print(f"Environment Name: '{name}' olarak ayarlandı.")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")

    def add_port(self, port_name, port_number):
        """
        Yeni bir port ekler.

        Args:
            port_name (str): Eklenmek istenen portun adı.
            port_number (str): Eklenmek istenen portun numarası.
        """
        try:
            print("Port ekleme işlemi başlatılıyor...")

            # Port ekleme butonuna tıkla
            add_port_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#start-environment-dialog > div > div > div.v-stepper__items > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(5) > div:nth-child(2) > div:nth-child(2) > div > div > div.v-alert__content > div > div > button"))
            )
            self.driver.execute_script("arguments[0].click();", add_port_button)
            print("Port ekleme butonuna başarıyla tıklandı.")

            # Port adı gir
            port_name_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#start-environment-dialog > div > div > div.v-stepper__items > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(5) > div:nth-child(2) > div:nth-child(2) > div > div > div.v-alert__content > div > div:nth-child(1) > div > div.mr-0.col.col-3 > div input"))
            )
            port_name_input.click()
            port_name_input.clear()
            port_name_input.send_keys(port_name)
            print(f"Port adı '{port_name}' olarak girildi.")

            # Port numarası gir
            port_number_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#start-environment-dialog > div > div > div.v-stepper__items > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(5) > div:nth-child(2) > div:nth-child(2) > div > div > div.v-alert__content > div > div:nth-child(1) > div > div.col.col-4 > div input"))
            )
            port_number_input.click()
            port_number_input.clear()
            port_number_input.send_keys(port_number)
            print(f"Port numarası '{port_number}' olarak girildi.")

            # Tik işaretine tıkla
            tick_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#start-environment-dialog > div > div > div.v-stepper__items > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(5) > div:nth-child(2) > div:nth-child(2) > div > div > div.v-alert__content > div > div:nth-child(1) > div > div.col.col-5 > div > div > div > div.v-input__slot > div > div"))
            )
            self.driver.execute_script("arguments[0].click();", tick_button)
            print("Tik işaretine başarıyla tıklandı.")

            # Kaydet butonuna tıkla
            save_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#start-environment-dialog > div > div > div.v-stepper__items > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(5) > div:nth-child(2) > div:nth-child(2) > div > div > div.v-alert__content > div > div.d-flex.justify-center.col.col-12 > button"))
            )
            self.driver.execute_script("arguments[0].click();", save_button)
            print("Port ekleme işlemi başarıyla tamamlandı.")

        except Exception as e:
            print(f"Bir hata oluştu: {e}")

    def start_env(self):
        """
        'Start Environment' butonuna tıklar.
        """
        try:
            print("'Start Environment' butonuna tıklama işlemi başlatılıyor...")
            start_env_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#start-environment-dialog > div > div > div.v-stepper__items > div:nth-child(3) > div > div:nth-child(2) > div > button.mt-3.v-btn.v-btn--is-elevated.v-btn--has-bg.theme--light.v-size--default.primary"))
            )
            self.driver.execute_script("arguments[0].click();", start_env_button)
            print("'Start Environment' butonuna başarıyla tıklandı.")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")
