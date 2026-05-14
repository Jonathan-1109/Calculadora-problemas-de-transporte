from .transport import transport
from .groq_conclusion import groq_conclusion

class vogel_approximation(transport):

    def __init__(self, matriz, offers, demands):
        super().__init__(matriz, offers, demands)

    def resolve_vogel(self):
        cont = 0

        while True:
            # Calcular penalizaciones de filas
            row_penalties = []
            for row in self.matriz:
                if len(row) >= 2:
                    sorted_row = sorted(row)
                    row_penalties.append(sorted_row[1] - sorted_row[0])
                elif len(row) == 1:
                    row_penalties.append(row[0])
                else:
                    row_penalties.append(-1)

            # Calcular penalizaciones de columnas
            col_penalties = []
            if len(self.matriz) > 0:
                for j in range(len(self.matriz[0])):
                    col = [self.matriz[i][j] for i in range(len(self.matriz))]
                    if len(col) >= 2:
                        sorted_col = sorted(col)
                        col_penalties.append(sorted_col[1] - sorted_col[0])
                    elif len(col) == 1:
                        col_penalties.append(col[0])
                    else:
                        col_penalties.append(-1)
            else:
                col_penalties = []

            # Encontrar la penalización máxima
            max_row_pen = max(row_penalties) if row_penalties else -1
            max_col_pen = max(col_penalties) if col_penalties else -1

            y = -1 # índice de fila
            x = -1 # índice de columna

            if max_row_pen >= max_col_pen and max_row_pen != -1:
                y = row_penalties.index(max_row_pen)
                minimun = min(self.matriz[y])
                x = self.matriz[y].index(minimun)
            else:
                if max_col_pen != -1:
                    x = col_penalties.index(max_col_pen)
                    col = [self.matriz[i][x] for i in range(len(self.matriz))]
                    minimun = min(col)
                    y = col.index(minimun)
                else:
                    break

            min_of_dem = self.demands[x] if self.demands[x] < self.offers[y] else self.offers[y]
            self.print_matriz(min_of_dem, minimun, cont, row_penalties, col_penalties)
            self.values.append(min_of_dem * minimun)

            self.demands[x] = self.demands[x] - min_of_dem
            self.offers[y] = self.offers[y] - min_of_dem

            if (self.demands == [0] and self.offers == [0]) or (len(self.demands) == 0 and len(self.offers) == 0):
                text = "\nValores para obtener el costo mínimo (Vogel): "
                for i in range(len(self.values)):
                    text += f"{self.values[i]}  "
                print(text)

                self.result = sum(self.values)
                print("\nEl costo mínimo es: " + str(self.result) + "\n")
                return

            if not self.demands[x]:
                self.demands.pop(x)
                for i in range(len(self.matriz)):
                    self.matriz[i].pop(x)
            if not self.offers[y]:
                self.offers.pop(y)
                self.matriz.pop(y)
                
            cont += 1

    def print_matriz(self, value1, value2, n, row_penalties, colt_penalties):
        super().print_matriz(value1, value2, n)
        text = f"\nPenalizaciones de la fila: "
        for value in row_penalties:
            text += f"{value} "
        text += f"\nPenalizaciones de la columna: "
        for value in colt_penalties:
            text += f"{value} "
        print(text)
        self.log_iteraciones.append(text)


    def groq_promt(self):
        suma_ofertas = sum(self.clone_offers)
        suma_demandas = sum(self.clone_demands)
        balanceado = suma_ofertas == suma_demandas

        asignaciones_str = ", ".join(str(v) for v in self.values)

        user_content = f"""Analiza el siguiente problema de transporte resuelto por el **Método de Aproximación de Vogel** y proporciona una conclusión académica estructurada.

DATOS DEL PROBLEMA:
- Método utilizado: Aproximación de Vogel
- Matriz de costos (filas=orígenes, columnas=destinos): {self.clone_matriz}
- Ofertas por origen: {self.clone_offers}  (suma total: {suma_ofertas})
- Demandas por destino: {self.clone_demands}  (suma total: {suma_demandas})
- Problema balanceado: {'Sí' if balanceado else 'No (se agregó variable ficticia con costo 0)'}
- Número de iteraciones realizadas: {len(self.values)}

RESULTADO OBTENIDO:
- Valores de asignación individuales (unidades × costo unitario): [{asignaciones_str}]
- Costo total obtenido: {self.result}

Por favor, estructura tu respuesta con estas secciones (máximo 200 palabras en total):
1. **Resumen del procedimiento**: Describe brevemente cómo funciona la Aproximación de Vogel y cómo se aplicó.
2. **Interpretación del resultado**: Explica qué significa el costo total de {self.result} en el contexto del problema.
3. **Calidad de la solución**: Indica si esta es una solución óptima o una excelente aproximación inicial.
4. **Observaciones adicionales**: Menciona si el problema estaba balanceado y cualquier aspecto relevante."""

        print("\nGenerando conclusión con IA...")
        conclusion = groq_conclusion(self.client, user_content)

        if conclusion:
            print("\nConclusión:\n")
            print(conclusion)
        else:
            print("\nNo se pudo obtener conclusión de la IA.")

        return conclusion