from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# options = Options()

# options.add_experimental_option('excludeSwitches', ['enable-logging'])

# driver = webdriver.Chrome(executable_path=r"D:\curso\Python\chromedriver.exe",chrome_options=options)

# url = 'https://carlsagan.com/'

# driver.get(url)


# driver.quit()


def openChrome():
  options = Options()
  options.add_experimental_option('excludeSwitches', ['enable-logging'])
  navegador = webdriver.Chrome(executable_path=r"D:\curso\Python\chromedriver.exe",chrome_options=options)
  return navegador


navegador = openChrome()
navegador.maximize_window()
navegador.get("http://www.google.com")
# import pyautogui
# import time;
# from selenium import webdriver

# navegador = webdriver.Chrome()
# time.sleep(1)
#navegador.maximize_window()
#pyautogui.hotkey("ctrl", "t")
#time.sleep(0.5)
#pyautogui.write("http://google.com.br")
#pyautogui.press("enter")
# time.sleep(3)
# print(pyautogui.position())
#Point(x=1736, y=339)
#Point(x=1815, y=342)