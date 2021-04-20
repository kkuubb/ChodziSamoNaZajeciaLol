from selenium import webdriver
import datetime
import json
import time
import os
import platform
from threading import Thread
import sys


# Dla uzytkownikow chroma i brave
# if platform.system() == 'Windows':
#     PATH = 'drivers/chromedriver.exe'
# elif platform.system() == 'Linux':
#     PATH = 'drivers/chromedriver'
# PATHbrave = "/usr/bin/brave-browser"
# option = webdriver.ChromeOptions()
# option.binary_location = PATHbrave


# Dla uzytkownikow Firefox
if platform.system() == 'Windows':
    PATH = 'drivers/geckodriver.exe'
elif platform.system() == 'Linux':
    PATH = 'drivers/geckodriver'
else:
    PATH = 'drivers/geckodrivermac'

plikjson = "L2.json"
wolne = True
#sprawdzajZajecia = True
wybieramPrzedmiot = False


def odczytajDaneLogowania():
    f = open('pasy.txt')
    dane = []
    dane.append(f.readline().replace('\n', ''))
    dane.append(f.readline().replace('\n', ''))
    return dane


def pobierzDaneOPrzedmiotach():
    jsonf = open(plikjson)
    lista = json.load(jsonf)
    return lista


def sprawdzGodzine():
    czas = {'dzien': '', 'godzina': 0, 'minuta': 0}
    now = datetime.datetime.now()
    czas['dzien'] = now.weekday() + 1
    czas['godzina'] = now.hour
    czas['minuta'] = now.minute
    return czas


def sprawdzCoJestTerazITamWejdz(driver, czas, przedmioty):
    global wolne
    #global driver
    for przedmiot in przedmioty:
        if czas['dzien'] == przedmioty[przedmiot]['dzien']:
            if czas['godzina'] * 60 + czas['minuta'] >= przedmioty[przedmiot]['godzinastart'] * 60 + przedmioty[przedmiot]['minutastart'] and czas['godzina'] * 60 + czas['minuta'] < przedmioty[przedmiot]['godzinakoniec'] * 60 + przedmioty[przedmiot]['minutakoniec']:
                if wolne:
                    # Jezeli uzywasz Firefox to zamien driver na:
                    driver = webdriver.Firefox(executable_path=PATH)
                    # Jezeli uzywasz chrome to zamien driver na:
                    # driver = webdriver.Chrome(PATH)
                    # Jezeli uzywasz Brave
                    # driver = webdriver.Chrome(executable_path=PATH, options=(option))
                    # print(driver)
                    driver.maximize_window()
                    zalogujDoEkursy(driver)
                    print("Zalogowano pomyslnie")
                    # driver.get(przedmioty[przedmiot]['linkprzedmiot'])
                    print("Jestem na stronie przedmiotu")
                    if (przedmioty[przedmiot]["typ"] == "bb" or przedmioty[przedmiot]["typ"] == "zoom" or przedmioty[przedmiot]["typ"] == "0"):
                        driver.get(przedmioty[przedmiot]['linkprzedmiot'])
                    wolne = False
                    return driver, przedmioty[przedmiot]
                else:
                    return driver, False
    if not(wolne):
        wolne = True
        #print(driver)
        driver.quit()
        print("Zajecia sie skonczyly, zamykam przegladarke")
        # print(driver)
        return driver, False
    else:
        return False, False


def zalogujDoEkursy(driver):
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
    time.sleep(2)
    if driver.current_url == "https://ekursy.put.poznan.pl/login/index.php":
        loginWithEKonto.click()


def wejdzNaBB(driver, przedmiot):
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
    print("Jestem na zajeciach na BBB")


