import traceback

from src.browser import Browser


class Main():
    def __init__(self, chromeApplication, chromeProfile):
        self.chromeApplication = chromeApplication
        self.chromeProfile = chromeProfile
        self.attemps_login = 0
        self.attemps_navigate = 0

    def access_cr_site(self):
        service = Browser(self.chromeProfile, self.chromeApplication)
        service.start_chrome()
        service.start_webDriver()
        if not (service.check_site_access()):
            service.close_chrome()
            self.access_cr_site()
            return
        return self.login_cr_site(service)

    def login_cr_site(self, service):
        try:
            recaptcha_text = service.recaptcha_handling()
            if (recaptcha_text) is None:
                service.resfresh_chrome()
                self.login_cr_site(service)
                return
            if (service.login_handling(recaptcha_text)) is None:
                service.resfresh_chrome()
                self.login_cr_site(service)
                return
        except Exception as err:
            self.attemps_login += 1
            if (self.attemps_login <= 3):
                service.close_chrome()
                self.access_cr_site()
                return
            print(err)
            traceback.print_exc()
            service.close_chrome()
            return
        self.attemps_login = 0
        return self.navigate_cr_site(service)

    def navigate_cr_site(self, service):
        try:
            # if (service.archive_page_handling()) is None:
            #     service.close_chrome()
            #     self.access_cr_site()
            #     return
            if not (service.check_transmition()):
                return
            return
        except Exception as err:
            self.attemps_navigate += 1
            if (self.attemps_navigate <= 0):
                service.close_chrome()
                self.access_cr_site()
                return
            print(err)
            service.close_chrome()
            return


main = Main(r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Users\pedro.santos\Downloads\ProjectCr\chromeprofile')
main.access_cr_site()
