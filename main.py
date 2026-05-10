import os
from dotenv import load_dotenv
from src.controllers.groq_conclusion import *

load_dotenv()

groqClient(os.getenv("GROQ_API_KEY"), "")
