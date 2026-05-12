import os
from dotenv import load_dotenv
from src.commands.groq_conclusion import *
from src.commands.minimun_cost import minimun_cost

load_dotenv()
groqKey = os.getenv("GROQ_API_KEY")

def main():
    groqClient(groqKey, "")

if __name__=="__main__":
    main()