FROM python:3.9-slim
ENV PYTHONDONTWRITEBYTECODE 1  # Не создавать файлы .pyc
ENV PYTHONUNBUFFERED 1         # Обеспечить вывод Python без буферизации
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
WORKDIR /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
