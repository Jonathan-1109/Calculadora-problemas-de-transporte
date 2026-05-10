class ejercicio:

    def __init__(self):
        self.oferta = []
        self.demanda = []
        self.matriz =  []
        self.valores = []
    
    def create(self):
        filas = int(input("Inserta el numero de filas: "))
        columnas = int(input("Inserta el numero de columnas: "))
        self.matriz = [[0] * columnas for i in range(filas)]
        self.demanda = [0 for i in range(columnas)]
        self.oferta =  [0 for i in range(filas)]

        for i in range(filas):
            for j in range(columnas):
                self.matriz[i][j] = int(input("Inserta el valor fila: " + str(i+1) + " columna: " + str(j+1) + ": "))

        for i in range(columnas):
            self.demanda[i] = int(input("Inserta el valor de la demanda columna: " + str(i+1) + ": "))

        for i in range(filas):
            self.oferta[i] = int(input("Inserta el valor de la oferta fila: " + str(i+1) + ": "))

        demanda_total = sum(self.demanda)
        oferta_total = sum(self.oferta)

        if demanda_total > oferta_total:
            self.oferta.append(demanda_total-oferta_total)
            self.matriz.append([0 for i in range(columnas)])
        elif demanda_total < oferta_total:
            self.demanda.append(oferta_total-demanda_total)
            for i in range(filas):
                self.matriz[i].append(0)

    def costo_minimmo(self):
        while True:
            print(self.matriz)
            if (self.oferta == [] and self.demanda == [0]) or (self.oferta == [0] and self.demanda == []):
                print("El costo minimo es: " + str(sum(self.valores)))
                break
            minimo = self.matriz[0][0] 
            x = 0
            y = 0
            
            for i in range(len(self.matriz)):
                for j in range(len(self.matriz[0])):
                    
                    if self.matriz[i][j] < minimo:
                        minimo = self.matriz[i][j]
                        x = i
                        y = j
            if self.demanda[y] < self.oferta[x]:
                min_of_dem = self.demanda[y]
            else:
                min_of_dem = self.oferta[x]

            self.demanda[y] = self.demanda[y] - min_of_dem
            self.oferta[x] = self.oferta[x] - min_of_dem
            self.valores.append(min_of_dem*minimo)

            if self.demanda[y] == 0:
                self.demanda.pop(y)
                for i in range(len(self.matriz)):
                    self.matriz[i].pop(y)
            elif self.oferta[x] == 0:
                self.oferta.pop(x)
                self.matriz.pop(x)

if __name__ == "__main__":
    ex = ejercicio()
    ex.create()
    ex.costo_minimmo()