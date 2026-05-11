def minimun_cost(offers: list[float], demands: list[float], matriz: list[list[float]]):
    
    values = []
    cont = 0
    if (sum(offers) != sum(demands)):
        raise ValueError("La oferta total es distinta a la demanda total")
    
    while True:
        print_matriz(values,offers,demands, matriz, cont)
        if (offers == [] and demands == [0]) or (offers == [0] and demands == []):
            return sum(values)

        minimun = matriz[0][0] 
        x = 0
        y = 0
            
        for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                    
                if matriz[i][j] < minimun:
                    minimun = matriz[i][j]
                    x = i
                    y = j

        min_of_dem = demands[y] if demands[y] < offers[x] else offers[x]

        demands[y] = demands[y] - min_of_dem
        offers[x] = offers[x] - min_of_dem

        values.append(min_of_dem*minimun)

        if not demands[y]:
            demands.pop(y)
            for i in range(len(matriz)):
                matriz[i].pop(y)

        elif not offers[x]:
            offers.pop(x)
            matriz.pop(x)
        cont += 1

def print_matriz(values: list[float],offers: list[float], demands: list[float], matriz: list[list[float]], n: int):
    filas = len(matriz)
    columnas = len(matriz[0])
    text = ""

    if filas != 0 and columnas != 0:
        text += f"\nIteración: {n+1}\n"
        for i in range(columnas):
            code = chr(ord('A') + i)
            text += f'\t{code}'
        text += "\tOfertas \n"

        for i in range(filas):
            code = chr(ord('A') + i)
            text += f'{code}\t'

            for j in range(columnas):
                text += f"{matriz[i][j]}\t"
            text += f"{offers[i]}\n"

        text += "Dem\t"
        for i in range(columnas):
            text += f"{demands[i]}\t"
        text += "\n"
    else:
        text += "Valores para obtener el costo minimo: "
        for i in range(len(values)):
            text += f"{values[i]}  "
        text += "\n"
    print(text)

if __name__ == "__main__":
    matriz = [[5,2,7,3],[3,6,6,1],[6,1,2,4], [4,3,6,6]]
    offers = [80,30,60,45]
    demands = [70,40,70,35]
    try:
        mc = minimun_cost(offers,demands,matriz) #Salida esperada 780
        print("El costo minimo es: " + str(mc))
    except ValueError as ve:
        print(ve)