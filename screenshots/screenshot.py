import string
import random
from selenium import webdriver
from selenium.webdriver.firefox import options as firefoxoptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

default_window_size = (1280,720)
tiltfile_overview_url = "http://localhost:10350/r/(all)/overview"
default_wait_timeout = 5
css_selector = "div.Pane2"

class Screenshot(object):
    def __init__(self, filename="", url=tiltfile_overview_url, git_repo=None, tiltfile=None):
        self.filename = filename
        self.url = url
        self.git_repo = git_repo
        self.tiltfile = tiltfile


class Screenshotter(object):
    def __init__(self, window_size=default_window_size, wait_timeout=default_wait_timeout):
        self.wait_timeout=wait_timeout
        opts = firefoxoptions.Options()
        opts.headless = True
        self.driver = webdriver.Firefox(options=opts)
        self.driver.set_window_size(window_size[0], window_size[1])

    def take_screenshot(self, screenshot):
        self.driver.get(screenshot.url)
        try:
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        except TimeoutException:
            print('Timed out')
            sys.exit(1)

        filename = screenshot.filename
        if filename == "":
            id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
            filename = 'screenshot%s.png' % id

        screenshot_file = '/app/screenshots/%s' % filename

        self.driver.save_screenshot(screenshot_file)

        print("Saved %s" % screenshot_file)
        return

    def close(self):
        self.driver.quit()
        return

if __name__ == '__main__':
    take_screenshot()
