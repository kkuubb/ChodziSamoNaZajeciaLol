from selenium import webdriver
import datetime
import json
import time
import os
import platform
wolne = True

# ######################## panel Kotrolny #####################################
# Uzupełnij dane logowania - pasy.txt

# Z jakiego pliku chcesz korzystac:
plikjson = "L2.json"

# Podaj imie i nazwisko (chuj wie czemu taki format, zoom tak robi)
imieINazwisko = 'Jakub%20Różycki'

# Z jakiej przegladarki chcesz korzystac(1. firefox, 2. Chrome, 3. Brave)
przegladarka = 1

# Jezeli uzywasz brave zmien lokalizacje programu (jezeli potrzeba)
PATHbrave = "/usr/bin/brave-browser"

# Jezli nie chcesz zeby jakies zajecia sie odpalaly, zmien ich typ w pliku json
# na jakikolwiek inny niz bb, zoom albo 0

# ######################## panel Kotrolny #####################################

if przegladarka == 3:
    # Dla uzytkownikow brave
    if platform.system() == 'Windows':
        PATH = 'drivers/chromedriver.exe'
    elif platform.system() == 'Linux':
        PATH = 'drivers/chromedriver'
    else:
        PATH = 'drivers/chromedrivermac'
    option = webdriver.ChromeOptions()
    option.binary_location = PATHbrave

if przegladarka == 1:
    # Dla uzytkownikow Firefox
    if platform.system() == 'Windows':
        PATH = 'drivers/geckodriver.exe'
        print("Windows")
    elif platform.system() == 'Linux':
        PATH = 'drivers/geckodriver'
        print("linux")
    else:
        PATH = 'drivers/geckodrivermac'
        print("mac")

if przegladarka == 2:
    # Dla uzytkownikow chroma
    if platform.system() == 'Windows':
        PATH = 'drivers/chromedriver.exe'
    elif platform.system() == 'Linux':
        PATH = 'drivers/chromedriver'
    else:
        PATH = 'drivers/chromedrivermac'


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


def sprawdzCoJestTerazITamWejdz(czas, przedmioty):
    global wolne
    global driver
    for przedmiot in przedmioty:
        if czas['dzien'] == przedmioty[przedmiot]['dzien']:
            if czas['godzina'] * 60 + czas['minuta'] > przedmioty[przedmiot]['godzinastart'] * 60 + przedmioty[przedmiot]['minutastart'] and czas['godzina'] * 60 + czas['minuta'] < przedmioty[przedmiot]['godzinakoniec'] * 60 + przedmioty[przedmiot]['minutakoniec']:
                if wolne:
                    # Jezeli uzywasz Firefox to zamien driver na:
                    if przegladarka == 1:
                        driver = webdriver.Firefox(executable_path=PATH)
                    # Jezeli uzywasz chrome to zamien driver na:
                    if przegladarka == 2:
                        driver = webdriver.Chrome(PATH)
                    # Jezeli uzywasz Brave
                    if przegladarka == 3:
                        driver = webdriver.Chrome(
                            executable_path=PATH, options=(option))
                    # print(driver)
                    driver.maximize_window()
                    zalogujDoEkursy()
                    print("Zalogowano pomyslnie")
                    print("Jestem na stronie przedmiotu")
                    if (przedmioty[przedmiot]["typ"] == "bb" or
                        przedmioty[przedmiot]["typ"] == "zoom" or
                            przedmioty[przedmiot]["typ"] == "0"):
                        driver.get(przedmioty[przedmiot]['linkprzedmiot'])
                    wolne = False
                    return driver, przedmioty[przedmiot]
                else:
                    return driver, False
    if not(wolne):
        wolne = True
        print("Zajecia sie skonczyly, zamykam przegladarke")
        driver.quit()
        # print(driver)
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
    time.sleep(2)
    if driver.current_url == "https://ekursy.put.poznan.pl/login/index.php":
        loginWithEKonto.click()


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
    print("Jestem na zajeciach na BBB")


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
    print("Jestem na zajeciach na Zoom")
    # driver.get(linkDoZooma.get_attribute('href'))


def wejdzNaZoomMac(przedmiot):
    global driver
    # driver.get(przedmiot["linkprzedmiot"])
    linkDoPodstrony = driver.find_element_by_xpath(
        przedmiot["linkDoPodstrony"].replace("\'", '\"'))
    driver.get(linkDoPodstrony.get_attribute('href'))
    if przedmiot["Przycisk"] == 0:
        linkDoOdpaleniaZooma = przedmiot["LinkDoZooma"]
        if linkDoOdpaleniaZooma.find('uname') != -1:
            id, password, uname = znajdzDaneZoomUname(linkDoOdpaleniaZooma)
            os.system('open "zoommtg://zoom.us/join?action=join&confno=' +
                      id + '&pwd=' + password + '&uname' + uname + '\"')
        else:
            id, password = znajdzDaneZoom(linkDoOdpaleniaZooma)
            os.system('open "zoommtg://zoom.us/join?action=join&confno=' +
                      id + '&pwd=' + password + '\"')
    elif przedmiot["Przycisk"] == 1:
        joinMeeting = driver.find_element_by_xpath(przedmiot["PrzyciskPath"])
        joinMeeting.click()
        driver.switch_to_window(driver.window_handles[1])
        linkDoOdpaleniaZooma = driver.current_url
        if linkDoOdpaleniaZooma.find('uname') != -1:
            id, password, uname = znajdzDaneZoomUname(linkDoOdpaleniaZooma)
            os.system('open "zoommtg://zoom.us/join?action=join&confno=' +
                      id + '&pwd=' + password + '&uname' + uname + '\"')
        else:
            id, password = znajdzDaneZoom(linkDoOdpaleniaZooma)
            os.system('open "zoommtg://zoom.us/join?action=join&confno=' +
                      id + '&pwd=' + password + '\"')
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
    return id, password, imieINazwisko


def wejdzNaZajecia(przedmiot):
    global driver
    if przedmiot['typ'] == "bb":
        print("Probuje wejsc na BBB")
        wejdzNaBB(przedmiot)
    elif przedmiot['typ'] == "zoom":
        print("Probuje wejsc na Zoom")
        if platform.system() == 'Linux':
            wejdzNaZoom(przedmiot)
        elif platform.system() == 'Windows':
            print("Niestety spotkania na zoomie nie sa obslugiwane na windowsie (nie ma mozliwosci otwarcia zooma przez terminal)")
        else:
            wejdzNaZoomMac(przedmiot)
    elif przedmiot['typ'] == "0":
        print("Niestety tych zajec Ci nie otworze :/")
    else:
        print("Odbywaja sie teraz zajecia ale nie chciales zebym ich otwieral")


while True:
    czas = sprawdzGodzine()
    przedmioty = pobierzDaneOPrzedmiotach()
    driver, coJest = sprawdzCoJestTerazITamWejdz(czas, przedmioty)
    if coJest:
        wejdzNaZajecia(coJest)
    time.sleep(30)
