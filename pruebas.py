import os

def renombrar_caratulas_pelis(path):

    lower=['A','Aboard', 'About', 'Above', 'Across', 'After', 'Against', 'Along', 'Amid', 'Among', 'Anti', 'Around', 'As', 'At', 'Before', 'Behind', 'Below', 'Beneath', 'Beside', 'Besides', 'Between', 'Beyond', 'But', 'By', 'Concerning', 'Considering', 'Despite', 'Down', 'During', 'Except', 'Excepting', 'Excluding', 'Following', 'For', 'From', 'In', 'Inside', 'Into', 'Like', 'Minus', 'Near', 'Of', 'Off', 'On', 'Onto', 'Opposite', 'Outside', 'Over', 'Past', 'Per', 'Plus', 'Regarding', 'Round', 'Save', 'Since', 'Than', 'Through', 'To', 'Toward', 'Towards', 'Under', 'Underneath', 'Unlike', 'Until', 'Up', 'Upon', 'Versus', 'Via', 'With', 'Within', 'Without','The','And']
    minus = ['A', 'Amb', 'Ante', 'Contra', 'Des', 'De', 'En', 'Entre', 'Fins', 'Per', 'Sobre', 'Sota', 'Davant', 'Darrere', 'El', 'La', 'Els', 'Les', 'Un', 'Una', 'Uns', 'Unes', 'I', 'O', 'Però', 'Sinò', 'També', 'Ni', 'Que', 'Si', 'Com', 'Quan', 'On', 'Perquè', 'Ja', 'Com', 'Jo', 'Tu', 'Ell', 'Ella', 'Vostè', 'Nosaltres', 'Vosaltres', 'Ells', 'Elles', 'Vostès', 'Meu', 'Meva', 'Teus', 'Teva', 'Seu', 'Seva', 'Nostre', 'Nostra', 'Vostre', 'Vostra', 'Aquest', 'Aquesta', 'Aquests', 'Aquestes', 'Aquell', 'Aquella', 'Aquells', 'Aquelles', 'Algú', 'Ningú', 'Res', 'Tot', 'Alguns', 'Moltes', 'Pocs', 'Altres']
    
    total=set(lower+minus)
    
    renombradas=[]

    os.chdir(path)

    for elemento in os.listdir():
        nombre = elemento
        if os.path.isfile(elemento):
            nombre, extension = os.path.splitext(nombre)
        
        if len(nombre.split()) == 1:
            continue

        nombre=nombre.title().split(' - ')
        for i in range (len(nombre)):
            palabras=nombre[i].split()
            for j in range (1, len(palabras)) if len(palabras)>1 else [0]:
                separaciones=palabras[j].split('-')
                for k in range(len(separaciones)) if len(separaciones)>1 else [0]:
                    if separaciones[k] in total:
                        separaciones[k]=separaciones[k].lower()
                    if separaciones[k][-2]=="'":
                        separaciones[k]=f"{separaciones[k][:-2]}'{separaciones[k][-1]}"
                    if separaciones[k][1]=="'":
                        separaciones[k]=f"{separaciones[k][0]}'{separaciones[k][2:]}"
                    if separaciones[k]=="Rm":
                        separaciones[k]="RM"
                palabras[j]='-'.join(separaciones)
            nombre[i]=' '.join(palabras)
        nombre=' - '.join(nombre)

        os.rename(elemento, f'{nombre}{extension}' if os.path.isfile(elemento) else nombre)

    return renombradas
