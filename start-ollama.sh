#!/bin/sh

MODEL_DIR="/root/.ollama/models/manifests/registry.ollama.ai/library/phi3"

ollama serve &

echo 'Waiting for Ollama service to start...'
sleep 30

if [ ! "$(ls -A $MODEL_DIR)" ]; then
    echo 'phi model not found, downloading...'
    ollama pull phi3
    echo 'Model downloaded successfully.'
else
    echo 'phi3 model already present, skipping download.'
fi

# Keep the container running
tail -f /dev/null