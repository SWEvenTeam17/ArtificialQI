FROM python:latest
WORKDIR /usr/src/app/ArtificialQI
COPY requirements.txt .
RUN apt update && apt install -y git
RUN pip install -r requirements.txt
WORKDIR /usr/src/app/ArtificialQI/microservices/LLMService
EXPOSE 8001
CMD ["daphne", "-b", "0.0.0.0", "-p", "8001", "LLMService.asgi:application"]
