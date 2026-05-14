def verify(offers: list[float], demands: list[float], matriz: list[list[float]]):

    
    if (len(matriz[0]) != len(demands) or len(matriz) != len(offers)):
        raise ValueError("El tamaño de la matriz de datos es distinto al tamaño de ofertas o demandas")
    
    if not all(len(fila) == len(matriz[0]) for fila in matriz):
        raise ValueError("El tamaño de la matriz es irregular")
    
    dem_total = sum(demands)
    off_total = sum(offers)

    if dem_total > off_total:
        offers.append(dem_total-off_total)
        matriz.append([0 for i in range(len(demands))])
    elif dem_total < off_total:
        demands.append(off_total-dem_total)
        for i in range(len(offers)):
            matriz[i].append(0)

if __name__ == "__main__":
    matriz = [[5,2,7,3],[3,6,6,1],[6,1,2,4], [4,3,6,6]]
    offers = [80,30,60,5]
    demands = [70,40,70,35]
    verify(offers,demands,matriz) 
    print(matriz) #Salida esperada [[5, 2, 7, 3], [3, 6, 6, 1], [6, 1, 2, 4], [4, 3, 6, 6], [0, 0, 0, 0]]
    print(offers) #Salida esperada [80, 30, 60, 5, 40]
    print(demands) #Salida esperada [70,40,70,35]