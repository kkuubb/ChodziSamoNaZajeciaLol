from selenium import webdriver
import datetime
import json
import time
import os

PATH = 'chromedriver'
PATHbrave = "/usr/bin/brave-browser"
option = webdriver.ChromeOptions()
option.binary_location = PATHbrave
wolne = True


def odczytajDaneLogowania():
    f = open('pasy.txt')
    dane = []
    dane.append(f.readline().replace('\n', ''))
    dane.append(f.readline().replace('\n', ''))
    return dane


def pobierzDaneOPrzedmiotach():
    jsonf = open('zajecia.json')
    lista = json.load(jsonf)
    return lista


def sprawdzGodzine():
    czas = {'dzien': '', 'godzina': 0, 'minuta': 0}
    now = datetime.datetime.now()
    czas['dzien'] = now.weekday() + 1
    czas['godzina'] = now.hour
    czas['minuta'] = now.minute
    return czas


def sprawdzCoJestTerazITamWejdz(czas, przedmioty):
    global wolne
    global driver
    for przedmiot in przedmioty:
        if czas['dzien'] == przedmioty[przedmiot]['dzien']:
            if czas['godzina'] * 60 + czas['minuta'] > przedmioty[przedmiot]['godzinastart'] * 60 + przedmioty[przedmiot]['minutastart'] and czas['godzina'] * 60 + czas['minuta'] < przedmioty[przedmiot]['godzinakoniec'] * 60 + przedmioty[przedmiot]['minutakoniec']:
                if wolne:
                    # Jezeli uzywasz chrome to zamien driver na:
                    #driver = webdriver.Chrome(PATH)
                    driver = webdriver.Chrome(
                        executable_path=PATH, options=(option))
                    print(driver)
                    driver.maximize_window()
                    zalogujDoEkursy()
                    print("Zalogowano pomyslnie")
                    driver.get(przedmioty[przedmiot]['linkprzedmiot'])
                    print("Jestem na stronie przedmiotu")
                    wolne = False
                    return driver, przedmioty[przedmiot]
                else:
                    return driver, False
    if not(wolne):
        wolne = True
        print("zamykam")
        driver.quit()
        print(driver)
        return driver, False
    else:
        return False, False


def zalogujDoEkursy():
    global driver
    driver.get("https://ekursy.put.poznan.pl/login/index.php")
    loginWithEKonto = driver.find_element_by_xpath(
        '//*[@id="region-main"]/div[2]/div[2]/div[1]/div/div[2]/div/a')
    loginWithEKonto.click()
    loginUsername = driver.find_element_by_xpath('//*[@id="login"]')
    loginPassword = driver.find_element_by_xpath('//*[@id="password"]')
    loginButton = driver.find_element_by_xpath(
        '//*[@id="loginForm"]/div[2]/button')
    dane = odczytajDaneLogowania()
    loginUsername.send_keys(dane[0])
    loginPassword.send_keys(dane[1])
    loginButton.click()


def wejdzNaBB(przedmiot):
    global driver
    driver.get(przedmiot["linkzajecia"])
    joinButton = driver.find_element_by_xpath('//*[@id="join_button_input"]')
    joinButton.click()
    driver.switch_to.window(driver.window_handles[1])
    # print(driver.current_url)
    time.sleep(5)
    listenButton = driver.find_element_by_css_selector(
        "body > div.portal--27FHYi > div > div > div.content--IVOUy > div > div > span > button:nth-child(2) > span.button--Z2dosza.jumbo--Z12Rgj4.default--Z19H5du.circle--Z2c8umk")
    listenButton.click()
    if przedmiot['frek'] == 1:
        driver.switch_to.window(driver.window_handles[0])
        driver.get(
            'https://ekursy.put.poznan.pl/mod/attendance/view.php?id=242233')
        driver.switch_to.window(driver.window_handles[1])


def wejdzNaZoom(przedmiot):
    global driver
    # driver.get(przedmiot["linkprzedmiot"])
    linkDoPodstrony = driver.find_element_by_xpath(
        przedmiot["linkDoPodstrony"].replace("\'", '\"'))
    driver.get(linkDoPodstrony.get_attribute('href'))
    if przedmiot["Przycisk"] == 0:
        linkDoOdpaleniaZooma = przedmiot["LinkDoZooma"]
        if linkDoOdpaleniaZooma.find('uname') != -1:
            id, password, uname = znajdzDaneZoomUname(linkDoOdpaleniaZooma)
            os.system('xdg-open "zoommtg://zoom.us/join?action=join&confno=' +
                      id + '&pwd=' + password + '&uname' + uname + '\"')
        else:
            id, password = znajdzDaneZoom(linkDoOdpaleniaZooma)
            os.system('xdg-open "zoommtg://zoom.us/join?action=join&confno=' +
                      id + '&pwd=' + password + '\"')
    elif przedmiot["Przycisk"] == 1:
        joinMeeting = driver.find_element_by_xpath(przedmiot["PrzyciskPath"])
        joinMeeting.click()
        driver.switch_to_window(driver.window_handles[1])
        linkDoOdpaleniaZooma = driver.current_url
        if linkDoOdpaleniaZooma.find('uname') != -1:
            id, password, uname = znajdzDaneZoomUname(linkDoOdpaleniaZooma)
            os.system('xdg-open "zoommtg://zoom.us/join?action=join&confno=' +
                      id + '&pwd=' + password + '&uname' + uname + '\"')
        else:
            id, password = znajdzDaneZoom(linkDoOdpaleniaZooma)
            os.system('xdg-open "zoommtg://zoom.us/join?action=join&confno=' +
                      id + '&pwd=' + password + '\"')
        driver.switch_to_window(driver.window_handles[0])
    if przedmiot['frek'] == 1:
        driver.switch_to.window(driver.window_handles[0])
        driver.get(
            'https://ekursy.put.poznan.pl/mod/attendance/view.php?id=242233')

    # driver.get(linkDoZooma.get_attribute('href'))


def znajdzDaneZoom(link):
    id = link[link.find(
        '/j/') + 3:link.find('?pwd')]
    password = link[link.find('pwd=') + 4:]
    return id, password


def znajdzDaneZoomUname(link):
    id = link[link.find(
        '/j/') + 3:link.find('?pwd')]
    password = link[link.find('pwd=') + 4:link.find('&uname')]
    return id, password, 'Jakub%20Różycki'


def wejdzNaZajecia(przedmiot):
    global driver
    if przedmiot['typ'] == "bb":
        wejdzNaBB(przedmiot)
    if przedmiot['typ'] == "zoom":
        wejdzNaZoom(przedmiot)


while True:
    time.sleep(1)
    czas = sprawdzGodzine()
    przedmioty = pobierzDaneOPrzedmiotach()
    driver, coJest = sprawdzCoJestTerazITamWejdz(czas, przedmioty)
    if coJest:
        wejdzNaZajecia(coJest)