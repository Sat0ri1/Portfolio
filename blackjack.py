from random import shuffle


#________________________TWORZENIE TALII I TASOWANIE_______________________
"""Tworzenie listy talia i jej przetasowanie z uzyciem funkcji shuffle z pakietu random. 
Funkcja bedzie wykorzystana przed gra oraz w jej trakcie w przypadku gdy skoncza sie karty"""
def tasowanie():
    talia = ["AS(♥)", "AS(♠)", "AS(♣)", "AS(♦)", "Krol(♥)", "Krol(♠)", "Krol(♣)", "Krol(♦)",
             "Dama(♥)", "Dama(♠)", "Dama(♣)", "Dama(♦)", "Walet(♥)", "Walet(♠)", "Walet(♣)",
            "Walet(♦)", "10(♥)", "10(♠)", "10(♣)", "10(♦)", "9(♥)", "9(♠)", "9(♣)", "9(♦)",
             "8(♥)", "8(♠)", "8(♣)", "8(♦)", "7(♥)", "7(♠)", "7(♣)", "7(♦)", "6(♥)", "6(♠)",
            "6(♣)", "6(♦)", "5(♥)", "5(♠)", "5(♣)", "5(♦)", "4(♥)", "4(♠)", "4(♣)", "4(♦)",
            "3(♥)", "3(♠)", "3(♣)", "3(♦)", "2(♥)", "2(♠)", "2(♣)", "2(♦)"]
    shuffle(talia)
    return talia


#________________DEFINICJA ZKLADU I ODJECIE ZAKLADU OD KWOTY________________
"""Ta funkcja wykorzystana bedzie za kazdym razem gdy uzytkownik bedzie chcial postawic zaklad,
a wiec na poczatku kazdej iteracji petli tak dlugo jak uzytkownik chce grac"""

def zaklad(kwota):
    print("Masz na koncie:", kwota, "$")
    
    #Tak dlugo jak uzytkownik podaje nieliczbowy input, nie wyjdzie z petli while
    while True: 
        input_1 = input("Podaj kwote zakladu: ")
        if input_1.isdigit():
            kwota_zakladu = int(input_1)
            break
        else:
            print("Nieprawidlowa kwota. Podaj liczbe.")
    #Druga petla while bedzie dzialac dopoki uzytkownik nie poda kwoty wiekszej od 1 i nie wiekszej niz stan konta
    z = kwota_zakladu
    while z < 1 or z > kwota:
        z = int(input("Podaj kwote wieksza od 0 nieprzekraczajaca twojego stanu konta: "))
    
    #Odejmujemy zaklad od stanu konta(kwota) 
    kwota -=z
    return z, kwota


#______________________________ROZDANIE KART________________________________
"""Funkcja rozdaje 2 karty dla gracza i krupiera przy kazdej iteracji
oraz pokazuje graczowi jego karty oraz pierwsza karte krupiera. 
Poniewaz blackjack w duzej mierze polega na liczeniu kart, indeks przechodzi miedzy iteracjami,
to podejscie wymaga jednak zabezpieczenia indeksu i tasowania kart na nowo gdy dojdziemy do konca listy"""

def rozdanie(talia, i):

    #Tworzymy puste listy na ktorych beda znajdowac sie karty
    gracz = []
    krupier = []
    try:
        i #jesli mamy wskaznik z poprzedniej itercji to zostawiamy
    except NameError:
        i = 0 #jesli wskaznik nie istnieje to go tworzymy
    
    #Petla rozdajaca karty graczowi
    while len(gracz) < 2:
        if i == 51: 
            gracz.append(talia[i]) #jesli wskaznik dojdzie do ostatniej karty, chcemy zeby ja rozdal
            i = 0 #Po rozdaniu ostatniej karty wskaznik ustawiamy na 0 i tasujemy nowa talie
            talia = tasowanie()
        else: #jesli wskaznik nie doszedl do ostatniej karty to wydajemy karte graczowi
            gracz.append(talia[i])
            i += 1  #przesuwamy wskaznik do przodu
    print("Twoje karty:", gracz)

    #Petla rozdajaca karty krupierowi
    while len(krupier) < 2:
        if i == 51:
            krupier.append(talia[i])
            i = 0
        else:
            krupier.append(talia[i])
            i += 1
    print("Pierwsza karta krupiera:", krupier[1])
    return gracz, krupier, i

