# FastA2A Ollama Agent User Manual

## 1. Introduction and Purpose

The **FastA2A Ollama agent** is a Python FastAPI-based service that exposes a FastA2A v0.2-compatible API for avatars and automation tools. It acts as a bridge between FastA2A clients and a local Ollama LLM (e.g., Gemma3), enabling automated conversations, test automation, and integration into CI/CD workflows. The agent is designed for reliability, extensibility, and ease of use by both technical and non-technical users.

---

## 2. Installation and Setup

### Prerequisites
- Python 3.9+
- [Ollama](https://ollama.com/) installed and running locally (with a supported model, e.g., Gemma3)
- Git (for cloning the repository)
- Docker (optional, for containerized deployment)

### Clone the Repository
```bash
git clone https://github.com/your-org/ollama_a2a_agent.git
cd ollama_a2a_agent
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environment Setup
- Ensure Ollama is running and the desired model (e.g., Gemma3) is available.
- (Optional) Configure environment variables as needed (see `.env.example`).

### Running the Agent (Host)
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
- The agent will be available at `http://localhost:8000`.

### Running with Docker
```bash
docker build -t ollama-a2a-agent .
docker run -d -p 8000:8000 --network=host ollama-a2a-agent
```
**Note:**
- For Docker, use `--network=host` to allow access to the local Ollama instance.
- If running in a container, ensure the agent listens on `0.0.0.0` and that Docker networking allows access to Ollama.

---

## 3. Quick Start

### Verify Endpoints
- Check agent metadata:
  ```bash
  curl http://localhost:8000/.well-known/agent.json
  ```
- Send a test prompt:
  ```bash
  curl -X POST http://localhost:8000/a2a \
    -H 'Content-Type: application/json' \
    -d '{"prompt": "Hello, who are you?"}'
  ```
- You should receive a streaming or full JSON response from the model.

### Basic Testing
- Run the provided test suite:
  ```bash
  pytest
  ```
- See [testing_evident.md](./testing_evident.md) for detailed test evidence and scenarios.

---

## 4. Usage with Avatars and Automation

### FastA2A Integration
- The agent implements the FastA2A v0.2 protocol, supporting avatars and automation tools.
- Endpoints:
  - `GET /.well-known/agent.json` – Agent metadata
  - `POST /a2a` – Main conversation endpoint (accepts `prompt` or `message` fields)

### Example: Automated Conversation
```python
import requests

url = 'http://localhost:8000/a2a'
payload = {"prompt": "Summarize the latest test results."}
response = requests.post(url, json=payload, stream=True)
for line in response.iter_lines():
    print(line.decode())
```

### Sample Avatar Conversation
- Avatar sends a prompt to `/a2a` and receives a streaming response.
- Integrate with test automation frameworks by calling the API and parsing the response.

---

## 5. Testing and Quality Assurance

- Comprehensive automated tests are provided and documented in [testing_evident.md](./testing_evident.md).
- To run tests:
  ```bash
  pytest
  ```
- To extend tests, add new cases to the `tests/` directory following the existing structure.
- Tests cover:
  - Endpoint availability and correctness
  - Error handling (e.g., missing fields, wrong methods)
  - Model integration
  - Edge cases and streaming behavior

---

## 6. Troubleshooting and FAQ

### Common Issues
- **Cannot connect from Docker container:**
  - Ensure the agent listens on `0.0.0.0`.
  - Use Docker's `--network=host` mode.
  - Check firewall and Docker network settings.
- **Authentication errors with GitHub:**
  - Store your GitHub PAT as a secret (e.g., `GITHUB_PAT`) and reference it securely.
  - See secret management tips below.
- **Model not responding:**
  - Verify Ollama is running and the model is loaded.
  - Check agent logs for errors.
- **400/405 errors on /a2a:**
  - Ensure you use POST with a valid JSON body containing `prompt` or `message`.

### Solutions
- Restart the agent after changing configuration or secrets.
- Review [testing_evident.md](./testing_evident.md) for known issues and resolutions.
- For Docker networking, see [Docker networking docs](https://docs.docker.com/network/).

---

## 7. Extensibility and Development

### Adding Models or Endpoints
- To add a new model, update the Ollama configuration and ensure the agent forwards prompts correctly.
- To add endpoints, extend the FastAPI app in `main.py`.

### Best Practices
- Regularly review the repository for secrets before pushing.
- Clean up unnecessary files and artifacts before committing.
- Use automated secret scanning tools (e.g., git-secrets, truffleHog).
- Store secrets (e.g., GitHub PAT) securely and reference them as environment variables or via your automation platform.
- Follow PEP8 and FastAPI best practices for code quality.

---

## 8. Contact and Support

This user manual is provided as-is. For issues or feature requests, please use the GitHub repository issue tracker.
---

*Thank you for using the FastA2A Ollama agent! For more details, see the repository README and [testing_evident.md](./testing_evident.md).*