FROM python:3.11-slim

WORKDIR /app

# AEGIE system dependency for audio conversion and analysis
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy AEGIE source code
COPY app.py .
COPY src/ ./src/
COPY templates/ ./templates/
COPY data/question_bank/ ./data/question_bank/

# Runtime directories
RUN mkdir -p \
    audio/development \
    audio/pilot \
    audio/final \
    models/semantic_minilm \
    models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8

# Flask port inside container
EXPOSE 5001

ENV PYTHONUNBUFFERED=1

CMD ["python", "-c", "import app; app.app.run(host='0.0.0.0', port=5001, debug=False)"]