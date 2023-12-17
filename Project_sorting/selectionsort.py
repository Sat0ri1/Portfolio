#selection sort(niestabilny):

def selection_sort(lista):
    n = len(lista) #zapisujemy dlugosc listy do n
    for i in range(n - 1): #petla przez wszystkie elementy listy( n-1 bo indeksowanie listy zaczyna sie od 0, czyli pierwszy element ma indeks 0)
        min_index = i # zapisujemy indeks liczac ze tu jest minimum
        for j in range(i + 1, n):  # iterujemy przez pozostale indeksy
            if lista[j] < lista[min_index]: #jesli liczba z indeksem j(na poczatku 1) jest mniejsza od liczby z indeksem minx index(na poczatku 0)
                min_index = j #ustawiamy min index jako j, czyli aktualna najmniejsza liczbe przypisujemy do min_index

        # Tu jest ta niestabilnosc, bo zamieniamy element stojacy za i z elementem stojacym za min_index
        # jesli te elementy sa sobie rowne to i tak zamienią się miejscami
        lista[i], lista[min_index] = lista[min_index], lista[i]

#wytkumaczenie niestabilnosci:
#sortowanie jest niestabilne jesli algorytm zamienia miejscami rowne sobie elementy
lista = [5, 1, 7, 2, 9, 7, 3] #siodemka i trojka dopisana by pokazac niestabilnosc
#INDEKS: 5 1 7 2 9
selection_sort(lista)
print("Posortowna lista:", lista)

#wezmy powyzszy zmieniony indeks z dopisaną siodemka i trojka [5, 1, 7, 2, 9, 7, 3]
#Pierwsza iteracja: min_index = 0, elementem ktory tu stoi jest liczba 5, porownujemy ja z j(indeks 1), gdzie stoi jedynka, ta jest mniejsza
                    #wiec jedynka staje sie naszym min_index, w ostatnim kroku zamieniamy je miejscami i mamy [1, 5, 7, 2, 9, 7, 3]
                    

#Druga iteracja: naszym i jest teraz liczba 5(ma indeks 1, a petle for z kazdym przejsciem zwiekszaja indeks na ktorym iterujemy o 1 zeby przejsc przez cala liste)
                #uznajemy indeks 1(piatka) za min_index i iterujemy przez kolejne indeksy(i+1)
                #teraz trafiamy na 7, ale ona jest wieksza od 5 wiec stoja w dobrej kolejnosci, dalej trafiamy na 2
                #poniewaz 2<5 to min index = 2, zamieniamy miejscami 5 i 2, otrzymujemy ciag [1, 2, 7, 5, 9, 7, 3]

#trzecia iteracja: zaczyna sie od indeksu 2, czyli od 7, pamietaj ze pierwszy element listy zawsze ma indeks = 0/
                #nasza siodemka staje sie min_index, w drugiej petli  od razu trafiamy na 5. 7>5 wiec zamieniamy je miejscami
                #teraz mamy taki ciag: [1, 2, 5, 7, 9, 7, 3] 

#czwarta iteracja: zaczyna sie od indeksu 3, czyli od liczby 7. Trafiamy na 9, ale ta nie jest mniejsza od 7, wiec idziemy dalej
                #trafiamy na 7 nie jest mniejsza od 7, wiec idziemy dalej i trafiamy na 3. Oznaczmy sobie siodemki zeby widziec co sie dzieje:
                #[1, 2, 5, 7(1), 9, 7(2), 3] pierwsza siodemka ktora jest naszym i "trafia" na liczbe 3. Te liczby zamieniamy miejscami i otrzymujemy:
                #[1, 2, 5, 3, 9, 7(2), 7(1)]

#piata iteracja: zaczynamy od indeksu 4, czyli liczby 9. Trafiamy na 7(2), 7 jest mniejsze od 9 wiec zmieniaja sie miejscami i mamy ciag:
                #[1, 2, 5, 3, 7(2), 9, 7(1)]

#szosta iteracja: zaczynamy od indeksu 5 czyli liczby 9, trafiamy na 7(1), tj wyzej, 7 < 9, zamieniamy miejscami i konczymy z 
                #POSORTOWANYM JUZ ciagiem [1, 2, 5, 3, 7(2), 7(1), 9]

#Na powyzszym przykladzie widac jak siodemki zamienily sie miejscami, to obrazuje niestabilnosc metody sortowania przez wybor