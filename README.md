# Program do zdalnego (bo z łóżka) uczestniczenia w zajęciach
## Zbudowany dla grupy L2 ale łatwo modyfikowalny
### Uruchomienie
1. Instalacja Selenium - 'pip3 install Selenium'
2. Pobranie stereownika do używanej przeglądarki - sterowniki kompatybilne z wersjami przegladarek w czasie tworzenia znajduja sie w folderze drivers
3. W pliku 'pasy.txt' znajduja sie dane logowania do eKonta, musisz uzupelnic zeby dzialalo
5. W pliku 'L2.json' jest rozpiska zajęć - co, jak kiedy. Jeżeli chcesz dodać jakieś zajęcia dopisujesz je tam
6. Konfiguracji programu dokonujemy w panelu konfiguracyjnym w linijkach od 9 do 20
7. Program odpalamy 'python3 bot.py' programem, który ma uprawnienia admina, np terminal

### Dodawnia zajęć
Niestety nie działa dla każdego przedmiotu, trzeba porównać czy działa podobnie do któregoś z już istniejących.
Zmienne np. 'przyciskPath' to tak zwane xPath z pliku html. Jeżeli nie wiesz jak je znaleźć to polecam Google :)

### Mozliwe problemy
1. Program został przystosowany do windows najbardziej jak sie da - niestety nie beda dzialac spotkania na zoomie przez brak mozliwosci otwarcia zooma przez terminal.
2. Przy uyciu przegldarki brave na linuxie nie dziala zamykanie okna po skonczeniu zajec. Problem zdaje sie nie wystepowac przy uzyciu chrome oraz firefox.
