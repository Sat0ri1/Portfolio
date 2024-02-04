import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("windmill.txt", delimiter='\t')

#Wpisujemy pojedyncze kolumny do X i Y
X = df['wind_velocity'] 
Y = df['dc_power']

#Uzytkownik wybiera czy chce uzyc MNK
least_square = input('Jesli chcesz uzyc MNK wpisz T, jesli nie, wpisz inny znak: ') in ['T', 't']
#200 x z zakresu od 1 do 12, robimy macierz
X_new = np.linspace(1, 12, 200).reshape(-1, 1)

if least_square:
    #tworzenie obiektu klasy zawierajacej stopien wielomianu
    poly = PolynomialFeatures(degree=3, include_bias=True)
    #przeformatowujemy dane zeby byly w formie wielomianu
    poly_features = poly.fit_transform(X.to_numpy().reshape(-1, 1))
     #Robimy model regresji liniowej
    poly_reg_model = LinearRegression()
     #Dopasowanie modelu do danych
    poly_reg_model.fit(poly_features, Y.to_numpy().reshape(-1, 1))
    #Predykujemy wartosci do stworzenia wykresu
    Y_new = poly_reg_model.predict(poly.fit_transform(X_new.reshape(-1, 1)))
    #Podstawiamy do predykcji wartosci z ktorych uczylismy model
    Y_pred = poly_reg_model.predict(poly_features)
    #wspolczynniki wielomianu
    print(poly_reg_model.coef_)

     #Do wpisywania ręcznego
else:
    fun1 = lambda x: 0 + 0.2*x + -0.002*x**2

    Y_new = np.array(list(map(fun1, X_new)))
    Y_pred = np.array(list(map(fun1, X)))

#Tworzenie wykresu
plt.scatter(X, Y)
plt.plot(X_new, Y_new, color='red')
plt.show()
plt.savefig(f'wykres.jpg')

print(‘MSE: ‘, mean_squared_error(Y, Y_pred)) #blad
print(‘r2: ’, r2_score(Y, Y_pred)) #wsp determinacji
