from .transport import transport
from .groq_conclusion import groq_conclusion

class nortwest_corner(transport):

    def __init__(self, matriz, offers, demands):
        super().__init__()
        self.create(matriz, offers, demands)

    def resolve_nortwest(self):
        cont = 0
        while True:

            if not (self.offers and self.demands):
                self.result = sum(self.values)
                print(f"El resultado por esquina noroeste es: {self.result}")
                return
            
            self.print_matriz(cont)
  
            min_of_dem = self.offers[0] if self.offers[0] < self.demands[0] else self.demands[0]
            self.values.append(min_of_dem*self.matriz[0][0])
            self.offers[0] = self.offers[0] - min_of_dem
            self.demands[0] =  self.demands[0] - min_of_dem

            if not self.demands[0]:
                self.demands.pop(0)
                for i in range(len(self.matriz)):
                    self.matriz[i].pop(0)
            
            if not self.offers[0]:
                self.offers.pop(0)
                self.matriz.pop(0)

            cont += 1

    def groq_promt(self):
        content = f"""
        Genera una conclusión para este problema de transporte del método de esquina noroeste donde la matriz es: {self.clone_matriz}, las ofertas: {self.clone_offers},
        las demandas: {self.clone_demands} y que dio como resultado: {self.result}, 
        a partir de la suma de todos los valores de esta esta lista de valores: {self.values}"""
        
        groq_conclusion(self.client, content)
