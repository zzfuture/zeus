# Utilizar una imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo requirements.txt y las dependencias
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente (en la carpeta src) y el archivo .env al contenedor
COPY src/ /app/src
COPY .env /app/.env

# Establecer el directorio de trabajo dentro de src
WORKDIR /app/src

# Exponer el puerto de la aplicación si es necesario (por ejemplo, 5000 para Flask)
EXPOSE 8000

# Comando para ejecutar la aplicación (ajusta según el archivo de entrada)
CMD ["fastapi", "run", "main.py", "--port", "8000"]
