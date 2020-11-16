import array
import numpy as np

pole = [
1,8,0,0,0,9,6,0,0,
9,0,6,0,0,0,5,2,0,
0,0,0,2,0,6,0,8,9,
0,0,0,8,0,0,9,0,1,
3,0,0,0,0,4,0,0,5,
0,9,7,0,5,1,2,0,0,
7,0,0,1,9,0,0,0,6,
0,0,0,0,0,0,4,0,2,
2,0,0,0,0,5,3,1,7
]

class Konec(Exception): pass

def xy_to_number(x, y):
    return pole[(9*(8-y)+x)] #x zleva doprava a y odspoda nahoru

def xy_to_location(x, y):
    return (9*(8-y)+x) #x zleva doprava a y odspoda nahoru

def is_in_my_line(x, y, number):
    for sloupce in range(9): #checkne osu y
        if(sloupce != y): #aby to neregistrovalo samo sebe
            if (xy_to_number(x, sloupce) == number):
                return True #toto cislo nepasuje na misto kam ho chceme dat
    for radky in range(9): #checkne osu x
        if(radky != x): #aby to neregistrovalo samo sebe
            if (xy_to_number(radky, y) == number):
                return True
    return False #toto cislo pasuje na misto kam ho chceme dat

def my_square(puvodx, puvody, number):
    if (puvodx/3 < 1):
        square_x = 0
    elif (puvodx/3 >= 2):
        square_x = 2
    else: square_x = 1

    if (puvody/3 < 1):
        square_y = 0
    elif (puvody/3 >= 2):
        square_y = 2
    else: square_y = 1

    for x in range(3*square_x, 3*square_x+3):
        for y in range(3*square_y, 3*square_y+3):
            if(xy_to_number(x, y) == number):
                return True #toto cislo nepasuje na misto kam ho chceme dat
    return False #toto cislo pasuje na misto kam ho chceme dat

#musime vytvorit pole s dostupnymi cisly pro kazde prazdne policko v sudoku

def vytvorit_moznosti(array):
    moznosti = []
    vsechnymoznosti = [1,2,3,4,5,6,7,8,9]
    for x in range(len(array)):
        if array[x] == 0:
            moznosti.append(vsechnymoznosti)
        else:
            moznosti.append(array[x])
    return moznosti

def odstran(cislo, array):
    custom_array = array
    if(isinstance(custom_array, list)):
        for i in range(len(custom_array)):
            if len(custom_array) == 0:
                return 0
            if custom_array[i] == cislo:
                index = [i]
                custom_array = np.delete(custom_array, index)
                return list(custom_array)
    return list(array)

def muze_existovat(moznosti):
    custom_array = moznosti
    for i in range(len(custom_array)):
        if custom_array[i] == 0:
            return False
    return True

def check(pole):
    counter = 0
    for i in range(len(pole)):
        if(pole[i] == 0):
            counter = counter + 1
    return counter

def check_duplicates(array):
    if len(array) == len(set(array)):
        return False
    else:
        return True

def check_lines(array):
    cisla_v_radku = []
    pocet_cisel_v_rade = 9
    for line in range(81):
        if array[line] != 0 and len(cisla_v_radku) != pocet_cisel_v_rade:
            cisla_v_radku.append(array[line])
        elif array[line] == 0 and len(cisla_v_radku) != pocet_cisel_v_rade:
            pocet_cisel_v_rade = pocet_cisel_v_rade - 1
        if len(cisla_v_radku) == pocet_cisel_v_rade:
            #print(cisla_v_radku)
            if check_duplicates(cisla_v_radku) == True:
                return False #TOHLE POLE JE SPATNE
            pocet_cisel_v_rade = 9
            cisla_v_radku = []
    return True #TOHLE POLE JE SPRAVNE

def check_rows(array):
    cisla_v_sloupci = []
    pocet_cisel_v_sloupci = 9
    for line in range(9):
        for row in range(9):
            if array[9*row+line] != 0 and len(cisla_v_sloupci) != pocet_cisel_v_sloupci:
                cisla_v_sloupci.append(array[9*row+line])
            elif array[9*row+line] == 0 and len(cisla_v_sloupci) != pocet_cisel_v_sloupci:
                pocet_cisel_v_sloupci = pocet_cisel_v_sloupci - 1
            if len(cisla_v_sloupci) == pocet_cisel_v_sloupci:
                #print(cisla_v_sloupci)
                if check_duplicates(cisla_v_sloupci) == True:
                    return False #TOHLE POLE JE SPATNE
                pocet_cisel_v_sloupci = 9
                cisla_v_sloupci = []
    return True #TOHLE POLE JE SPRAVNE

def check_squares(array):
    #square x -> 0 - 2
    #square y -> 0 - 2
    cisla_v_sloupci = []
    pocet_cisel_v_sloupci = 9
    for y in range(3):
        for x in range(3):
            for a in range(3):
                for b in range(3):
                    if array[xy_to_location(a + x*3, b + y*3)] != 0 and len(cisla_v_sloupci) != pocet_cisel_v_sloupci:
                        cisla_v_sloupci.append(array[xy_to_location(a + x*3, b + y*3)])
                    elif array[xy_to_location(a + x*3, b + y*3)] == 0 and len(cisla_v_sloupci) != pocet_cisel_v_sloupci:
                        pocet_cisel_v_sloupci = pocet_cisel_v_sloupci - 1
                    if len(cisla_v_sloupci) == pocet_cisel_v_sloupci:
                        #print(cisla_v_sloupci)
                        if check_duplicates(cisla_v_sloupci) == True:
                            return False #TOHLE POLE JE SPATNE
                        pocet_cisel_v_sloupci = 9
                        cisla_v_sloupci = []
    return True #TOHLE POLE JE SPRAVNE

