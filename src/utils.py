import time
import pyautogui as py
import pandas as pd


class Utils():
    def wait_seconds(self, seconds):
        time.sleep(seconds)

    def print_screenBox(self, x, y, width, height):
        screenshot = py.screenshot(region=(x, y, width, height))
        screenshot.save(
            r'C:\Users\pedro.santos\Downloads\ProjectCr\temp\image.png')

    def generate_xml_error(self, data, columns, lote):
        return pd.DataFrame(data, columns=columns).to_excel(lote + '.xlsx', index=False)
