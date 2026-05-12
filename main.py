from os import getenv
from dotenv import load_dotenv
from src.commands.minimun_cost import minimun_cost

load_dotenv()

if __name__ == "__main__":
    try:
        matriz = [[5,2,7,3],[3,6,6,1],[6,1,2,4],[4,3,6,6]]
        offers = [80,30,60,45]
        demands = [70,40,70,35]
        t = minimun_cost(matriz, offers, demands)
        t.resolve_minimun_cost()
        t.groq_promt()
    except ValueError as ve:
        print(ve)