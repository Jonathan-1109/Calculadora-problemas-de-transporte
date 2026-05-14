from dotenv import load_dotenv
import copy
from src.commands.minimun_cost import minimun_cost
from src.commands.northwest_corner import nortwest_corner
from src.commands.vogel_approximation import vogel_approximation

load_dotenv()

if __name__ == "__main__":
    try:
        matriz = [[5, 2, 7, 3],
                  [3, 6, 6, 1],
                  [6, 1, 2, 4],
                  [4, 3, 6, 6]]
        offers  = [80, 30, 60, 45]
        demands = [70, 40, 70, 35]

        """print("="*40)
        print("  MÉTODO DE COSTO MÍNIMO")
        print("="*40)
        t = minimun_cost(copy.deepcopy(matriz), offers[:], demands[:])
        t.resolve_minimun_cost()
        #t.groq_promt()

        print("\n" + "="*40)
        print("  MÉTODO DE LA ESQUINA NOROESTE")
        print("="*40)
        t2 = nortwest_corner(copy.deepcopy(matriz), offers[:], demands[:])
        t2.resolve_nortwest()
        t2.groq_promt()"""

        print("\n" + "="*40)
        print("  MÉTODO DE APROXIMACIÓN DE VOGEL")
        print("="*40)
        t3 = vogel_approximation(copy.deepcopy(matriz), offers[:], demands[:])
        t3.resolve_vogel()
        t3.groq_promt()

    except ValueError as ve:
        print(f"[Error de validación] {ve}")
    except Exception as e:
        print(f"[Error inesperado] {e}")
