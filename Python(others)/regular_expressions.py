import re
from google.colab import files

# Otwieranie wyżej pobranej zawartości
with open('page.html', 'r') as file:
    zawartosc = file.read()

# Wyciąganie linków wyrażeniem regularnym
# Wyciągamy wszystko co zaczyna się od "src="
# Wykluczamy apostrofy
# Dalej wyciągamy wszystko co ma dane rozszerzenie mogące świadczyć
# o tym, że jest to obraz, czyli .jpg itp.
linki = re.findall(r'src="([^"]+\.(jpg|jpeg|png|gif))"', zawartosc)

# Bazowy adres strony
url = "https://www.tarantupedia.com"

# Formatujemy linki
sformatowane = [f'<img src="{url}{link[0]}" width=10%><hr>' for link in linki]

# Zapisujemy sformatowane linki do pliku HTML
linki_html = "\n".join(sformatowane)
with open('gotowe_linki.html', 'w') as file:
    file.write(linki_html)

# Wyświetlamy kilkanascie gotowych linkow
print("Linki do obrazów:")
for link in sformatowane[:15]:
    print(link)

# Wyświetlamy i pobieramy plik HTML
files.view('gotowe_linki.html')
files.download('gotowe_linki.html')
