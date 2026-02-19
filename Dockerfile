FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Ecosystem_Alfa_TC .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py loaddata store_app/fixtures/* && python manage.py runserver 0.0.0.0:8000"]