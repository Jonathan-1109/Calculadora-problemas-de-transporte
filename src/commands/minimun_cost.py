from .transport import transport
from .groq_conclusion import groq_conclusion

class minimun_cost(transport):

    def __init__(self, matriz, offers, demands):
        super().__init__(matriz, offers, demands)
        
    def resolve_minimun_cost(self):
        cont = 0
        
        while True:

            minimun = self.matriz[0][0] 
            x = 0
            y = 0
                
            for i in range(len(self.matriz)):
                for j in range(len(self.matriz[0])):
                        
                    if self.matriz[i][j] < minimun:
                        minimun = self.matriz[i][j]
                        y = i
                        x = j

            min_of_dem = self.demands[x] if self.demands[x] < self.offers[y] else self.offers[y]
            self.print_matriz(min_of_dem, minimun, cont)
            self.values.append(min_of_dem*minimun)

            self.demands[x] = self.demands[x] - min_of_dem
            self.offers[y] = self.offers[y] - min_of_dem

            if (self.demands == [0] and self.offers == [0]):
                text = "\nValores para obtener el costo minimo: "
                for i in range(len(self.values)):
                    text += f"{self.values[i]}  "
                print(text)

                self.result = sum(self.values)
                print("\nEl costo minimo es: " + str(self.result) + "\n")
                return
            
            if not self.demands[x]:
                self.demands.pop(x)
                for i in range(len(self.matriz)):
                    self.matriz[i].pop(x)

            elif not self.offers[y]:
                self.offers.pop(y)
                self.matriz.pop(y)
            cont += 1

    def groq_promt(self):
        content = f"""
        Genera una conclusión para este problema de transporte del método de costo mínimo donde la matriz es: {self.clone_matriz}, las ofertas: {self.clone_offers},
        las demandas: {self.clone_demands} y que dio como resultado: {self.result}, 
        a partir de la suma de todos los valores de esta esta lista de valores: {self.values}"""
        
        groq_conclusion(self.client, content)