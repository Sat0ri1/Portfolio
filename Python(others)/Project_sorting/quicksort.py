#Quicksort, Paweł Grygielski i Michał Somala(do prezentacji metody), 17.11.2022

import time

#Funkcja, która pozwoli nam na znalezienie miejsca w ktorym podzielimy liste
def podzial(lista, low, high):

	#wybieramy skrajny element z prawej strony listy jako pivot
	pivot = lista[high]

	#tworzymy wskaźnik
	i = low - 1

    #przyrównujemy wszystkie elementy do pivota
	for j in range(low, high):
		if lista[j] <= pivot:

			#Jeśli znajdziemy coś mniejszego niż pivot, zamieniamy miejscami z i
            #Za i będzie stać wtedy albo liczba większa od j albo ona sama

			i = i + 1

			#Zamieniamy elementy miejscami
			(lista[i], lista[j]) = (lista[j], lista[i])

	#Jeśli nie znaleźliśmy liczby mniejszej(lub równej) niż pivot to zamieniamy go miejscami z i(większa liczba)
	(lista[i + 1], lista[high]) = (lista[high], lista[i + 1])

	return i + 1


def quickSort(lista, low, high):
	if low < high:

		p = podzial(lista, low, high)

		#Funkcje rekurencyjne dla lewej i prawej strony pivotu
		quickSort(lista, low, p - 1)

		quickSort(lista, p + 1, high)

dane = []

l = len(dane)
print("Nieposortowana lista: ", dane)

tm = time.perf_counter()

quickSort(dane, 0, l - 1)

tm = time.perf_counter()-tm

print('Posortowana lista: ', dane, 'Sortowanie zajelo: ', tm)