#CHECK IF THE SUDOKU ARRAY DOESN´T BREAK ANY RULES
def check2(array):
    if check_rows(array) == True and check_lines(array) == True and check_squares(array) == True: return True
    return False

moznosti = vytvorit_moznosti(pole)

#DELETE ALL FALSE OPTIONS FOR INDIVIDUAL BOXES
def odstraneni_moznosti(moznosti):
    for a in range(9):
        for b in range(9):
            for c in range(10):
                if(xy_to_number(a, b) == 0):
                    if(is_in_my_line(a,b,c) == True):
                        pozice = xy_to_location(a, b)
                        moznosti[pozice] = odstran(c, moznosti[pozice])
                    elif(my_square(a,b,c) == True):
                        pozice = xy_to_location(a, b)
                        moznosti[pozice] = odstran(c, moznosti[pozice])
    return moznosti

def vykresleni_do_pole(moznosti, pole):
    for a in range(81):
        if(isinstance(moznosti[a], list) == True):
            if(len(moznosti[a]) == 1): 
                styl = moznosti[a]
                pole[a] = styl[0]
    return pole

def vynulovani(array, moje_pozice):
    for a in range(len(backtracking_moznosti)):
        if a >= moje_pozice - 1:
            array[a] = backup_pole[a]
            vybrane_moznosti[a] = 0
        else:
            print(array[a])
    return array

predchozi_vysledek = 0

while(check(pole) > 1):
    if predchozi_vysledek == check(pole):
        break
    predchozi_vysledek = check(pole)
    moznosti = odstraneni_moznosti(moznosti)
    pole = vykresleni_do_pole(moznosti, pole)
    print(pole)
    print(moznosti)
    print("Jeste musim vyresit: " + str(check(pole)) + " policek")

if check(pole) == 0: print(pole) #done
else: #backtracking
    print("JESTE NENI HOTOVO -> backtracking")
    backtracking_pole = pole
    backup_pole = pole
    backtracking_moznosti = []
    poloha_backtracking_moznosti = []
    vybrane_moznosti = []
    moje_pozice = 0
    for i in range(len(moznosti)):
        if(isinstance(moznosti[i], list) and len(moznosti[i]) > 1):
            backtracking_moznosti.append(moznosti[i])

    for i in range(len(backtracking_moznosti)):
        backtracking_moznosti[i] = [0] + backtracking_moznosti[i]
        vybrane_moznosti.append(0)
            
    for i in range(len(pole)):
        if(pole[i] == 0):
            poloha_backtracking_moznosti.append(i)

    def backtracking(moje_pozice):
        print(backtracking_pole)
        if check2(backtracking_pole) == False:
            if vybrane_moznosti[moje_pozice] < len(backtracking_moznosti[moje_pozice]) - 1:
                #print("ZVEDAM O JEDNICKU")
                vybrane_moznosti[moje_pozice] += 1
                backtracking_pole[poloha_backtracking_moznosti[moje_pozice]] = backtracking_moznosti[moje_pozice][vybrane_moznosti[moje_pozice]]
            elif vybrane_moznosti[moje_pozice] == len(backtracking_moznosti[moje_pozice]) - 1:
                #print("VYNULOVAT A ZVEDAM PREDCHOZI POLE O JEDNICKU")
                backtracking_pole[poloha_backtracking_moznosti[moje_pozice]] = 0
                vybrane_moznosti[moje_pozice] = 0
                backtracking_pole[poloha_backtracking_moznosti[moje_pozice]] = backtracking_moznosti[moje_pozice][vybrane_moznosti[moje_pozice]]
                moje_pozice -= 1
                vynulovano = False
                while(vynulovano == False):
                    if vybrane_moznosti[moje_pozice] < len(backtracking_moznosti[moje_pozice]) - 1:
                        vybrane_moznosti[moje_pozice] += 1
                        backtracking_pole[poloha_backtracking_moznosti[moje_pozice]] = backtracking_moznosti[moje_pozice][vybrane_moznosti[moje_pozice]]
                        vynulovano = True
                    else:
                        vybrane_moznosti[moje_pozice] = 0
                        backtracking_pole[poloha_backtracking_moznosti[moje_pozice]] = backtracking_moznosti[moje_pozice][vybrane_moznosti[moje_pozice]]
                        moje_pozice -= 1
            return moje_pozice
        else:
            if vybrane_moznosti[moje_pozice] == 0:
                #print("ZVEDAM O JEDNICKU")
                vybrane_moznosti[moje_pozice] += 1
                backtracking_pole[poloha_backtracking_moznosti[moje_pozice]] = backtracking_moznosti[moje_pozice][vybrane_moznosti[moje_pozice]]
            else:
                #print("POSOUVAM O JEDNO POLE DOPREDU")
                if moje_pozice < len(vybrane_moznosti) - 1:
                    moje_pozice += 1
                    vybrane_moznosti[moje_pozice] += 1
                    backtracking_pole[poloha_backtracking_moznosti[moje_pozice]] = backtracking_moznosti[moje_pozice][vybrane_moznosti[moje_pozice]]
                else:
                    print("KONEC")
                    raise Konec
        return moje_pozice

    print("\n")
    print("BACKTRACKING POLE:")
    print(backtracking_pole)
    print("\n")
    print("POLOHA MOZNOSTI:")
    print(poloha_backtracking_moznosti)
    print("\n")
    print("BACKTRACKING MOZNOSTI:")
    print(backtracking_moznosti)
    print("\n")
    print("VYBRANE MOZNOSTI:")
    print(vybrane_moznosti)

    try:
        while True:
            backup_pole = backtracking_pole
            moje_pozice = backtracking(moje_pozice)
    except Konec:
        pass

    print(backtracking_pole)