#______________________________DOBIERANIE GRACZ_______________________________
"""Ta funckaj pozwala graczowi dobierac dodatkowe karty. 
W blackjacku gracz moze dobierac karty az nie bedzie usatysfakcjonowany wynikiem
Funkcja zadaje wiec pytanie o dobranie kolejnej karty, dopoki gracz nie zrezygnuje wpisujac 'nie'.
Funkcja zawiera to samo zabezpieczenie indeksu co w przypadku funkcji rozdajacej karty"""

def dobieranie(gracz, talia, i):
    dobranie = input("czy chcesz dobrac karte? (wpisz 'tak' lub 'nie'): ")
    while dobranie != "tak" and dobranie != "nie":
        dobranie = input("czy chcesz dobrac karte? (wpisz 'tak' lub 'nie'): ")
    while dobranie == "tak":
        if i == 51:
            gracz.append(talia[i])
            i = 0 
            talia = tasowanie()
        else:
            gracz.append(talia[i])
            i += 1

        print("Twoje karty:", gracz)
        
        dobranie = input("czy chcesz dobrac karte? (wpisz 'tak' lub 'nie'): ")
    return gracz, i


#_____________________________Liczenie pnuktow________________________________
"""Funkcja optymalna_kombinacja_asy pozwala wyliczyc optymalna punktacje dla asow,
zarowno dla gracza jak i dla krupiera. 
Jest to konieczne, poniewaz w blackjacku as moze byc wart 1 lub 11 pkt, a talia moze zawierac 4 asy
Funkcja ta jest pierwotnie wywolywana przez kolejna funkcje 'oblicz_punkty' a nastepnie poprzez rekurencje,
wywoluje sama siebie"""

def optymalna_kombinacja_asy(ilosc_asow, kombinacja_aktualna, wynik):
    if ilosc_asow == 0: #bedzie wykonywac sie w nieskonczonsoc dopoki nie zotanie spelnione
        wynik.append(sum(kombinacja_aktualna)) #jesli nie ma juz asow to dodajemy sume do wyniku
    elif ilosc_asow > 0: #jezeli mamy jeszcze asy
        # Dodajemy Asa jako 1 do kombinacji i rekurencyjnie powtarzamy dla reszty asow
        optymalna_kombinacja_asy(ilosc_asow - 1, kombinacja_aktualna + [1], wynik)
        # Dodajemy Asa jako 11 do kombinacji i rekurencyjnie powtarzamy dla reszty asow
        optymalna_kombinacja_asy(ilosc_asow - 1, kombinacja_aktualna + [11], wynik)

"""Funkja oblicz_punkty tworzy liste asow i wywoluje funckje optymalna_kombinacja_asy, nastepnie zlicza punkty 
i wybiera najlepsza kombinacje punktow za asy w stosunku do pozostalych kart, przy ktorych punktacja jest stala"""

