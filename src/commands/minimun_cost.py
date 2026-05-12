from .transport import transport
from .groq_conclusion import groq_conclusion

class minimun_cost(transport):

    def __init__(self, matriz, offers, demands):
        super().__init__()
        self.create(matriz, offers, demands)
        
    def resolve_minimun_cost(self):
        cont = 0
        
        while True:
            self.print_matriz(cont)

            minimun = self.matriz[0][0] 
            x = 0
            y = 0
                
            for i in range(len(self.matriz)):
                for j in range(len(self.matriz[0])):
                        
                    if self.matriz[i][j] < minimun:
                        minimun = self.matriz[i][j]
                        x = i
                        y = j

            min_of_dem = self.demands[y] if self.demands[y] < self.offers[x] else self.offers[x]
            self.demands[y] = self.demands[y] - min_of_dem
            self.offers[x] = self.offers[x] - min_of_dem
            self.values.append(min_of_dem*minimun)

            if (self.demands == [0] and self.offers == [0]):
                text = "\nValores para obtener el costo minimo: "
                for i in range(len(self.values)):
                    text += f"{self.values[i]}  "
                print(text)

                self.result = sum(self.values)
                return
            
            if not self.demands[y]:
                self.demands.pop(y)
                for i in range(len(self.matriz)):
                    self.matriz[i].pop(y)

            elif not self.offers[x]:
                self.offers.pop(x)
                self.matriz.pop(x)
            cont += 1

    def groq_promt(self):
        content = f"""
        Genera una conclusión para este problema de transporte del método de costo mínimo donde la matriz es: {self.clone_matriz}, las ofertas: {self.clone_offers},
        las demandas: {self.clone_demands} y que dio como resultado: {self.result}, 
        a partir de la suma de todos los valores de esta esta lista de valores: {self.values}"""
        
        groq_conclusion(self.client, content)