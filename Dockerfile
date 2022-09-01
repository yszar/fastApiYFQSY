FROM antonapetrov/uvicorn-gunicorn-fastapi:python3.10

COPY ./backend/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./backend /app