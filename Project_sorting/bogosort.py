#bogosort polega na losowym ukladaniu ciagu a pozniej na sprawdzaniu czy jest posortowany. W najgorszym przypadku moze to trwac w nieskonczonosc
import random 
lista = [10, 22, 1, 19, 2, 18, 2, 0, 99, 3]

#funkcja do sprawdzania czy ciag jest posortowany
def sprawdz_posortowanie(lista): #jedyny parametr to lista
    n = len(lista) #zapisujemy dlugosc listy do n 
    for i in range(n - 1): # iterujemy po dlugosci listy -1, bo indeksowanie listy zaczyna sie od 0
        if lista[i] > lista[i + 1]: #jesli 1 element wiekszy niz 2 element to nie sa posortowane
            return False #zwracamy false
    return True #jesli przeszlismy po calej dlugosci i wszystko bylo posortowane to zwracamy true

def bogosort(lista):
    while sprawdz_posortowanie(lista) == False: #jesli funkcja sprawdz posortowanie dala nam false(jednoczesnie wywolujemy tą funkcję):
        random.shuffle(lista) #mieszamy 


#odpalamy

bogosort(lista)

# printujemy posortowana liste
print("Posortowana lista:", lista)

