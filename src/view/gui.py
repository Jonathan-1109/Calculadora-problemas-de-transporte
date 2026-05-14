import sys
import copy
import customtkinter as ctk
from src.commands.minimun_cost import minimun_cost
from src.commands.northwest_corner import nortwest_corner
from src.commands.vogel_approximation import vogel_approximation

BG_COLOR = "#121212" 
FRAME_COLOR = "#1E1E1E"       
TEXT_COLOR = "#E0E0E0"       
PRIMARY_COLOR = "#3B82F6"     
PRIMARY_HOVER = "#2563EB"     
SUCCESS_COLOR = "#10B981"    
SUCCESS_HOVER = "#059669"   
INPUT_BG = "#2C2C2C"          
OFFER_BG = "#1F2937"          
DEMAND_BG = "#372F2F"        
FONT_TITLE = ("Roboto", 24, "bold")
FONT_SUBTITLE = ("Roboto", 16, "bold")
FONT_BODY = ("Roboto", 14)
FONT_CONSOLE = ("Consolas", 13)


class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", string)
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")

    def flush(self):
        pass


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora de Problemas de Transporte")
        self.geometry("1000x850")
        self.configure(fg_color=BG_COLOR)
        self.eval('tk::PlaceWindow . center')

        self.matrix_entries = []
        self.offer_entries = []
        self.demand_entries = []

        self.setup_ui()

    def setup_ui(self):
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=40, pady=30)

        title_label = ctk.CTkLabel(
            self.main_container, 
            text="Calculadora de Transporte", 
            font=FONT_TITLE,
            text_color=TEXT_COLOR
        )
        title_label.pack(anchor="w", pady=(0, 20))

        self.top_frame = ctk.CTkFrame(self.main_container, fg_color=FRAME_COLOR, corner_radius=12)
        self.top_frame.pack(fill="x", pady=(0, 20), ipadx=10, ipady=10)

        top_inner = ctk.CTkFrame(self.top_frame, fg_color="transparent")
        top_inner.pack(pady=15, padx=20, anchor="w")

        ctk.CTkLabel(top_inner, text="Orígenes (Filas):", font=FONT_BODY).grid(row=0, column=0, padx=(0, 10))
        self.rows_entry = ctk.CTkEntry(top_inner, width=80, fg_color=INPUT_BG, border_width=1, font=FONT_BODY)
        self.rows_entry.grid(row=0, column=1, padx=(0, 30))

        ctk.CTkLabel(top_inner, text="Destinos (Columnas):", font=FONT_BODY).grid(row=0, column=2, padx=(0, 10))
        self.cols_entry = ctk.CTkEntry(top_inner, width=80, fg_color=INPUT_BG, border_width=1, font=FONT_BODY)
        self.cols_entry.grid(row=0, column=3, padx=(0, 30))

        self.btn_generate = ctk.CTkButton(
            top_inner, 
            text="Generar Matriz", 
            font=FONT_BODY,
            fg_color=PRIMARY_COLOR, 
            hover_color=PRIMARY_HOVER,
            corner_radius=8,
            command=self.generate_matrix
        )
        self.btn_generate.grid(row=0, column=4, padx=(10, 0))

        self.matrix_wrapper = ctk.CTkFrame(self.main_container, fg_color=FRAME_COLOR, corner_radius=12)
        self.matrix_wrapper.pack(fill="both", expand=True, pady=(0, 20))
        
        ctk.CTkLabel(self.matrix_wrapper, text="Matriz de Costos, Oferta y Demanda", font=FONT_SUBTITLE).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.matrix_frame = ctk.CTkScrollableFrame(self.matrix_wrapper, fg_color="transparent")
        self.matrix_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.control_frame = ctk.CTkFrame(self.main_container, fg_color=FRAME_COLOR, corner_radius=12)
        self.control_frame.pack(fill="x", pady=(0, 20), ipadx=10, ipady=10)

        control_inner = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        control_inner.pack(pady=15, padx=20, anchor="w")

        ctk.CTkLabel(control_inner, text="Método de Resolución:", font=FONT_BODY).grid(row=0, column=0, padx=(0, 15))
        
        self.method_var = ctk.StringVar(value="Costo Mínimo")
        self.method_dropdown = ctk.CTkComboBox(
            control_inner, 
            variable=self.method_var,
            values=["Costo Mínimo", "Esquina Noroeste", "Aproximación de Vogel"],
            state="readonly",
            width=220,
            font=FONT_BODY,
            dropdown_font=FONT_BODY,
            fg_color=INPUT_BG,
            button_color=PRIMARY_COLOR,
            button_hover_color=PRIMARY_HOVER,
            border_width=1
        )
        self.method_dropdown.grid(row=0, column=1, padx=(0, 30))

        self.btn_calculate = ctk.CTkButton(
            control_inner, 
            text="Calcular Resultado", 
            font=("Roboto", 14, "bold"),
            fg_color=SUCCESS_COLOR, 
            hover_color=SUCCESS_HOVER,
            corner_radius=8,
            command=self.calculate
        )
        self.btn_calculate.grid(row=0, column=2)

        console_wrapper = ctk.CTkFrame(self.main_container, fg_color=FRAME_COLOR, corner_radius=12)
        console_wrapper.pack(fill="both", expand=True)

        ctk.CTkLabel(console_wrapper, text="Consola de Salida", font=FONT_SUBTITLE).pack(anchor="w", padx=20, pady=(15, 0))

        self.console_text = ctk.CTkTextbox(
            console_wrapper, 
            state="disabled", 
            font=FONT_CONSOLE,
            fg_color="#0D0D0D",
            text_color="#A9B7C6",  
            corner_radius=8,
            border_width=1,
            border_color="#333333"
        )
        self.console_text.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        sys.stdout = RedirectText(self.console_text)
        sys.stderr = RedirectText(self.console_text)

        print("Esperando configuración de matriz...")

    def generate_matrix(self):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            if rows <= 0 or cols <= 0:
                raise ValueError
        except ValueError:
            print("[Error]: Por favor ingresa números enteros mayores a 0 para filas y columnas.")
            return

        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        self.matrix_entries = []
        self.offer_entries = []
        self.demand_entries = []

        for j in range(cols):
            ctk.CTkLabel(self.matrix_frame, text=f"D{j+1}", font=("Roboto", 13, "bold"), text_color="#888888").grid(row=0, column=j+1, padx=8, pady=8)
        
        ctk.CTkLabel(self.matrix_frame, text="OFERTA", font=("Roboto", 13, "bold"), text_color="#60A5FA").grid(row=0, column=cols+1, padx=15, pady=8)
        for i in range(rows):
            ctk.CTkLabel(self.matrix_frame, text=f"O{i+1}", font=("Roboto", 13, "bold"), text_color="#888888").grid(row=i+1, column=0, padx=8, pady=8)
            
            row_entries = []
            for j in range(cols):
                entry = ctk.CTkEntry(self.matrix_frame, width=65, height=35, justify="center", font=FONT_BODY, fg_color=INPUT_BG, border_width=1)
                entry.grid(row=i+1, column=j+1, padx=4, pady=4)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

            offer_entry = ctk.CTkEntry(self.matrix_frame, width=65, height=35, justify="center", font=FONT_BODY, fg_color=OFFER_BG, border_color="#3B82F6", border_width=1)
            offer_entry.grid(row=i+1, column=cols+1, padx=15, pady=4)
            self.offer_entries.append(offer_entry)

        ctk.CTkLabel(self.matrix_frame, text="DEMANDA", font=("Roboto", 13, "bold"), text_color="#F87171").grid(row=rows+1, column=0, padx=8, pady=15)
        for j in range(cols):
            demand_entry = ctk.CTkEntry(self.matrix_frame, width=65, height=35, justify="center", font=FONT_BODY, fg_color=DEMAND_BG, border_color="#EF4444", border_width=1)
            demand_entry.grid(row=rows+1, column=j+1, padx=4, pady=15)
            self.demand_entries.append(demand_entry)

        print(f"Matriz generada exitosamente: {rows} Orígenes x {cols} Destinos.")

    def calculate(self):
        self.console_text.configure(state="normal")
        self.console_text.delete("1.0", "end")
        self.console_text.configure(state="disabled")

        try:
            matriz = []
            for row_entries in self.matrix_entries:
                row_values = [float(entry.get()) for entry in row_entries]
                matriz.append(row_values)

            offers = [float(entry.get()) for entry in self.offer_entries]
            demands = [float(entry.get()) for entry in self.demand_entries]
        except ValueError:
            print("[Error]: Por favor llena todos los campos generados con números válidos.")
            return

        method = self.method_var.get()
        print(f"--- EJECUTANDO MÉTODO: {method.upper()} ---\n")

        try:
            if method == "Costo Mínimo":
                t = minimun_cost(copy.deepcopy(matriz), offers[:], demands[:])
                t.resolve_minimun_cost()
                t.groq_promt()

            elif method == "Esquina Noroeste":
                t = nortwest_corner(copy.deepcopy(matriz), offers[:], demands[:])
                t.resolve_nortwest()
                t.groq_promt()

            elif method == "Aproximación de Vogel":
                t = vogel_approximation(copy.deepcopy(matriz), offers[:], demands[:])
                t.resolve_vogel()
                t.groq_promt()

        except ValueError as ve:
            print(f"[Error de validación]: {ve}")
        except Exception as e:
            print(f"[Error inesperado]: {e}")
