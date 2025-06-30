import time
import random
from typing import List

import requests
import sys
import pyperclip

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys


def connect_rabby(driver: webdriver, wait):
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(random.uniform(2, 3))
    confirm_buttons = driver.find_elements(By.TAG_NAME, 'button')
    driver.execute_script('arguments[0].click();', confirm_buttons[0])


def add_chain(driver: webdriver.Chrome):
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(random.uniform(3, 4))
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    driver.execute_script('arguments[0].click();', buttons[1])

def confirm_in_rabby(driver: webdriver.Chrome):
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(random.uniform(2, 3))
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    driver.execute_script('arguments[0].click();', buttons[0])
    time.sleep(random.uniform(1, 2))
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    # print(buttons)
    driver.execute_script('arguments[0].click();', buttons[0])


def click_button_by_xpath(xpath, wait: WebDriverWait, driver: webdriver.Chrome):
    button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    driver.execute_script("arguments[0].click();", button)


def create_profile(name, proxy_host=None, proxy_port=None, proxy_user=None, proxy_password=None, sys_app_cate_id=39898):
    url = "http://127.0.0.1:50325/api/v1/user/create"
    user_agents = random.choice([
        # Chrome (132-135)
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    ])
    version_browser = random.choice(["131", "132"])

    if proxy_host:
        payload = {
            "name": str(name),
            "group_id": "0",
            "country": "us",
            "sys_app_cate_id": sys_app_cate_id,  # Отвечает за расширения
            "fingerprint_config": {
                "language": ["en-US"],
                "flash": "block",
                "webrtc": "proxy",
                "do_not_track": "true",
                "browser_kernel_config": {
                    "version": version_browser,
                    "type": "chrome"
                },
                "ua": user_agents
            },

            "user_proxy_config": {
                "proxy_soft": "other",
                # "proxy_soft": "no_proxy",
                "proxy_type": "socks5",
                "proxy_host": proxy_host,
                "proxy_port": proxy_port,
                "proxy_user": proxy_user,
                "proxy_password": proxy_password
            },
            "random_cookie": True
        }
    else:
        payload = {
            "name": str(name),
            "group_id": "0",
            "country": "us",
            "sys_app_cate_id": sys_app_cate_id,  # Отвечает за расширения
            "fingerprint_config": {
                "language": ["en-US"],
                "flash": "block",
                "webrtc": "proxy",
                "do_not_track": "true",
                "browser_kernel_config": {
                    "version": version_browser,
                    "type": "chrome"
                },
                "ua": user_agents
            },

            "user_proxy_config": {
                "proxy_soft": "no_proxy",
            },
            "random_cookie": True
        }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request(
        "POST", url, headers=headers, json=payload).json()

    return response['data']['id']


def open_profile(ads_id):
    open_url = "http://127.0.0.1:50325/api/v1/browser/start?user_id=" + ads_id

    resp = requests.get(open_url).json()
    if resp["code"] != 0:
        print(resp["msg"])
        print("please check ads_id")
        sys.exit()

    chrome_options = Options()
    chrome_options.add_experimental_option(
        "debuggerAddress", resp["data"]["ws"]["selenium"])

    chrome_driver = resp['data']['webdriver']
    service = Service(executable_path=chrome_driver)

    return webdriver.Chrome(service=service, options=chrome_options)


def close_profile(ads_id):
    close_url = "http://127.0.0.1:50325/api/v1/browser/stop?user_id=" + ads_id
    requests.get(close_url)


def delete_profile(ads_id):
    url = "http://localhost:50325/api/v1/user/delete"

    payload = {
        "user_ids": [
            ads_id
        ]
    }
    headers = {
        'Content-Type': 'application/json'
    }

    return requests.request("POST", url, headers=headers, json=payload)


def log_in_rabby(driver, wait, seed_phrase):
    driver.switch_to.window(driver.window_handles[-1])
    driver.refresh()
    time.sleep(random.uniform(3, 4))

    driver.execute_script(
        "document.getElementsByTagName('button')[1].click();")
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]')))
    driver.find_element(
        By.XPATH, '//*[@id="root"]/div/div/div[2]/div[1]').click()

    seed_phrase = seed_phrase
    pyperclip.copy(seed_phrase)
    search = driver.find_element(
        By.XPATH, '//*[@id="root"]/div/div/form/div/div/div/div/div/div/div[2]/div[1]/input')
    search.send_keys(pyperclip.paste())
    time.sleep(random.uniform(1, 3))
    driver.find_element(
        By.XPATH, '//*[@id="root"]/div/div/form/button').click()

    # password
    password = 'Rabby!!!'
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="password"]')))

    passwd = driver.find_element(By.XPATH, '//*[@id="password"]')
    passwd.send_keys(password)

    # confirm password
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="confirmPassword"]')))
    passwd = driver.find_element(By.XPATH, '//*[@id="confirmPassword"]')
    passwd.send_keys(password)

    # continue
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="root"]/div/div/div/form/footer/button')
    ))
    driver.find_element(
        By.XPATH, '//*[@id="root"]/div/div/div/form/footer/button').click()

    # import to wallet
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="root"]/div/div/button')
    ))
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/button').click()

    # last click
    button = driver.find_element(
        By.CSS_SELECTOR,
        'button.ant-btn.ant-btn-primary.ant-btn-block'
    )
    button.click()


def get_proxie(filename, num=1) -> List[str]:
    """Возвращает список из 4 строк (proxy_host, proxy_port, proxy_user, proxy_password)."""
    with open(file=filename, mode='r') as f:
        proxies = f.readlines()
        proxies = [x.strip() for x in proxies]
        return proxies[num - 1].split(':')


def get_seed(filename, num=1) -> str:
    """Возвращает seed фразу"""
    with open(file=filename, mode='r') as f:
        seeds = f.readlines()
        seeds = [x.strip() for x in seeds]
        return seeds[num - 1]


def get_ads_profiles():
    with open('C:\\Users\\wagmi\\Desktop\\Scripts\\monag_gm\\monad_gm_files\\ads_profiles.txt', mode='r') as f:
        file = f.readlines()
    ads_id = [x.strip().split('=')[1] for x in file[1::3]]
    return ads_id


def close_all_windows_except_current(driver):
    current_window = driver.current_window_handle
    all_windows = driver.window_handles

    for window in all_windows:
        if window != current_window:
            driver.switch_to.window(window)
            driver.close()

    driver.switch_to.window(current_window)


def input_password_in_rabby(driver: webdriver.Chrome):
    driver.get('chrome-extension://acmacodkjbdgmoleebolmdjonilkdbch/notification.html#/unlock')
    time.sleep(random.uniform(2, 3))
    driver.find_element(By.TAG_NAME, 'input').send_keys('Rabby!!!' + Keys.ENTER)


def check_count_windows(driver: webdriver.Chrome):
    time_close = 0
    while time_close < 5:
        if len(driver.window_handles) > 1:
            return True
        time_close += 1
        time.sleep(1)
    return False


def tap_on_monad_card(driver):
    monad_card = WebDriverWait(driver=driver, timeout=20).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-network-id='10143']"))
    )
    connect_button = monad_card.find_elements(By.TAG_NAME, "button")[1]
    WebDriverWait(driver, 20).until(
        lambda d: not connect_button.get_attribute("disabled")
    )
    is_disabled = connect_button.get_attribute("disabled")
    if is_disabled:
        print("Кнопка заблокирована!")
    driver.execute_script("arguments[0].click();", connect_button)