def oblicz_punkty(reka):
    asy = []
    for karta in reka:
        if karta.startswith("AS"):
            asy.append(karta)
    ilosc_asow = len(asy)  #zapisujemy ilosc asow potrzbna do wywolania funkcji optymalna_kombinacja_asow

    kombinacje_punktow = []
    optymalna_kombinacja_asy(ilosc_asow, [], kombinacje_punktow) #wywolujemy rekurencyjna funkcje optymalna_kombinacja_asy

    suma_punktow = [] #tu bedzie ostateczna suma pkt dla kazdej kombinacji

    for kombinacja in kombinacje_punktow: #iterujemy przez kombinacje na liscie kombinacje_punktow
        
        if type(kombinacja) == list: #jesli kombinacja jest lista
            suma_kombinacji = sum(kombinacja) #przypisujemy zsumowane elemnty do suma_kombinacji
        else: #jesli nie jest lista
            suma_kombinacji = kombinacja #przypisujemy kombinacje bez zmian do sumy kombinacji
        

        punkty_reka = 0

        for karta in reka:

            if karta.startswith("Krol") or karta.startswith("Dama") or karta.startswith("Walet") or karta.startswith("10"):
                punkty_reka += 10
    
            elif karta.startswith("9"):
                punkty_reka += 9

            elif karta.startswith("8"):
                punkty_reka += 8

            elif karta.startswith("7"):
                punkty_reka += 7

            elif karta.startswith("6"):
                punkty_reka += 6

            elif karta.startswith("5"):
                punkty_reka += 5

            elif karta.startswith("4"):
                punkty_reka += 4

            elif karta.startswith("3"):
                punkty_reka += 3

            elif karta.startswith("2"):
                punkty_reka += 2

        suma_punktow.append(suma_kombinacji + punkty_reka) #pkt za asy do pozostalych pkt

    dostepne_sumy = []
    for suma in suma_punktow:
        if suma <= 21:
            dostepne_sumy.append(suma)

    if dostepne_sumy:
        return max(dostepne_sumy)  # Wybieramy najwyzsza sume, ktora nie przekracza 21
    else:
        return min(suma_punktow)  # Wybieramy najnizsza sume, jesli wszystkie przekraczaja 21

#___________________________________Dobieranie krupiera______________________________________________
"""Krupier dobiera karty dopiero po podliczeniu punktow za rozdanie,
poniewaz musi dobierac gdy ma mniej niz 17 pkt i nie moze juz dobierac
gdy ma 17 lub wiecej punktow. W zwiazku z tym konieczne jest stworzenie petli,
ktora po kazdym dobraniu sprawdza punkty ponownie i dodaje karte krupierowi
za kazdym razem gdy ma mniej niz 17pkt. 
Tu takze obecne jest zabezpieczenie wskaznika"""

def dobieranie_krupiera(talia, krupier, i):
    suma_punktow_krupier = oblicz_punkty(krupier)
    while suma_punktow_krupier < 17:
        if i == 51:
            krupier.append(talia[i])
            i = 0
            talia = tasowanie()
        else:
            krupier.append(talia[i])
            i += 1
        suma_punktow_krupier = oblicz_punkty(krupier)
    return krupier, i, suma_punktow_krupier

#_____________________________________WYLONIENIE ZWYCIEZCY_________________________________________
"""warunkujemy mozliwe zwyciestwa i przegrane, w przypadku zwyciestwa mnozymy z(zaklad) * 2
I wygrana trafia na konto gracza(kwota). W przypadku remisu zwracamy kwote zakladu.
Gdy gracz przegra nie odzyskuje postawionych pieniedzy. 
Jesli punkty gracza i krupiera nie przekraczaja 21, wygrywa ten kto ma ich wiecej. 
Jesli punkty gracza i krupiera przekraczaja 21, wygrywa ten, kto ma ich mniej.
Jesli punkty gracza i krupiera sa sobie rowne, wystepuje remis 
Jesli tylko 1 z 'osob'(gracz/krupier), przekroczy 21, wygrywa ten, kto nie przekroczyl 21"""

def zwyciestwo(suma_punktow_gracz, suma_punktow_krupier, z, kwota):
    if suma_punktow_gracz > suma_punktow_krupier:
        if suma_punktow_gracz <= 21:
            z *= 2
            kwota += z
            print("WYGRYWASZ", z, "$! Lacznie posiadasz:", kwota, "$." )

        elif suma_punktow_gracz > 21:
            print("PRZEGRYWASZ", z, "$! Pozostalo ci:", kwota, "$." )

    elif suma_punktow_gracz < suma_punktow_krupier:

        if suma_punktow_krupier <= 21:
            print("PRZEGRYWASZ", z, "$! Pozostalo ci:", kwota, "$." )

        elif  suma_punktow_krupier > 21:
            z *= 2
            kwota += z
            print("WYGRYWASZ", z, "$! Lacznie posiadasz:", kwota, "$." )
    
    elif suma_punktow_gracz == suma_punktow_krupier:
        kwota += z
        print("REMIS. Postawione:", z, "$ wraca na twoje konto. Lacznie posiadasz:", kwota, "$." )
    return kwota
