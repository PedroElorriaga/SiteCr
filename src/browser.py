import os
import subprocess
import pyautogui as py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from src.utils import Utils
from services.orcService import ORCService


class Browser(Utils):
    def __init__(self, chromeProfile, chromePathApplication):
        self.chromeProfile = chromeProfile
        self.chromePathApplication = chromePathApplication
        self.driver = None

    def start_chrome(self):
        subprocess.Popen([self.chromePathApplication, '--remote-debugging-port=8989',
                         f'--user-data-dir={self.chromeProfile}'])
        self.wait_seconds(5)
        py.moveTo(1171, 352)
        self.wait_seconds(2)
        py.click()
        self.wait_seconds(2)

    def start_webDriver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", "localhost:8989")
        self.driver = webdriver.Chrome(options=options)

    def check_site_access(self):
        attemps = 3
        while attemps > 0:
            try:
                if (py.locateOnScreen(r'C:\Users\pedro.santos\Downloads\ProjectCr\static\imgs\AcessoSiteCr.png')):
                    return True
            except:
                attemps -= 1
        return False

    def recaptcha_handling(self):
        self.print_screenBox(595, 272, 110, 35)
        self.wait_seconds(2)
        response = ORCService.ORCApi()
        error_response = response['IsErroredOnProcessing']
        if (error_response):
            raise Exception('Erro ao processar imagem na API')
        image_text = response['ParsedResults'][0]['ParsedText']

        if (len(image_text) == 6):
            return image_text[1:]
        if (len(image_text) == 5):
            return image_text
        return None

    def close_chrome(self):
        self.driver.close()
        self.driver.quit()

    def login_handling(self, recaptcha_code):
        user_input = self.driver.find_element(
            By.XPATH, '//*[@id="txtLogin"]').send_keys('rciserviços')
        pass_input = self.driver.find_element(
            By.XPATH, '//*[@id="txtSenha"]').send_keys('RCI@2025')
        self.wait_seconds(2)
        recp_input = self.driver.find_element(
            By.XPATH, '//*[@id="txtCodeTextBox"]').send_keys(recaptcha_code)
        enter_button = self.driver.find_element(
            By.XPATH, '//*[@id="btnLogar"]').click()
        self.wait_seconds(3)
        if (self.check_login_access()):
            return
        return True

    def check_login_access(self):
        try:
            error_message = self.driver.find_element(
                By.XPATH, '//*[@id="lblMsg"]')
        except NoSuchElementException:
            return None

        if (error_message.text):
            return True
        return None

    def archive_page_handling(self):
        self.driver.switch_to.frame('fraMenu')
        archives_button = self.driver.find_element(
            By.XPATH, '//*[@id="td1_div1"]/b/span').click()
        self.driver.switch_to.default_content()
        self.wait_seconds(3)
        self.driver.switch_to.frame('fraMain')
        self.driver.switch_to.frame('iFrameMenu')
        rps_button = self.driver.find_element(
            By.XPATH, '//*[@id="form1"]/div[2]/table/tbody/tr/td/div[3]/a').click()
        self.driver.switch_to.default_content()
        self.wait_seconds(3)
        self.driver.switch_to.frame('fraMain')
        choose_file_button = self.driver.find_element(
            By.XPATH, '//*[@id="fileUpload"]').send_keys(r'C:\Users\pedro.santos\Downloads\ProjectCr\arquivo.xml')
        self.wait_seconds(3)
        if (self.check_send_rps_error) is None:
            return
        close_button = self.driver.find_element(
            By.XPATH, '//*[@id="imageButtonFechar"]').click()
        self.wait_seconds(3)
        self.driver.switch_to.default_content()
        return True

    def check_send_rps_error(self):
        try:
            error_element = self.driver.find_element(
                By.CLASS_NAME, 'messageerrortext')
            print('ErroMapeado')
            return True
        except NoSuchElementException:
            return None

    def check_transmition(self):
        self.driver.switch_to.frame('fraMenu')
        archives_button = self.driver.find_element(
            By.XPATH, '//*[@id="td1_div1"]/b/span').click()
        self.driver.switch_to.default_content()
        self.wait_seconds(3)
        self.driver.switch_to.frame('fraMain')
        self.driver.switch_to.frame('iFrameMenu')
        rps_button = self.driver.find_element(
            By.XPATH, '//*[@id="form1"]/div[2]/table/tbody/tr/td/div[7]/a').click()
        self.driver.switch_to.default_content()
        self.wait_seconds(3)
        self.driver.switch_to.frame('fraMain')
        nr_lote_input = self.driver.find_element(
            By.ID, 'textBoxNumLote').send_keys('6293')  # TODO TROCAR PARA DINAMICO
        self.wait_seconds(3)
        search_button = self.driver.find_element(
            By.ID, 'imageButtonPesquisar').click()
        self.wait_seconds(10)
        status = self.driver.find_element(
            By.XPATH, '//*[@id="gridView"]/tbody/tr[2]/td[5]').text
        if (status == 'Processado com sucesso'):
            view_notes = self.driver.find_element(
                By.ID, 'gridView_ctl02_imageButtonVisualizarNotas').click()
            self.wait_seconds(10)
            generate_excel_button = self.driver.find_element(
                By.ID, 'imageButtonGerarExcel').click()
            self.wait_seconds(5)
            self.close_chrome()
            return True
        if (status == 'Processado com erro'):
            view_notes = self.driver.find_element(
                By.ID, 'gridView_ctl02_imageButtonVisualizarErros').click()
            protocol_number = self.driver.find_element(
                By.XPATH, '//*[@id="gridView"]/tbody/tr[2]/td[3]').text
            self.wait_seconds(10)
            self.error_table_handling()
            self.wait_seconds(5)
            self.close_chrome()
            return False

    def error_table_handling(self):
        tr_list = []
        pager_element = self.driver.find_element(
            By.XPATH, '//*[@id="popUpErrosLote_dataPagerErrosLote"]')
        pager_a = pager_element.find_elements(By.TAG_NAME, 'a')
        if (len(pager_a) > 0):
            for i in range(len(pager_a)):
                pager_element = self.driver.find_element(
                    By.XPATH, '//*[@id="popUpErrosLote_dataPagerErrosLote"]')
                a = pager_element.find_elements(By.TAG_NAME, 'a')[i]
                tr_list += self.error_table_messages()
                a.click()
                self.wait_seconds(4)
        else:
            tr_list += self.error_table_messages()

        print(tr_list)
        self.generate_xml_error(
            tr_list, ['Código', 'Mensagem', 'Correção', 'Posição RPS', 'Série RPS', 'Nº RPS'], '6293')

    def resfresh_chrome(self):
        self.driver.refresh()

    def error_table_messages(self):
        tr_list = []
        table_element = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                (By.ID, 'popUpErrosLote_gridViewErrosLote'))
        )
        tr_element = WebDriverWait(table_element, 15).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
        for tr in tr_element[1:]:
            td_list = []
            td_element = tr.find_elements(By.TAG_NAME, 'td')
            for td in td_element:
                td_list.append(td.text)

            tr_list.append(td_list)

        return tr_list
