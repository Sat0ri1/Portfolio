#zad 4, Pawel Grygielski, Michal Somala 22.01.2023
"""
Czy podany graf nieskierowany jest drzewem? 
Jesli jest spojny ale nie jest drzewem, wypisac cykl
"""
import os

"""
### ODCZYTYWANIE LISTY SASIEDZTW ###
Tworzymy slownik.
Otwieramy plik.
Dzielimy wiersz na pojedyncze elementy.
Usuwamy pierwszy element.
Jezeli klucza w nie ma w grafie to dodajemy w jako klucz, 
a pod wartosc przypisujemy wiersz
"""
def lista_sasiedztw(sciezka):
    graf = { }
    with open(sciezka) as s:
        for wiersz in s.readlines():
            wiersz = wiersz.split()
            if wiersz:
                w = wiersz.pop(0)
                if not w in graf:
                    graf[w] = (wiersz)
    return graf


"""
### SPRAWDZENIE SPOJNOSCI ###
Sprawdzamy czy z podanego wierzcholka jest sciezka do kazdego innego wierzcholka
"""
def spojnosc(graf, wierzcholek):
    for i in graf:
        bfs = Przeszukiwanie_wszerz(graf, wierzcholek, i)
        if not bfs:
            return False
    return True

"""
### PRZESZUKIWANIE WSZERZ ###
Tworzymy liste wierzcholkow ktore bedziemy sprawdzac
Tworzymy liste odwiedzonych wierzcholkow ktore juz sprawdzilismy
Dopoki sa elementy do sprawdzenia:
-Wyciagamy pierwszy element z listy
-jesli ten element = cel to zwracamy true
-jesli ten element != cel i nie zostal odwiedzony, 
 dodajemy go do odwiedzonych i dajemy jego sasiadow do sprawdzenia
-jesli nie znaleziono sciezki do celu, zwracamy false
"""
def Przeszukiwanie_wszerz(graf, poczatek, cel):
    do_sprawdzenia = [poczatek]  
    odwiedzone = [] 
    while do_sprawdzenia: 
        obecnie_sprawdzany = do_sprawdzenia.pop(0)  
        if obecnie_sprawdzany == cel:     
            return True    
        else:   
            if obecnie_sprawdzany not in odwiedzone:   
                odwiedzone.append(obecnie_sprawdzany)  
                do_sprawdzenia.extend(graf[obecnie_sprawdzany]) 
    return False    
"""
Tworzymy liste ktora bedzie zawierac cykl
Tworzymy slownik odwiedzonych
Tworzymy liste z listy kluczy i bierzemy pierwszy element:
cyklicznosc_rec(list(graf.keys())[0]
"""

def cyklicznosc(graf):
    cykl = []
    odwiedzone = []
    return cyklicznosc_rec(list(graf.keys())[0], -1, odwiedzone, graf, cykl)

"""
Dodajemy obecny wierzcholek do odwiedzonych.
Dodajemy obecny wierzcholek do cyklu.
Przechodzimy przez wszystkich sasiadow obecnego wierzcholka

Jesli sasiad nie byl odwiedzony:  
-Przeszukujemy wglab
-Wywolujemy metode cyklicznosc rec dla sasiada
-Jesli znalezlismy cykl to go zwracamy

Jesli sasiad byl odwiedzony i nie jest wierzch. porpzednim:
-Bierzmy cykl od sasiada i go zwracamy

Usuwamy obecny z cyklu i zwracamy false
"""

def cyklicznosc_rec(obecny, poprzedni, odwiedzone, graf, cykl):
    odwiedzone.append(obecny)
    cykl.append(obecny)
    for sasiad in graf[obecny]:
        if not sasiad in odwiedzone:
            condition, cykl = cyklicznosc_rec(sasiad, obecny, odwiedzone, graf, cykl)
            if condition:
                return True, cykl
        elif poprzedni != sasiad:
            return True, cykl[cykl.index(sasiad):]
    cykl.remove(obecny)
    return False, cykl
        

sciezka = input('Podaj sciezke do pliku: ')
wierzcholek = input("Podaj wierzcholek do sprawdzenia spojnosci: ")

assert os.path.exists(sciezka), "Nie znaleziono sciezki: "+str(sciezka)


V = lista_sasiedztw(sciezka)
print(f"Lista sąsiedztw: \n{V}\n")

"""
Jeśli graf jest spojny i:
-cykliczny to wypisujemy cykl
-nie ma cyklu, to informujemy ze jest drzewem
Jesli graf jest niespojny, informujemy ze jest niespojny
"""

if spojnosc(V, wierzcholek):
    condition, cykl = cyklicznosc(V)
    if condition:
        print(f"cykl: \n{cykl}\n")
    else:
        print("Graf jest drzewem")
else:
    print("Graf nie jest spójny")
