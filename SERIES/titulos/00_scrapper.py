import os, requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

###########
with open (os.path.join(os.path.dirname(__file__), '00_urls.txt'), 'r', encoding='utf-8') as w:
    urls = [line for line in w if line.strip() != ""]

class Titulos_episodios:
    
    def __init__(self, url):
        self.enlace = unquote(url)
    
    def nombre(self):
        if 'wikipedia' in self.enlace:
            nombre = self.enlace.split('/')[-1].split('#')[0].split('_')
            nombre = ' '.join(nombre[2:]) if 'Anexo' in self.enlace else ' '.join(nombre)
            nombre = nombre.split('(')[0][:-1] if '(' in nombre else nombre
            return nombre
    
    def scrapper(self):
        return BeautifulSoup(requests.get(self.enlace).text, 'html.parser')
    
    def wikipedia(self):

        soup=self.scrapper()
        resultado = {}

        ep1=False
        soup_temporadas = []
        for temporada in soup.find_all(class_='wikitable'):
            if temporada.find(class_='vevent'):
                comprobacion = temporada.find(class_='vevent').find('th') or temporada.find(class_='vevent').find('td')
                if comprobacion.has_attr('id'):
                    if comprobacion['id'] == "ep1" and not ep1:
                        ep1 = not ep1
                    elif (comprobacion['id'] == "ep1" and ep1) or (comprobacion['id'] != "ep1" and not ep1):
                        continue
                    soup_temporadas.append(temporada)

        for i, temporada in enumerate(soup_temporadas):
            resultado[i] = []
            soup_episodios = [episodio for episodio in temporada.find_all(class_='vevent') if (episodio.find('th') or episodio.find('td'))['id'][2:].isdigit()]
            for episodio in soup_episodios:
                nombre = episodio.find(class_='resumen') or episodio.find(class_='summary')
                nombre = nombre.text.split('»')[0].replace('«', '').replace('[l]', '')
                nombre = nombre.split('""')[0][1:] if '""' in nombre else nombre
                resultado[i] += [nombre[1:-1] if nombre[0] == '"' and nombre[-1]=='"' else nombre]
        
        return resultado
    
    # Resultado debe ser formato: "{1: [Episodio 1, Episodio 2, ...], 2: [Episodio 1, Episodio 2, ...], ... }"

    def seleccion(self):
        if 'wikipedia' in self.enlace:
            return self.wikipedia()
    
    def archivo(self):

        nombre = self.nombre()
        temporadas = self.seleccion()
        linias = []
        cifras_temporadas = len(str(len(temporadas)))
        for temporada, episodios in temporadas.items():
            cifras_episodios = len(str(len(episodios)))
            for j, episodio in enumerate(episodios):
                linias += [f'{str(temporada+1).zfill(cifras_temporadas)}x{str(j+1).zfill(cifras_episodios)} - {episodio}']

        with open (os.path.join(os.path.dirname(__file__), 'comprobar', f'{nombre}.txt'), 'w', encoding='utf-8') as w:
            w.write('\n'.join(linias))

for url in urls:
    Titulos_episodios(url).archivo()