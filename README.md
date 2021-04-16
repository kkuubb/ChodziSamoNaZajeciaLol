# Program do zdalnego(bo z łóżka) uczestniczenia w zajęciach
## Zbudowany dla grupy L2 ale łatwo modyfikowalny
### Uruchomienie
1. Instalacja Selenium - 'pip3 install Selenium'
2. Pobranie stereownika do używanej przeglądarki - sterowniki kompatybilne z wersją w czasie tworzenia znajduja sie w folderze drivers, jezeli chcesz zmienic przegladarke odkomentuj wybrane wiersze (9-23)
3. Ustawienie defaultowej przeglądarki - w linijce 49 kodu definiowany jest obiekt driver ale dla przeglądarki - w komentarzu znajduje sie podpowiedz jak zamienic to na przegladarke np brave, chrome - defaultowo ustawiony jest firefox (najmniej problematyczny)
4. W pliku 'pasy.txt' znajduja sie dane logowania do eKonta, musisz uzupelnic zeby dzialalo
5. W pliku 'L2.json' jest rozpiska zajęć - co, jak kiedy. Jeżeli chcesz dodać jakieś zajęcia dopisujesz je tam
6. Program odpalamy 'python3 bot.py' programem, który ma uprawnienia admina, np terminal

### Dodawnia zajęć
Niestety nie działa dla każdego przedmiotu, trzeba porównać czy działa podobnie do któregoś z już istniejących.
Zmienne np. 'przyciskPath' to tak zwane xPath z pliku html. Jeżeli nie wiesz jak je znaleźć to polecam Google :)

### Mozliwe problemy
1. Program został przystosowany do windows najbardziej jak sie da - niestety nie beda dzialac spotkania na zoomie przez brak mozliwosci otwarcia zooma przez terminal.
2. Przy uyciu przegldarki brave na linuxie nie dziala zamykanie okna po skonczeniu zajec. Problem zdaje sie nie wystepowac przy uzyciu chrome oraz firefox.
