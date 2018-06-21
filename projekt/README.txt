PROJEKT III
===========
Biblioteki
----------
Django
gspread
oauth2client

Jak używać
----------
1. Aplikacja jest podłączona pod dokument google:
https://docs.google.com/spreadsheets/d/1LlmEFboIAB1v3lEnZ8zPOkoCxZw_oDWoagm0lQWsJOM/edit?usp=sharing
Ten link umożliwia edycje arkusza.
2. Aplikacja zawiera gotową bazę sql lite dla poprawnego arkusza. W celu
walidacji zmienionego arkusza wymagane jest usunięcie pliku ./wiet/db.sqlite3
i wykonanie z uprawnieniami administratora następującej komendy w folderze ./wiet
  python3 manage.py migrate
3. Uruchamiamy aplikacje komendą:
  python3 manage.py runserver
4. Otwieramy w przeglądarce adres: http://127.0.0.1:8000/validator/
5. Klikamy przycisk Validate.
6. Czekamy -- proces validacji a wraz z nim ładowanie strony może trochę zająć.
7. Jeżeli pojawił się napis OK to możemy prześć dalej patrz punkt 9.
8. Jeżeli pojawił się napis Failed to poniżej znajduje się lista błędów.
Popraw je w arkuszu i ponów kroki od 2.
9. Podaj semestr zgodnie z konwencją p oznacza semestr parzysty a np nieparzysty.
10. Podaj tydzień dla którego rozkład sal chcesz uzyskać. A lub B
11. Kliknij Ok
12. W przypadku niepoprawnych danych otrzymasz komunikat Unknown parameters
13. W przypadku powodzenia otrzymasz nową stronę z listą sal. Dla każdej sali
podany jest dzień tygodnia oraz przedziały czasowe kiedy jest wolna albo napis
WOLNA jeśli jest wolna cały dzień.
