# AEGIE

## Adaptive Agentic AI-Based Voice Interview Evaluation

AEGIE is a research prototype for **voice-based interview evaluation using Agentic AI**. The framework processes a candidate's spoken interview response, converts speech to text, extracts speech-related features, evaluates semantic evidence, adapts subsequent question difficulty, and presents the collected evidence through a research dashboard.

> **Research prototype:** AEGIE is designed to support research and human review. It does not make hiring, pass/fail, or employment decisions.

---

## System Pipeline

```text
Candidate Voice Response
        ↓
NVIDIA Parakeet STT
        ↓
Transcript
        ↓
Speech Feature Extraction
        +
MiniLM Semantic Evidence
        ↓
Evaluation Agent
        ↓
Adaptive Agent
        ↓
Feedback Agent
        ↓
Research Results Dashboard
```

---

## Main Components

### 1. Voice Interview Interface

The Flask web interface presents interview questions and records candidate responses through the browser microphone.

Recorded responses are stored in WebM format for processing.

### 2. Speech-to-Text

AEGIE uses:

**NVIDIA Parakeet TDT 0.6B V2 INT8**

The model runs locally through **Sherpa-ONNX**.

The speech pipeline converts the recorded WebM audio into a compatible 16 kHz mono WAV representation before transcription.

### 3. Speech Features

AEGIE extracts descriptive speech evidence including:

- Words per minute (WPM)
- Filler-word count
- Pause count
- Response duration
- Word count

These features provide supporting evidence about the recorded response.

### 4. Semantic Evidence

AEGIE uses **MiniLM ONNX embeddings** to compare candidate responses with reference evidence.

Three semantic views are maintained:

- Whole-answer similarity
- Sentence-level similarity
- Concept-level similarity

This separation allows the framework to preserve multiple forms of semantic evidence instead of reducing the response immediately to a single opaque value.

### 5. Agentic AI Pipeline

AEGIE contains four primary agents:

```text
Interview Agent
      ↓
Evaluation Agent
      ↓
Adaptive Agent
      ↓
Feedback Agent
```

**Interview Agent** selects interview questions according to the job role and current interview state.

**Evaluation Agent** processes transcript, semantic evidence, and speech features.

**Adaptive Agent** determines the next question difficulty during DEVELOPMENT mode.

**Feedback Agent** converts the available evidence into prototype-level feedback for research analysis.

---

## Adaptive Logic

During DEVELOPMENT mode, AEGIE uses:

```text
Adaptive Evidence =
0.60 × Concept Mean Similarity
+
0.40 × Whole-Answer Similarity
```

Prototype thresholds:

```text
Evidence < 0.45        → EASIER
0.45 ≤ Evidence < 0.65 → SAME
Evidence ≥ 0.65        → HARDER
```

These thresholds are **development-only research rules**. They are not validated competency thresholds.

---

## Supported Job Roles

AEGIE currently contains question banks and reference evidence for:

- Data Scientist
- Software Developer
- Data Analyst
- Machine Learning Engineer
- Cloud DevOps Engineer
- Cybersecurity Analyst

---

## Research Collection Modes

AEGIE separates data collection into:

```text
DEVELOPMENT
PILOT
FINAL
```

DEVELOPMENT mode supports rule-based prototype experimentation.

PILOT and FINAL modes protect calibrated evaluation paths until appropriate human-annotated calibration evidence and validated scoring artifacts are available.

---

## Technology Stack

- Python 3.11
- Flask
- NVIDIA Parakeet TDT
- Sherpa-ONNX
- MiniLM
- ONNX Runtime
- FFmpeg / FFprobe
- NumPy
- Pandas
- Tokenizers
- Git
- GitHub
- GitHub Actions
- Docker

---

## Project Structure

```text
AEGIE/
├── app.py
├── Dockerfile
├── requirements.txt
├── data/
│   └── question_bank/
├── src/
│   ├── agents/
│   ├── audio_features.py
│   ├── transcription.py
│   ├── parakeet_adapter.py
│   ├── speech_features.py
│   ├── quality_check.py
│   ├── evaluation_feature_store.py
│   └── calibrated_score_store.py
├── templates/
│   ├── index.html
│   ├── interview.html
│   └── results.html
└── .github/
    └── workflows/
        └── aegie-ci.yml
```

---

## Local Setup

Create and activate a Python 3.11 environment, then install:

```bash
pip install -r requirements.txt
```

FFmpeg and FFprobe must also be available on the host system.

AEGIE additionally requires the local Parakeet and MiniLM model artifacts.

Expected model directories:

```text
models/
├── semantic_minilm/
│   ├── model.onnx
│   └── tokenizer.json
│
└── sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8/
    ├── encoder.int8.onnx
    ├── decoder.int8.onnx
    ├── joiner.int8.onnx
    └── tokens.txt
```

The large model files are intentionally excluded from Git.

---

## Run Locally

From the project directory:

```bash
python app.py
```

If port `5000` is unavailable, AEGIE can be started on another port, for example:

```bash
python -c "import app; app.app.run(host='127.0.0.1', port=5001, debug=False)"
```

Then open:

```text
http://127.0.0.1:5001
```

---

## Docker

Build the image:

```bash
docker build -t aegie:latest .
```

Run AEGIE while mounting the local model directory:

```bash
docker run --rm \
  --name aegie-container \
  -p 5002:5001 \
  -v "$(pwd)/models:/app/models:ro" \
  aegie:latest
```

Open:

```text
http://127.0.0.1:5002
```

Health check:

```text
http://127.0.0.1:5002/ping
```

Expected response:

```text
AEGIE SERVER OK
```

---

## Continuous Integration

The repository includes a GitHub Actions workflow:

```text
.github/workflows/aegie-ci.yml
```

The CI pipeline performs:

```text
GitHub Push
     ↓
Dependency Installation
     ↓
Python Syntax Validation
     ↓
Docker Image Build
```

Large local AI models are intentionally excluded from CI.

---

## Research Scope and Limitations

AEGIE currently operates as a **research prototype**.

The DEVELOPMENT workflow provides semantic evidence, speech evidence, rule-based adaptation, and prototype feedback.

The current development thresholds must not be interpreted as validated measures of candidate competency.

The framework does not produce an autonomous hiring recommendation or pass/fail decision.

Calibrated scoring requires appropriate pilot data, human annotations, calibration procedures, and validation before it can be treated as a validated evaluation mechanism.

---

## Repository

**Project:** AEGIE  
**Repository:** AEGIE123

---

## Author

**Dhaslim N**  
M.Tech Data Science