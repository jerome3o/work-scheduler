FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src /app

RUN mkdir outputs

# fastapi
CMD ["uvicorn", "solver.server:app", "--host", "0.0.0.0", "--port", "8000"]
