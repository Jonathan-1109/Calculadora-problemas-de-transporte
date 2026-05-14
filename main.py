from dotenv import load_dotenv
from src.view.gui import App

load_dotenv()

if __name__ == "__main__":
    app = App()
    app.mainloop()
