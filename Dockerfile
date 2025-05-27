# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Instala Poetry
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias sin entorno virtual (Poetry ya maneja)
RUN pip install poetry 
ENV POETRY_VIRTUALENVS_CREATE=false



# Copia los archivos de dependencias primero
# Copiar solo pyproject.toml y poetry.lock primero
COPY francisco-rodriguez-alfaro/pyproject.toml francisco-rodriguez-alfaro/poetry.lock /app/

RUN poetry install


COPY francisco-rodriguez-alfaro /app/



# Expone el puerto
EXPOSE 8888

# Comando para ejecutar la app
CMD ["python", "run.py"]
