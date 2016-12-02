# Gra w Pythonie

W ramach zajęć z języka *Python* została stworozna prosta gra typu arcade, przy użyciu pakietu **Pygame**.  
Gra została oparta na tytule *River Ride* i jest napisana w języku *Phyton 3.5*. Niniejszy plik zawiera krótki opis gry, instrukcje jak zacząć rozgrywkę oraz listę wykorzystanych źródeł.

# Instrukcja

Grę uruchamiamy wpisując w konsolę komendę
```
./main_game.py
```
Musimy znajdywac się w scieżce zawierającego wszystkie pozostałe skrypty i foldery dołączone do powyższego pliku.

W grze dostępne są trzy okna:
* MENU
* OPTIONS
* GAME WINDOW

W *MENU* poruszamy się za pomocą klawiszy <kbd>UP</kbd> oraz <kbd>DOWN</kbd>. Wyobru dokonujemy klikająć klawisz <kbd>ENTER</kbd>. Dostępne są trzy opcje
* *START*: kliknięcie rozpocznie rozgrywkę.
* *OPTIONS*: kliknięcie zainicjuje okno OPTIONS.
* *QUIT*: kliknięcie spowouje wyjscie z gry i zamknięcie okna.

W oknie OPTIONS możemy zmienić niektóre ustawienia gry. Pomiędzy polami poruszamy się przy pomocy kalwiszy <kbd>UP</kbd> oraz <kbd>DOWN</kbd>. Gdy dana opcja została wybrana wybieramy poziom danego parametru przy pomocy klawiszy <kbd>LEFT</kbd> oraz <kbd>RIGHT</kbd>. Gdy wskaźniki **>** ustawimy na żądane poziomy wychodzimy klikając <kbd>ENTER</kbd> po zaznaczeniu pola EXIT. Ustawienia zostaną zapisane do pliku 
```
options.txt
```
i wczytane w momencie uruchomienia rozgrywki.

## Rozgrywka

Celem gry jest pokonanie jak największej odległości i uzyskanie jak największej liczby punktów. 
Po planszy poruszamy się czerownym statkiem przy pomocy klawiszy
* <kbd>UP</kbd> oraz <kbd>DOWN</kbd> w osi pionowej,
* <kbd>LEFT</kbd> oraz <kbd>RIGHT</kbd> w osi poziomej.

By zestrzelwać nadlatujące obiekty używamy klaiwsza <kbd>SPACE</kbd>.  W rogach ekranu widoczne są parametry statku: poziom paliwa i schłodzenia broni. Pierwszy uzupełniamy zestrzeliwując nadpływające beczki. Drugi opada automatycznie gdy przestaniemy strzelać. 
W lewym, górnym rogu wyświetla się nasz aktualny wynik, który zależy od liczby i rodzaju zniszczonych obiektów.
Rozbicie pojazdu nastąpi w skutek:
* Kolizji z:
  * helikopterem,
  * samolotem,
  * terenem (wyspa, arkady mostu),
  * mostem,
* wylotu poza planszę.
* Braku paliwa.

W podmenu OPTIONS możemy zmienić częstość pojawiania się wysp lub helikopterów by zmienić poziom trudności.
  
# Autor

* wkocin

# Licencja 
Gra została udostępniona pod licencją  MIT.

# Źródła plików wykorzystanych podczas tworznia gry

* Czcionka zostłą pobrana ze strony http://www.dafont.com/
* Pliki dźwiękowe zostały pobrane ze strony http://soundbible.com/ , w oparciu o licencję CC BY 3.0.
* Pliki graficzne zostały pobrane ze stron:
  * http://www.pd4pic.com/ 
  * http://opengameart.org
  
 w oparciu o licencję CC0 1.0 Universal (CC0 1.0) .
 
# Python Game

During Python programming course at university a simple arcade was created, using **Pygame** pakacge. The game was based on original *River Ride* game and was developed i *Python 3.5* programming language. This file contains hsort description and instructions how to start playing and the list of sources of used files. 

# Instructions 

We run the game by typing in command window the following text
```
./main_game.py
```
The directory is presumed to contain all the other files commited with the game.

In game three windows are available:

* MENU
* OPTIONS
* GAME WINDOW

In *MENU* we move using <kbd>UP</kbd> and <kbd>DOWN</kbd> keys. We confirm our choice by klicking <kbd>ENTER</kbd> key. Three options are available

* *START*: starts the game.
* *OPTIONS*: initializes OPTIONS menu.
* *QUIT*: ends game and closes the window.

In OPTIONS window we can change some of the game settings. One moves verivally using <kbd>UP</kbd> and <kbd>DOWN</kbd> keys. We choose a xertain level of given game parameter by moving horizontally with <kbd>LEFT</kbd> and <kbd>RIGHT</kbd> keys. When an arrows **>** are placed in wanted positions we confirm our choice by sliding on EXIT and clikcing <kbd>ENTER</kbd>. Chosen settings will be automatically saved in 
```
options.txt
```
file.

## Gameplay

The aim of the game is to cover the longest distance and score as many points as possible by shooting down enemies and other obstacles. We move using arrow keys, namely
* <kbd>UP</kbd> and <kbd>DOWN</kbd>,
* <kbd>LEFT</kbd> and <kbd>RIGHT</kbd>.

To shoot down incoming objects we press  <kbd>SPACE</kbd>. In the bottom corners of the screen we can see two mesueres of ship parameters - cooldown rate and fuel level. We fill the tank by shooting incoming barrels. The gun cools down automatically afetr we stop shooting. 
In the left top corner we can observe our actual score, which depends on number of shoot down objects. The crush follows events like:
* Collison with:
  * a helicopter,
  * a plane,
  * parts of the terrain (islands and green parts of the bridge),
  * a bridge 
* Leaving screen,
* Lack of fuel.
In the OPTIONS submenu we can change frequency of incoming helicopters, islands and the volume level.

# Author

* wkocin

# License 
The game is lincsed under MIT License.

#  Sources of used files 

* The font was downloaded from http://www.dafont.com/
* Sound files were downloaded from http://soundbible.com/ , under CC BY 3.0 License.
* Graphic files were downloaded from:
  * http://www.pd4pic.com/ 
  * http://opengameart.org
  
 under CC0 1.0 Universal (CC0 1.0) License.