def wejdzNaZoom(driver, przedmiot):
    # driver.get(przedmiot["linkprzedmiot"])
    linkDoPodstrony = driver.find_element_by_xpath(
        przedmiot["linkDoPodstrony"].replace("\'", '\"'))
    driver.get(linkDoPodstrony.get_attribute('href'))
    if przedmiot["Przycisk"] == 0:
        linkDoOdpaleniaZooma = przedmiot["LinkDoZooma"]
        if linkDoOdpaleniaZooma.find('uname') != -1:
            id, password, uname = znajdzDaneZoomUname(linkDoOdpaleniaZooma)
            os.system('xdg-open "zoommtg://zoom.us/join?action=join&confno=' +
                      id + '&pwd=' + password + '&uname' + uname + '\"' + " > /dev/null")
        else:
            id, password = znajdzDaneZoom(linkDoOdpaleniaZooma)
            os.system('xdg-open "zoommtg://zoom.us/join?action=join&confno=' +
                      id + '&pwd=' + password + '\"' + " > /dev/null")
    elif przedmiot["Przycisk"] == 1:
        joinMeeting = driver.find_element_by_xpath(przedmiot["PrzyciskPath"])
        joinMeeting.click()
        driver.switch_to_window(driver.window_handles[1])
        linkDoOdpaleniaZooma = driver.current_url
        if linkDoOdpaleniaZooma.find('uname') != -1:
            id, password, uname = znajdzDaneZoomUname(linkDoOdpaleniaZooma)
            os.system('xdg-open "zoommtg://zoom.us/join?action=join&confno=' +
                      id + '&pwd=' + password + '&uname' + uname + '\"' + " > /dev/null")
        else:
            id, password = znajdzDaneZoom(linkDoOdpaleniaZooma)
            os.system('xdg-open "zoommtg://zoom.us/join?action=join&confno=' +
                      id + '&pwd=' + password + '\"' + " > /dev/null")
        driver.switch_to_window(driver.window_handles[0])
    if przedmiot['frek'] == 1:
        driver.switch_to.window(driver.window_handles[0])
        driver.get(
            'https://ekursy.put.poznan.pl/mod/attendance/view.php?id=242233')
    print("Jestem na zajeciach na Zoom")
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


def wejdzNaZajecia(driver, przedmiot):
    #global driver
    if przedmiot['typ'] == "bb":
        print("Probuje wejsc na BBB")
        wejdzNaBB(driver, przedmiot)
    elif przedmiot['typ'] == "zoom":
        print("Probuje wejsc na Zoom")
        if platform.system() == 'Linux':
            wejdzNaZoom(driver, przedmiot)
        if platform.system() == 'Windows':
            print("Niestety spotkania na zoomie nie sa obslugiwane na windowsie (nie ma mozliwosci otwarcia zooma przez terminal)")
    elif przedmiot['typ'] == "0":
        print("Niestety tych zajec Ci nie otworze :/")
    else:
        print("Odbywaja sie teraz zajecia ale nie chciales zebym ich otwieral")


def sprawdzanieZajec():
    driver = ""
    while True:
        try:
            czas = sprawdzGodzine()
            przedmioty = pobierzDaneOPrzedmiotach()
            #print(driver)
            driver, coJest = sprawdzCoJestTerazITamWejdz(driver, czas, przedmioty)
            if coJest:
                wejdzNaZajecia(driver, coJest)
            time.sleep(30)

        except:
            print("Zamnkieto przegladarke\n\n\n")


def wejdzNaStronePrzedmiotu():
    przedmioty = pobierzDaneOPrzedmiotach()
    k = 1
    lista = []
    for i in przedmioty:
        print(str(k) + ". ", i)
        lista.append(i)
        k += 1
    przedmiot = int(input("Podaj numerek przedmiotu: "))
    driver = webdriver.Firefox(executable_path=PATH)
    driver.maximize_window()
    zalogujDoEkursy(driver)
    driver.get(przedmioty[lista[przedmiot - 1]]["linkprzedmiot"])
    while True:
        try:
            driver.window_handles[0]
        except:
            print("Zamnkieto przegladarke\n\n\n")
            break


def odswiezMenu():
    global wybieramPrzedmiot
    while True:
        time.sleep(120)
        if not(wybieramPrzedmiot):
            print("\n\nPROSTE MENU!!!!!!!!!!!!")
            print("1. Otworz strone przedmiotu")
            print("2. Zamknij program")
            print("Co chcesz zrobic: ")
        else:
            przedmioty = pobierzDaneOPrzedmiotach()
            k = 1
            print("\n\n")
            for i in przedmioty:
                print(str(k) + ". ", i)
                k += 1
            print("Podaj numerek przedmiotu: ")


if __name__ == "__main__":
    watki = []
    watekMenu = Thread(target=odswiezMenu)
    watekMenu.daemon = True
    watekMenu.start()
    watekZajecia = Thread(target=sprawdzanieZajec)
    watekZajecia.daemon = True
    watekZajecia.start()
    while True:
        print("PROSTE MENU!!!!!!!!!!!!")
        print("1. Otworz strone przedmiotu")
        print("2. Zamknij program")
        wybieramPrzedmiot = False
        x = input("Co chcesz zrobic: ")
        if x == "1":
            wybieramPrzedmiot = True
            x = 0
            watki.append(Thread(target=wejdzNaStronePrzedmiotu()))
            watki[-1].start()
            # wejdzNaStronePrzedmiotu()
        elif x == "2":
            sys.exit()
