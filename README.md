# Program do zdalnego(bo z łóżka) uczestniczenia w zajęciach
## Zbudowany dla grupy L2 ale łatwo modyfikowalny
### Uruchomienie
1. Instalacja Selenium - 'pip3 install Selenium'
2. Pobranie stereownika do używanej przeglądarki - tutaj zainstalowany jest domyślnie sterownik do chroma (jak używasz chroma to sie tym nie martw)
3. Ustawienie defaultowej przeglądarki - w linijce 44 kodu definiowany jest obiekt driver ale dla przeglądarki Brave - w komentarzu znajduje sie podpowiedz jak zamienic to na przegladarke chrome
4. W pliku 'pasy.txt' znajduja sie dane logowania do eKonta, musisz uzupelnic zeby dzialalo
5. W pliku 'zajecia.json' jest rozpiska zajęć - co, jak kiedy. Jeżeli chcesz dodać jakieś zajęcia dopisujesz je tam
6. Program odpalamy 'python3 bot.py' programem, który ma uprawnienia admina, np terminal

### Dodawnia zajęć
Niestety nie działa dla każdego przedmniotu, trzeba porównać czy działa podobnie do któregoś z już istniejących.
Zmienne np. 'przyciskPath' to tak zwane xPath z pliku html. Jeżeli nie wiesz jak je znaleźć to polecam Google :)

### Mozliwe problemy
1. Tak jak pisalem wyżej program przystosowany do przegladarki brave - zmiana przegladarki to zmiana kawalka kodu
2. Program został przystosowany do windows najbardziej jak sie da - niestety nie beda dzialac spotkania na zoomie przez brak mozliwosci otwarcia zooma przez terminal.
