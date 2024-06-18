import requests
from bs4 import BeautifulSoup
import pandas as pd

START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

headers = ["Nombre", "Constelación", "Ascensión Recta", "Declinación", "Magnitud", "Distancia (pc)", "Espectro", "Masa (M_J)", "Radio (R_J)", "Descubrimiento"]

star_data = []

headers_req = {"User-Agent": "Mozilla/5.0"}
try:
    response = requests.get(START_URL, headers=headers_req)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error al obtener la página: {e}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all("table", {"class": "wikitable"})

if len(tables) < 3:
    print("No se encontraron suficientes tablas en la página.")
    exit()

table = tables[2]

rows = []

for i, row in enumerate(table.find_all("tr")):
    if i < 7:  
        continue
    cells = row.find_all("td")
    if len(cells) >= 10:
        star = [
            cells[0].text.strip(),
            cells[1].text.strip(),
            cells[2].text.strip(),
            cells[3].text.strip(),
            cells[4].text.strip(),
            cells[5].text.strip(),
            cells[6].text.strip(),
            cells[7].text.strip(),
            cells[8].text.strip(),
            cells[9].text.strip()
        ]
        star_data.append(star)

star_df = pd.DataFrame(star_data, columns=headers)

star_df.to_csv("field_brown_dwarfs.csv", index=False)


