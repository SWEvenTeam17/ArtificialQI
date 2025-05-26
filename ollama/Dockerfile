FROM ollama/ollama:latest
COPY start-ollama.sh /start-ollama.sh
RUN chmod +x /start-ollama.sh
RUN sed -i -e 's/\r$//' start-ollama.sh
RUN /start-ollama.sh
