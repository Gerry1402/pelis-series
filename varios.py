import os
from directorios import *
from itertools import islice

def dividir_lista(lista, tamaño):
    """Divide una lista usando iteradores."""
    iterador = iter(lista)
    return [list(islice(iterador, tamaño)) for _ in range(0, len(lista), tamaño)]

def lista_carpetas(carpeta):
    return [elemento for elemento in os.listdir(carpeta) if os.path.isdir(os.path.join(carpeta, elemento))]

def lista_archivos(carpeta, extension:str=None):
    lista = [] if extension else {}
    for elemento in os.listdir(carpeta):
        if os.path.isfile(os.path.join(carpeta, elemento)):
            nombre, ext = os.path.splitext(elemento)
            if extension:
                lista.append(nombre) if extension == ext else None
            elif nombre in lista:
                lista[nombre] += [ext]
            else:
                lista[nombre] = [ext]
    return sorted(lista) if extension else lista

def renombrar_elementos(carpeta, english=True):

    lower=['A','Aboard', 'About', 'Above', 'Across', 'After', 'Against', 'Along', 'Amid', 'Among', 'Anti', 'Around', 'As', 'At', 'Before', 'Behind', 'Below', 'Beneath', 'Beside', 'Besides', 'Between', 'Beyond', 'But', 'By', 'Concerning', 'Considering', 'Despite', 'Down', 'During', 'Except', 'Excepting', 'Excluding', 'Following', 'For', 'From', 'In', 'Inside', 'Into', 'Like', 'Minus', 'Near', 'Of', 'Off', 'On', 'Onto', 'Opposite', 'Outside', 'Over', 'Past', 'Per', 'Plus', 'Regarding', 'Round', 'Save', 'Since', 'Than', 'Through', 'To', 'Toward', 'Towards', 'Under', 'Underneath', 'Unlike', 'Until', 'Up', 'Upon', 'Versus', 'Via', 'With', 'Within', 'Without','The','And']
    minus = ['A', 'Amb', 'Ante', 'Contra', 'Des', 'De', 'En', 'Entre', 'Fins', 'Per', 'Sobre', 'Sota', 'Davant', 'Darrere', 'El', 'La', 'Els', 'Les', 'Un', 'Una', 'Uns', 'Unes', 'I','O', 'Però', 'Sinò', 'També', 'Ni', 'Que', 'Si', 'Com', 'Quan', 'On', 'Perquè', 'Ja', 'Com', 'Jo', 'Tu', 'Ell', 'Ella', 'Vostè', 'Nosaltres', 'Vosaltres', 'Ells', 'Elles', 'Vostès', 'Meu', 'Meva', 'Teus', 'Teva', 'Seu', 'Seva', 'Nostre', 'Nostra', 'Vostre', 'Vostra', 'Aquest', 'Aquesta', 'Aquests', 'Aquestes', 'Aquell', 'Aquella', 'Aquells', 'Aquelles', 'Algú', 'Ningú', 'Res', 'Tot', 'Alguns', 'Moltes', 'Pocs', 'Altres']
    
    total=set(lower+minus)

    lista = lista_archivos(carpeta)

    for elemento in lista:
        nombre = elemento
        nombre=nombre.title().split(' - ')
        for i in range (len(nombre)):
            palabras=nombre[i].split()
            for j in range (1, len(palabras)) if len(palabras)>1 else [0]:
                separaciones=palabras[j].split('-')
                for k in range(len(separaciones)) if len(separaciones)>1 else [0]:
                    separaciones[k] = separaciones[k].lower() if separaciones[k] in total else separaciones[k]
                    separaciones[k] = f"{separaciones[k][:-2]}'{separaciones[k][-1].lower()}" if separaciones[k][-2] == "'" else separaciones[k]
                    separaciones[k] = f"{separaciones[k][0].lower()}'{separaciones[k][2:]}" if separaciones[k][1] == "'" else separaciones[k]
                    #separaciones[k] = "RM" if separaciones[k] == "Rm" else separaciones[k] = "RM"
                palabras[j]='-'.join(separaciones)
            nombre[i]=' '.join(palabras)
        nombre=' - '.join(nombre)

        nombre = nombre.replace(' i ', ' I ') if english else nombre

        direccion_elemento = os.path.join(carpeta, elemento)
        direccion_nombre = os.path.join(carpeta, nombre)

        for extension in lista[elemento]:
            os.rename(direccion_elemento+extension, direccion_nombre+extension)

def no_existen(ruta_1, ruta_2):
    lista_1 = [nombre.lower() for nombre in lista_archivos(ruta_1).keys()]
    lista_2 = [nombre.lower() for nombre in lista_archivos(ruta_2).keys()]
    return sorted(set(lista_1) ^ set(lista_2))

def mayus_minus(ruta_1, ruta_2):
    diferencias = {
        nombre.lower() for nombre in lista_archivos(ruta_1).keys()^lista_archivos(ruta_2).keys()
    }
    return sorted(diferencias - set(no_existen(ruta_1, ruta_2)))