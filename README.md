# powerplant-coding-challenge


## Welcome
Technical test Francisco Rodriguez Alfaro


## Run with docker
docker build -t flask-api .

docker run -p 8888:8888 flask-api


## Ejecutar en local con python 3
pip install poetry

poetry config virtualenvs.in-project true

cd francisco-rodriguez-alfaro

poetry install

.\.venv\Scripts\activate.ps1

python run.py


## Ejecutar los tests 
cd francisco-rodriguez-alfaro

.\.venv\Scripts\activate.ps1

pytest
