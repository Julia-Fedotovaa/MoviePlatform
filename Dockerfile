FROM python:3.13-slim

LABEL authors="julia"

WORKDIR /MoviePlatform

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade dataclass-wizard

COPY . .

EXPOSE 8000

CMD ["python", "MoviePlatform/manage.py", "runserver_plus", "0.0.0.0:8000", "--cert-file", "cert.crt"]
