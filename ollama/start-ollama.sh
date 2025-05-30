#!/bin/sh
# start-ollama.sh
ollama serve &
sleep 2
ollama pull llama3.2:1b