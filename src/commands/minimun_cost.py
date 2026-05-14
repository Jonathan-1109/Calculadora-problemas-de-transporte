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
            self.values.append(min_of_dem * minimun)

            self.demands[x] = self.demands[x] - min_of_dem
            self.offers[y] = self.offers[y] - min_of_dem

            if (self.demands == [0] and self.offers == [0]):
                text = "\nValores para obtener el costo mínimo: "
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

    def groq_promt(self):
        suma_ofertas = sum(self.clone_offers)
        suma_demandas = sum(self.clone_demands)
        balanceado = suma_ofertas == suma_demandas

        asignaciones_str = ", ".join(str(v) for v in self.values)

        user_content = f"""Analiza el siguiente problema de transporte resuelto por el **Método de Costo Mínimo** y proporciona una conclusión académica estructurada.

DATOS DEL PROBLEMA:
- Método utilizado: Costo Mínimo
- Matriz de costos (filas=orígenes, columnas=destinos): {self.clone_matriz}
- Ofertas por origen: {self.clone_offers}  (suma total: {suma_ofertas})
- Demandas por destino: {self.clone_demands}  (suma total: {suma_demandas})
- Problema balanceado: {'Sí' if balanceado else 'No (se agregó variable ficticia con costo 0)'}
- Número de iteraciones realizadas: {len(self.values)}

RESULTADO OBTENIDO:
- Valores de asignación individuales (unidades × costo unitario): [{asignaciones_str}]
- Costo total mínimo: {self.result}

Por favor, estructura tu respuesta con estas secciones (máximo 200 palabras en total):
1. **Resumen del procedimiento**: Describe brevemente cómo funciona el Método de Costo Mínimo y cómo se aplicó.
2. **Interpretación del resultado**: Explica qué significa el costo total de {self.result} en el contexto del problema.
3. **Calidad de la solución**: Indica si esta es una solución óptima o una solución factible inicial (básica).
4. **Observaciones adicionales**: Menciona si el problema estaba balanceado y cualquier aspecto relevante."""

        print("\nGenerando conclusión con IA...")
        conclusion = groq_conclusion(self.client, user_content)

        if conclusion:
            print("\nConclusión:\n")
            print(conclusion)
        else:
            print("\nNo se pudo obtener conclusión de la IA.")

        return conclusion