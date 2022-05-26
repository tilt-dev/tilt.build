import argparse
import os
import string
import random
from selenium import webdriver
from selenium.webdriver.firefox import options as firefoxoptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

window_size = (1280,720)
url = "http://localhost:10350/r/(Tiltfile)/overview"
css_selector = "div.Pane2"
filename = ""
wait_timeout = 5

# os.environ['MOZ_HEADLESS_WIDTH'] = str(window_size[0])
# os.environ['MOZ_HEADLESS_HEIGHT'] = str(window_size[1])

def parse_args():
    return

def take_screenshot():
    session = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
    print('Started session '+session)

    opts = firefoxoptions.Options()
    opts.headless = True
    driver = webdriver.Firefox(options=opts)
    driver.set_window_size(window_size[0],window_size[1])
    driver.get(url)

    try:
        WebDriverWait(driver, wait_timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    except TimeoutException:
        print('Timed out')
        sys.exit(1)

    screenshot_file = filename
    if screenshot_file == "":
        screenshot_file = '/app/screenshots/screenshot'+session+'.png'

    driver.save_screenshot(screenshot_file)

    print("Saved %s" % screenshot_file)

    driver.quit()
    return

def main():
    parse_args()
    take_screenshot()

if __name__ == '__main__':
    main()
