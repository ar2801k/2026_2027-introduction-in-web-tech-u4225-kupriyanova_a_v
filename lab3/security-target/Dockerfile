FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN mkdir -p /app/files \
    && echo "This is a public training file." > /app/files/public.txt \
    && echo "LAB3_SECRET=training-only-secret" > /app/secret.txt

EXPOSE 8081

CMD ["python", "app.py"]