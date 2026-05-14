import os
from datetime import datetime
from os import getenv
from groq import Groq
from .verify import verify

class transport:

    def __init__(self, matriz, offers, demands):
        groqKey = getenv("GROQ_API_KEY", "")
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
        self.log_iteraciones: list[str] = []

    def print_matriz(self, value1: float, value2: float, n: int):
        filas = len(self.matriz)
        columnas = len(self.matriz[0])

        text = f"\nIteración: {n + 1}\n"
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
        self.log_iteraciones.append(text)

    def save_result_to_txt(self, method_name: str, conclusion: str | None):
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "resultados")
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(output_dir, f"resultado_{method_name}_{timestamp}.txt")

        matriz_str = "\n".join(
            f"  {row}" for row in self.clone_matriz
        )
        valores_str = "  " + "  |  ".join(str(v) for v in self.values)

        sep = "=" * 60

        lines = [
            sep,
            "   CALCULADORA DE PROBLEMAS DE TRANSPORTE",
            f"   Método: {method_name}",
            f"   Fecha:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            sep,
            "",
            "DATOS DE ENTRADA",
            "-" * 40,
            "Matriz de costos (filas=orígenes, columnas=destinos):",
            matriz_str,
            f"Ofertas:   {self.clone_offers}",
            f"Demandas:  {self.clone_demands}",
            f"Suma ofertas:  {sum(self.clone_offers)}",
            f"Suma demandas: {sum(self.clone_demands)}",
            f"Balanceado:    {'Sí' if sum(self.clone_offers) == sum(self.clone_demands) else 'No (se añadió variable ficticia)'}",
            "",
            "PROCESO DE RESOLUCIÓN",
            "-" * 40,
            *self.log_iteraciones,
            "",
            "RESULTADO FINAL",
            "-" * 40,
            f"Valores de asignación (unidades × costo):",
            valores_str,
            f"Costo total obtenido: {self.result}",
            "",
            "CONCLUSIÓN (generada por IA - Groq / llama-3.3-70b-versatile)",
            "-" * 40,
            conclusion if conclusion else "[Sin conclusión]",
            "",
            sep,
        ]

        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"\nResultado guardado en: {filename}")
        return filename

    def groq_promt(self):
        pass
