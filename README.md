# Calculadora de problemas de transporte (Python)
Calculadora con interfaz para los métodos de costo minimo, esquina noroeste y aproximación de vogel, con conexión a la API de groq para generar y obtener una conclusión del ejercicio

### 1. Clonar repositorio
```bash
git clone https://github.com/Jonathan-1109/Calculadora-problemas-de-transporte.git
```

### 2. Crear el entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate #linux/mac
.venv\Scripts\activate #windows
```

### 3. Instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
### 4. Generar una apikey 
Crea y obten una apikey en [GroqCloud](https://console.groq.com/) y crea un archivo .env en la raiz del proyecto, usando de ejemplo el .env.example
