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
2. Program byl pisany na linuxie i pod linuxa jest przystosowany - nie powinno miec to wplywu na dzialanie spotkan na BBB ale moze miec wplyw na odpalanie sie zooma. W tym poradniku chyba wszystko jest wytłumaczone jak to zrobić na windowsie- 'https://superuser.com/questions/1563255/start-a-zoom-meeting-from-the-command-line'. Trzeba zmienic kod w linijkach 112, 116, 125, 129. Trzeba również zamienic chromedriver na chromedriver.exe.
