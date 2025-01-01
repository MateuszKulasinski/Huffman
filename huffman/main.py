class TreeNode:
    def __init__(self, value,czestotliwosc):
        self.value = value
        self.czestotliwosc = czestotliwosc
        self.left = None
        self.right = None
        self.numer = ""

    def add_children(self, left_value, lczest, right_value, rczest):
        self.left = TreeNode(left_value, lczest)
        self.right = TreeNode(right_value, rczest)


    def search(self, target):
        if self.value == target:
            return self

        if self.left:
            found = self.left.search(target)
            if found:
                return found

        if self.right:
            found = self.right.search(target)
            if found:
                return found

        return None

    def binarne(self,galaz,num):
        if galaz.left is not None:
            galaz.binarne(galaz.left, num + '0')
        if galaz.right is not None:
            galaz.binarne(galaz.right, num + '1')
        if galaz.right is None and galaz.left is None:
            galaz.numer = num

    def zapiszdotablicy(self,galaz,wynik):
        if galaz.left is not None:
            galaz.zapiszdotablicy(galaz.left, wynik)
        if galaz.right is not None:
            galaz.zapiszdotablicy(galaz.right, wynik)
        if galaz.right is None and galaz.left is None:
            x = [galaz.value, galaz.numer]
            wynik.append(x)



zapasowa =[]
def odczyt(nazwa):
    alfabet = {}
    with open("odczyt/" + nazwa + ".txt", "r", encoding="utf-8") as plik:
        zawartosc = plik.read()
        for znak in zawartosc:
            if znak not in alfabet:
                alfabet[znak] = 1
            else:
                alfabet[znak] += 1
    return alfabet


def buildheap(alf):
    i = (len(alf) // 2) - 1
    while i >= 0:
        heapify(alf, i, len(alf))
        i -= 1
    return alf


def heapify(alf, i, n):
    l = (2 * i) + 1
    r = (2 * i) + 2
    zamien = i

    if l < n and alf[l][1] < alf[zamien][1]:
        zamien = l


    if r < n and alf[r][1] < alf[zamien][1]:
        zamien = r

    if zamien != i:
        alf[i], alf[zamien] = alf[zamien], alf[i]
        heapify(alf, zamien, n)


def huffman(C):
    n = len(C)
    Q = C
    for i in range(1,n):
        freqleft = Q[0][1]
        left = Q[0][0]
        Q[0] = Q[-1]
        del Q[-1]

        heapify(Q, 0, len(Q))
        freqright = Q[0][1]
        right = Q[0][0]
        Q[0] = Q[-1]
        del Q[-1]
        z = [left+right, freqleft + freqright]
        Q.append(z)

        zapasowa.append([])
        zapasowa[i - 1].append(z)
        zapasowa[i - 1].append([left, freqleft])
        zapasowa[i - 1].append([right, freqright])

        heapify(Q, 0, len(Q))
    return Q[0]


def zbudujdrzewo():
    root = TreeNode(zapasowa[-1][0][0], zapasowa[-1][0][1])
    root.add_children(zapasowa[-1][1][0], zapasowa[-1][1][1], zapasowa[-1][2][0], zapasowa[-1][2][1])
    zapasowa.remove(zapasowa[-1])
    while zapasowa:
        i = 0
        while i < len(zapasowa):
            tab = zapasowa[i]
            galaz = root.search(tab[0][0])
            if galaz:
                root.search(tab[0][0]).add_children(tab[1][0], tab[1][1], tab[2][0], tab[2][1])
                zapasowa.remove(tab)
            else:
                i += 1
    root.binarne(root, '')
    wynik = []
    root.zapiszdotablicy(root, wynik)
    return wynik


def zaszyfruj(nazwa1,nazwa2,slownik):
    with open("zaszyfrowane/" + nazwa1 + ".txt", 'wb') as plik1:
        for litera in slownik:
            tekst = litera[0] + "= " + litera[1] + "  "
            plik1.write(tekst.encode('utf-8'))
        plik1.write(b"\n\nbcb\n\n")

    with open("zaszyfrowane/" + nazwa1 + ".txt", 'ab') as plik1:
        with open("odczyt/" + nazwa2 + ".txt", "r", encoding="utf-8") as plik2:
            zawartosc = plik2.read()
            wstaw = ''
            for znak in zawartosc:
                for tab in slownik:
                    if znak == tab[0]:
                        bity = tab[1]
                        for bit in bity:
                            if len(wstaw) < 8:
                                wstaw += bit
                            if len(wstaw) == 8:
                                bajt = int(wstaw, 2)
                                plik1.write(bytes([bajt]))
                                wstaw = ''
                        break
            if len(wstaw) < 8 and len(wstaw) != 0:
                licznik = 0
                while len(wstaw) < 8:
                    wstaw += '0'
                    licznik += 1
                bajt = int(wstaw, 2)
                plik1.write(bytes([bajt]))
                plik1.write(bytes([licznik]))





def odszyfruj(nazwa1, nazwa2):
    with open("zaszyfrowane/" + nazwa1 + ".txt", 'rb') as plik1:
        caly = plik1.read()
    podzielony = caly.split(b"\n\nbcb\n\n")
    linia = podzielony[0]
    tab = linia.split(b"  ")
    tab.pop()
    slownik = []
    for litera in tab:
        x = litera.split(b"= ")
        slownik.append([x[0].decode('utf-8'), x[1].decode('utf-8')])
        
    with open("zaszyfrowane/" + nazwa1 + ".txt", 'rb') as plik1:
        caly = plik1.read()
        podzielony = caly.split(b"\n\nbcb\n\n")
        linia = podzielony[1]
        przekonwertowane = ''.join(format(byte, '08b') for byte in linia)

        dousuniecia = przekonwertowane[-8:]
        usun = int(dousuniecia, 2) + 8
        przekonwertowane = przekonwertowane[:-usun]

        with open("odszyfrowane/" + nazwa2 + ".txt", 'w',  encoding='utf-8') as plik2:
            bity = ''
            for bit in przekonwertowane:
                bity += str(bit)
                for litera in slownik:
                    if bity == litera[1]:
                        plik2.write(litera[0])
                        bity = ''
                        break



def main():
    while True:
        print("Zaszyfrowanie wybierz 1, odszyfrowanie wybierz 2,wyjdz wybierz 3")
        wybor = int(input())
        if wybor == 1:
            print("Podaj nazwe pliku do zaszyfrowania (musi znajdowac sie w folderze odczyt)(bez dopisku txt):")
            nazwa1 = input()
            print("Podaj jak ma sie nazywac zaszyfrownay plik")
            nazwa2 = input()
            alf = odczyt(nazwa1)
            alfabet = list(alf.items())
            buildheap(alfabet)
            huffman(alfabet)
            slownik = zbudujdrzewo()
            zaszyfruj(nazwa2, nazwa1, slownik)
        elif wybor == 2:
            print("Podaj nazwe pliku do odszyfrowania (musi znajdowac sie w folderze zaszyfrowane)(bez dopisku txt):")
            nazwa1 = input()
            print("Podaj jak ma sie nazywac odszyfrowany plik(bedzie znajdował sie w folderze odszyfrowane")
            nazwa2 = input()
            odszyfruj(nazwa1, nazwa2)
        elif wybor == 3:
            exit()



if __name__ == '__main__':
    main()