#_________________________________WCZYTYWANIE ZAPISU Z PLIKU_____________________________________
"""Aby gracz mogl korzystac z poprzedniego stanu konta w kolejnych grach, wczytujemy kwote z pliku tekstowego.
Jesli nie istnieje plik z zapisem, przydzielamy graczowi startowy 1000$"""

def wczytaj_kwote_z_pliku(nazwa_pliku="zapis_gry.txt"):
    try:
        with open(nazwa_pliku, "r") as plik:
            return int(plik.read())
    except FileNotFoundError:
        print("Plik z zapisem nie istnieje. Otrzymujesz startowe 1000$.")
        return 1000  # Jesli nie ma pliku, dajemy startowy 1000


#________________________________________PORZADEK GRY___________________________________________
"""funkcja blackjack sprawdza stan kotna, a nastepnie wywoluje inne funkcje w odpowiednim porzdku
Dodatkowo wyswietla koncowy zestaw kart gracza i krupiera oraz sume punktow przed wylonieniem zwyciezcy"""

def blackjack(kwota, i):
    if kwota <= 0:
        kwota = 1000
        print("Przegrales wszystkie pieniadze, otrzymujesz 1000 na start")
    z, kwota = zaklad(kwota)
    gracz, krupier, i = rozdanie(talia, i)
    gracz, i = dobieranie(gracz, talia, i)
    krupier, i, suma_punktow_krupier = dobieranie_krupiera(talia, krupier, i)
    suma_punktow_gracz = oblicz_punkty(gracz)
    print("twoje karty:", gracz)
    print("twoje punkty:", suma_punktow_gracz)
    print("karty krupiera: ", krupier)
    print("punkty krupiera: ", suma_punktow_krupier)
    kwota = zwyciestwo(suma_punktow_gracz, suma_punktow_krupier, z, kwota)
    return kwota, i

#________________________________ZAPISYWANIE KWOTY DO PLIKU_____________________________________
"""Zapis kwoty do pliku (zapisujemy ja do miejsca gdzie znajduje sie skrypt, aby nie zadac sciezek do pliku)"""
def zapisz_kwote_do_pliku(kwota, nazwa_pliku="zapis_gry.txt"):
    with open(nazwa_pliku, "w") as plik:
        plik.write(str(kwota))

#________________________________________GRA____________________________________
"""Skrypt wczytuje kwote, wywoluje pierwsze tasowanie, (ktore nie moze byc w funkcji blackjack,
aby nie odbywalo sie w kazdej iteracji), wywoluje funkcje blackjack w petli dopoki gracz
nie zrezygnuje z gry. 
Po wyjsciu z petli(odpowiedz 'nie' na pytanie 'Czy chcesz grac? (wpsiz 'tak' lub 'nie'):'
Gracz jest pytany o chec zapisu dla pliku, jesli odmowi, gra zamyka sie bez zapisu."""

i = 0 # Musi byc zmienna globalna zeby przekazywac pomiedzy iteracjami

rozgrywka = input("Czy chcesz grac? (wpisz 'tak' lub 'nie'): ")
while rozgrywka != "tak" and rozgrywka != "nie":
    rozgrywka = input("Czy chcesz grac? (wpisz 'tak' lub 'nie'): ")

kwota = wczytaj_kwote_z_pliku()

talia = tasowanie()

while rozgrywka == "tak":
    kwota, i = blackjack(kwota, i)
    rozgrywka = input("Czy chcesz grac? (wpsiz 'tak' lub 'nie'): ")
    while rozgrywka != "tak" and rozgrywka != "nie":
        rozgrywka = input("Czy chcesz grac? (wpsiz 'tak' lub 'nie'): ")


zapis = input("Czy chcesz zapisac kwote do dalszej gry? (wpsiz 'tak' lub 'nie'): ")
while zapis != "tak" and zapis != "nie":
    zapis = input("Czy chcesz zapisac kwote do dalszej gry? (wpsiz 'tak' lub 'nie'): ")
if zapis == "tak":
    zapisz_kwote_do_pliku(kwota)
    print("Zapisano kwote. Dziekuje za gre.")
else:
    print("Zakonczono bez zapisu. Dziekuje z gre.")

