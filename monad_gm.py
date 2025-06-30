import time
import random
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from monad_gm_core.monad_gm_functions import connect_rabby, add_chain, confirm_in_rabby, click_button_by_xpath, \
    open_profile, close_profile, get_ads_profiles, \
    close_all_windows_except_current, input_password_in_rabby, check_count_windows, tap_on_monad_card


def monad_gm(profile):
    global connect_button
    driver = open_profile(ads_id=profile)
    wait = WebDriverWait(driver=driver, timeout=15)
    driver.set_page_load_timeout(15)
    driver.implicitly_wait(5)
    try:
        driver.maximize_window()
    except:
        # print("не получилось расширить окно")
        pass
    try:
        driver.get('https://onchaingm.com/')
        time.sleep(random.uniform(1, 2))
        close_all_windows_except_current(driver)
        driver.refresh()
        time.sleep(random.uniform(2, 3))

        # auth rabby
        driver.switch_to.new_window()
        input_password_in_rabby(driver)
        time.sleep(random.uniform(1, 2))
        driver.switch_to.window(driver.window_handles[0])
        driver.refresh()
        time.sleep(random.uniform(2, 3))

        # switch chain
        # ToDo: добавить нажатие по пустому окну, если монад уже выбран

        try:
            chain_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='rk-chain-button']")))
            img_src = "https://onchaingm.com/chains/monad.jpg"
            try:
                monad_chain = chain_button.find_element(By.CSS_SELECTOR, f"img[src='{img_src}']")
            except:
                monad_chain = False

            if not monad_chain:
                click_button_by_xpath(xpath="//button[@data-testid='rk-chain-button']", wait=wait,
                                      driver=driver)
                time.sleep(random.uniform(1, 2))
                click_button_by_xpath(xpath="//button[.//div[text()='Monad']]", wait=wait, driver=driver)
                time.sleep(random.uniform(1, 2))
                if check_count_windows(driver):
                    add_chain(driver)
                time.sleep(random.uniform(2, 3))
                driver.switch_to.window(driver.window_handles[0])
        except:
            pass

        # testchain button
        testchain_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div/div[1]/div/div/main/div[1]/div[1]/button[4]')))
        driver.execute_script("arguments[0].click();", testchain_button)
        time.sleep(random.uniform(2, 3))

        # monad card
        monad_card = WebDriverWait(driver=driver, timeout=60).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "[data-network-id='10143']"))
        )
        # print('find monad card')

        # ждем пока кнопки станут доступны
        button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@data-network-id='10143']//button[contains(., 'GMonad on Monad')]"))
        )
        # print('button ready')

        monad_buttons = monad_card.find_elements(By.TAG_NAME, "button")
        # print(monad_buttons)
        for button in monad_buttons:
            try:
                button_text = button.text
            except:
                button_text = False
            # print(button_text)
            if button_text in ['GMonad on Monad', 'Connect']:
                connect_button = button
                # print('found connect button')
                break

        if connect_button:
            try:
                WebDriverWait(driver, 60).until(
                    lambda d: not connect_button.get_attribute("disabled")
                )

                is_disabled = connect_button.get_attribute("disabled")
                if is_disabled:
                    print("Кнопка заблокирована!")
            except:
                pass

        driver.execute_script("arguments[0].click();", connect_button)
        time.sleep(random.uniform(2, 3))

        # click rabby wallet
        try:
            click_button_by_xpath('/html/body/div[2]/div/div/div[2]/div/div/div/div/div[1]/div[2]/div[2]/div/button',
                                  driver=driver, wait=wait)
            time.sleep(random.uniform(4, 5))

            # connect_rabby
            connect_rabby(driver, wait)
            time.sleep(random.uniform(2, 3))

            driver.switch_to.window(driver.window_handles[0])
            time.sleep(random.uniform(2, 3))

            # switch chain
            try:
                click_button_by_xpath(xpath="//button[@data-testid='rk-chain-button']", wait=wait,
                                      driver=driver)
                time.sleep(random.uniform(1, 2))
                click_button_by_xpath(xpath="//button[.//div[text()='Monad']]", wait=wait, driver=driver)
                time.sleep(random.uniform(1, 2))

                if check_count_windows(driver):
                    add_chain(driver)
                time.sleep(random.uniform(2, 3))
                driver.switch_to.window(driver.window_handles[0])
            except:
                pass

            # second tap on monad card
            tap_on_monad_card(driver)
            time.sleep(random.uniform(4, 5))
        except:
            pass

        confirm_in_rabby(driver)
        time.sleep(random.uniform(3, 4))
        success = True
    except Exception as e:
        success = False
        # print(e)
    finally:
        driver.quit()
        close_profile(ads_id=profile)

    return success


if __name__ == '__main__':
    ads_profiles = get_ads_profiles()
    for profile in ads_profiles:
        flag = monad_gm(profile)
        print(f'{ads_profiles.index(profile) + 1}: {"❌" if not flag else "✅"}')
