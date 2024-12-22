from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
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

    def create_device_group_child(self, group_name, group_description):
        try:
            # Add Group Button
            add_group_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "i.v-icon.notranslate.mdi.mdi-plus.theme--light")
            ))
            add_group_button.click()
            print("Alt cihaz grubu oluşturma butonuna başarıyla tıklandı.")

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

            # Dropdown menüsünü açmak için farklı stratejiler
            try:
                # Önce üst elementi bulup içindeki ikonu seçin
                dropdown_container = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'v-input__slot')]//div[contains(@class, 'v-select__slot')]")
                ))
                
                # İkon için daha spesifik bir seçici kullanın
                dropdown_icon = dropdown_container.find_element(By.CSS_SELECTOR, "i.mdi-menu-down")
                
                # JavaScript ile tıklama
                self.driver.execute_script("arguments[0].click();", dropdown_icon)
                print("Dropdown menüsü başarıyla açıldı.")
            except Exception as dropdown_open_error:
                print(f"Dropdown açılırken hata oluştu: {str(dropdown_open_error)}")
                
                # Alternatif yöntem: JavaScript ile doğrudan tıklama
                try:
                    self.driver.execute_script("""
                        var dropdownIcon = document.querySelector('div.v-input__icon.v-input__icon--append i.mdi-menu-down');
                        if (dropdownIcon) dropdownIcon.click();
                    """)
                    print("JavaScript ile dropdown menüsü açıldı.")
                except Exception as js_error:
                    print(f"JavaScript ile dropdown açılamadı: {str(js_error)}")

            # İlk seçeneği seçme
            time.sleep(1)  # Dropdown açılması için kısa bir bekleme
            first_option = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='listbox']//div[contains(@class, 'v-list-item')][1]")
            ))
            first_option.click()
            print("Dropdown menüden ilk seçenek başarıyla seçildi.")

            # Save Button
            save_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.v-btn.v-btn--is-elevated.v-btn--has-bg.theme--light.v-size--default.primary.accent-1")
            ))
            save_button.click()
            print("Save butonuna başarıyla tıklandı.")

        except Exception as e:
            print(f"Alt cihaz grubu oluşturulurken hata oluştu: {str(e)}")
            # Hata durumunda ekran görüntüsü alma
            try:
                self.driver.save_screenshot("device_group_error.png")
                print("Hata ekran görüntüsü kaydedildi: device_group_error.png")
            except:
                pass

    def rename_device(self, new_name):
        """
        Bir cihazın ismini değiştirmek için ilgili işlemleri yapar.
        """
        try:
            # Click the second Edit Icon
            edit_icons = self.wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "i.v-icon.notranslate.mdi.mdi-circle-edit-outline.theme--light")
            ))
            if len(edit_icons) > 1:
                self.driver.execute_script("arguments[0].click();", edit_icons[1])
                print("İkinci edit iconuna başarıyla tıklandı.")
            else:
                print("Yeterli sayıda edit iconu bulunamadı.")
                return

            # Enter New Device Label
            device_label_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//label[contains(text(), 'Device Label')]/following-sibling::input")
            ))
            device_label_input.clear()
            device_label_input.send_keys(new_name)
            print(f"Yeni cihaz ismi başarıyla girildi: {new_name}")

            # Click Save Changes Button
            save_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.v-btn.v-btn--is-elevated.v-btn--has-bg.theme--light.v-size--default.primary")
            ))
            self.driver.execute_script("arguments[0].click();", save_button)
            print("Save Changes butonuna başarıyla tıklandı.")

            # Click OK Button
            ok_button = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled")
            ))
            self.driver.execute_script("arguments[0].click();", ok_button)
            print("OK butonuna başarıyla tıklandı.")
        
        except Exception as e:
            print(f"Cihaz ismi değiştirilirken hata oluştu: {str(e)}")

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


    # CAMERA FONKSIYONLARI
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

    def camera_type_open_attach_dropdown(self):
        """
        Camera tipleri arasında geçiş yapmak için . Alttakiyle beraber kullan.
        """
        try:
            # WebDriverWait nesnesi oluşturulur
            wait = WebDriverWait(self.driver, 10)

            # Kaplamanın kaybolmasını bekle
            wait.until(EC.invisibility_of_element(
                (By.CSS_SELECTOR, "div.v-overlay__scrim")
            ))

            # Menü ikonunu bul ve tıkla
            menu_icon = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#app > div.v-dialog__content.v-dialog__content--active > div > div > div.v-card__text.mt-4 > form > div > div:nth-child(1) > div > div.v-input__control > div > div.v-select__slot > div.v-select__selections")
            ))
            menu_icon.click()
            print("Menü ikonuna tıklandı.")

        except Exception as e:
            print(f"Menü açılırken hata oluştu: {str(e)}")

    def select_physical_option(self):
        """
        Fizikseli seçiyoruz.
        """
        try:
            # WebDriverWait nesnesi oluşturulur
            wait = WebDriverWait(self.driver, 10)

            # Physical seçeneğini içeren tüm öğeleri bul
            options = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.v-list-item__title")
            ))

            # Physical seçeneğini bul ve tıkla
            for option in options:
                if option.text.strip() == "Physical":
                    option.click()
                    print("Physical seçeneği seçildi.")
                    break

        except Exception as e:
            print(f"Physical seçeneği seçilirken hata oluştu: {str(e)}")

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