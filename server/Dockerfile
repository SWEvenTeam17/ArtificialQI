FROM python:latest
WORKDIR /usr/src/app/ArtificialQI
# Installa git e curl
RUN apt update && apt install -y git curl
COPY requirements.txt .

# Installa le dipendenze (saranno disponibili via volume)
RUN pip install -r requirements.txt

# Scarica wait-for-it
RUN curl -o /wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /wait-for-it.sh

# Imposta la working dir dove sarà montato il volume
WORKDIR /usr/src/app/ArtificialQI/server/ArtificialQI

# Espone la porta
EXPOSE 8000

# Avvio del servizio
CMD ["/wait-for-it.sh", "mysql:3306", "--", "sh", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 8000 ArtificialQI.asgi:application"]
