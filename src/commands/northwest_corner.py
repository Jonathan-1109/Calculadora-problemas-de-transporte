from .transport import transport
from .groq_conclusion import groq_conclusion

class nortwest_corner(transport):

    def __init__(self, matriz, offers, demands):
        super().__init__(matriz, offers, demands)

    def resolve_nortwest(self):
        cont = 0
        while True:

            if not (self.offers and self.demands):
                self.result = sum(self.values)
                text = "\nValores para obtener el resultado de esquina noroeste: "
                for i in range(len(self.values)):
                    text += f"{self.values[i]}  "
                print(text)
                print(f"\nEl resultado por esquina noroeste es: {self.result}\n")
                return

            min_of_dem = self.offers[0] if self.offers[0] < self.demands[0] else self.demands[0]
            self.print_matriz(min_of_dem, self.matriz[0][0], cont)
            self.values.append(min_of_dem * self.matriz[0][0])
            self.offers[0] = self.offers[0] - min_of_dem
            self.demands[0] = self.demands[0] - min_of_dem

            if not self.demands[0]:
                self.demands.pop(0)
                for i in range(len(self.matriz)):
                    self.matriz[i].pop(0)

            if not self.offers[0]:
                self.offers.pop(0)
                self.matriz.pop(0)

            cont += 1

    def groq_promt(self):
        suma_ofertas = sum(self.clone_offers)
        suma_demandas = sum(self.clone_demands)
        balanceado = suma_ofertas == suma_demandas

        asignaciones_str = ", ".join(str(v) for v in self.values)

        user_content = f"""Analiza el siguiente problema de transporte resuelto por el **Método de la Esquina Noroeste** y proporciona una conclusión académica estructurada.

DATOS DEL PROBLEMA:
- Método utilizado: Esquina Noroeste
- Matriz de costos (filas=orígenes, columnas=destinos): {self.clone_matriz}
- Ofertas por origen: {self.clone_offers}  (suma total: {suma_ofertas})
- Demandas por destino: {self.clone_demands}  (suma total: {suma_demandas})
- Problema balanceado: {'Sí' if balanceado else 'No (se agregó variable ficticia con costo 0)'}
- Número de iteraciones realizadas: {len(self.values)}

RESULTADO OBTENIDO:
- Valores de asignación individuales (unidades × costo unitario): [{asignaciones_str}]
- Costo total obtenido: {self.result}

Por favor, estructura tu respuesta con estas secciones (máximo 200 palabras en total):
1. **Resumen del procedimiento**: Describe brevemente cómo funciona el Método de Esquina Noroeste y cómo se aplicó.
2. **Interpretación del resultado**: Explica qué significa el costo total de {self.result} en el contexto del problema.
3. **Calidad de la solución**: Clarifica que la Esquina Noroeste es una solución factible inicial, NO necesariamente óptima, y sugiere aplicar el Método Simplex de Transporte para optimizarla.
4. **Comparativa**: Menciona brevemente que métodos como Costo Mínimo o Aproximación de Vogel suelen dar un mejor punto de partida."""

        print("\nGenerando conclusión con IA...")
        conclusion = groq_conclusion(self.client, user_content)

        if conclusion:
            print("\nConclusión:\n")
            print(conclusion)
        else:
            print("\nNo se pudo obtener conclusión de la IA.")

        return conclusion
