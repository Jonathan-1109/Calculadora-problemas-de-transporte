from os import getenv
from groq import Groq
from .verify import verify

class transport:

    def __init__(self, matriz, offers, demands):
        groqKey = getenv("GROQ_API_KEY","groqKey")
        self.client = Groq(api_key=groqKey)

        self.matriz = matriz
        self.offers = offers
        self.demands = demands
        self.clone_matriz = [fila[:] for fila in matriz]
        self.clone_offers = offers[:]
        self.clone_demands = demands[:]
        verify(self.offers, self.demands, self.matriz)

        self.values = []
        self.result = 0

    def print_matriz(self, value1:float, value2: float,n:int):
        filas = len(self.matriz)
        columnas = len(self.matriz[0])

        text = f"\nIteración: {n+1}\n"
        for i in range(columnas):
            code = chr(ord('A') + i)
            text += f'\t{code}'
        text += "\tOfertas \n"

        for i in range(filas):
            code = chr(ord('A') + i)
            text += f'{code}\t'

            for j in range(columnas):
                text += f"{self.matriz[i][j]}\t"
            text += f"{self.offers[i]}\n"

        text += "Dem\t"
        for i in range(columnas):
            text += f"{self.demands[i]}\t"
        text += f"\nValores a multiplicar: {value1} * {value2}"
        print(text)

    def groq_promt(self):
        pass

