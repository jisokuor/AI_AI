# Ollama Gemma3 FastA2A Agent

The **FastA2A Ollama agent** is a Python FastAPI-based service that exposes a FastA2A v0.2-compatible API for avatars and automation tools. It acts as a bridge between FastA2A clients and a local Ollama LLM (e.g., Gemma3), enabling automated conversations, test automation, and integration into CI/CD workflows. The agent is designed for reliability, extensibility, and ease of use by both technical and non-technical users.

## Installation and Setup
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

## Quick Start
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

## Usage with Avatars and Automation

### FastA2A Agent Metadata (.well-known/agent.json)

This repository includes a static agent card at `.well-known/agent.json`.

**Key fields for FastA2A v0.2 compatibility:**
- `protocol`: Specifies protocol name and version.
- `endpoints`: Now includes both `a2a` and `metadata` (and optionally `health`).
- `build`: (Optional) Includes commit and build time for auditability.

**Purpose:** Enables automated discovery and integration with FastA2A-compatible tools.
**Customization:** Edit the fields (name, description, endpoints, etc.) to match your deployment.
**Reference:** See the template for required fields and example values.



This repository includes a static agent card at `.well-known/agent.json`. This file follows the FastA2A protocol and describes the agent's identity, capabilities, and endpoint for discovery by other agents or clients.

- **Location:** `.well-known/agent.json`
- **Purpose:** Enables automated discovery and integration with FastA2A-compatible tools.
- **Customization:** Edit the fields (name, description, endpoints, etc.) to match your deployment.
- **Reference:** See the template for required fields and example values.

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

## Testing and Quality Assurance
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

## Troubleshooting and FAQ
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

## Extensibility and Development
### Adding Models or Endpoints
- To add a new model, update the Ollama configuration and ensure the agent forwards prompts correctly.
- To add endpoints, extend the FastAPI app in `main.py`.

### Best Practices
- Regularly review the repository for secrets before pushing.
- Clean up unnecessary files and artifacts before committing.
- Use automated secret scanning tools (e.g., git-secrets, truffleHog).
- Store secrets (e.g., GitHub PAT) securely and reference them as environment variables or via your automation platform.
- Follow PEP8 and FastAPI best practices for code quality.

## Further Documentation
- See [User_manual.md](./User_manual.md) for a full user guide.
- See [testing_evident.md](./testing_evident.md) for test evidence and scenarios.


---

## Internet Connectivity Checker (connectivity_checker.py)

This repository also includes a simple Python utility for checking internet connectivity.

### What is it?
- `connectivity_checker.py` is a reusable module that checks if the environment has outbound internet access.
- It attempts a GET request to a specified URL (default: https://www.google.com) with a configurable timeout.
- Returns `True` if the network is reachable (status code < 500), otherwise `False`.
- Handles all network errors gracefully (returns `False` on timeout, DNS failure, etc.).

### Usage
**As a module in your Python code:**
```python
from connectivity_checker import is_connected
if is_connected():
    print('Internet is reachable!')
else:
    print('No internet connection.')
```

**Standalone test:**
```bash
python3 -c "from connectivity_checker import is_connected; print(is_connected())"
```

### Customization
- You can specify a different URL or timeout:
```python
is_connected(url='https://example.com', timeout=5)
```

### When to use
- Before running scripts or automation that require internet access
- In CI/CD pipelines to check network status
- As a diagnostic tool in containers or cloud environments

---

---

## Human-Dolphin Grid Simulation as a System Under Test (SUT) for Learning Software Testing

This repository includes a unique, grid-based simulation designed specifically as a **System Under Test (SUT)** for training and developing software test teams—including both human and virtual AI agentified teams.

### Purpose and Educational Value
- **Realistic Practice:** The simulation provides a controllable, engaging environment for practicing all phases of the software testing lifecycle: requirements analysis, test design, execution, defect reporting, and results analysis.
- **Agent-Based Complexity:** By simulating interactions between human and dolphin agents on a 50x50 grid—with configurable illness rates, safe zones, and adjacency logic—the SUT offers rich scenarios for black-box, white-box, exploratory, and regression testing.
- **Auditability & Traceability:** Each simulation run creates a unique output directory, ensuring data safety, reproducibility, and auditability—ideal for test reporting and process improvement exercises.
- **Teamwork & Role Rotation:** The SUT supports collaborative exercises, role rotation (analyst, automator, reviewer), and feedback cycles, aligning with ISTQB and test management best practices.
- **AI-Driven Testing:** The simulation is suitable for both human testers and AI-driven/agentified test automation, making it a modern platform for hybrid or fully virtual test teams.

### Key Components
- `grid_competition.py`: Main simulation script for human-dolphin interactions.
- `human_dolphin_competition_cluster50x50.py`: For batch or clustered simulation runs.
- `grid_competition/`: Supporting modules and configurations.
- `simulation_runs/`: Stores all output data, logs, and results, organized by unique run folders.

### Typical Training Use Cases
- Practicing test case design, execution, and defect reporting in a safe, repeatable environment.
- Onboarding new testers or AI agents to real-world testing challenges.
- Team-building, mentoring, and skill development through collaborative exercises.
- Experimenting with automation frameworks and test management tools.

**In summary:**
> This simulation SUT is a powerful, motivating tool for building technical, methodological, and soft skills in test teams—whether human, AI, or a mix of both.

---

## Verbal Walkthrough: Main Use Cases for the Human-Dolphin Grid Simulation

This simulation is designed as a hands-on System Under Test (SUT) for software test teams and learners. Here’s how you might use it in practice:

**1. Test Case Design and Requirements Analysis**
- Begin by reviewing the simulation’s rules: humans and dolphins are placed in pairs on a 50x50 grid, with safe zones, illness rates, and adjacency logic.
- Teams can analyze requirements (e.g., what constitutes a valid pair, how illness spreads, what outputs are expected) and design black-box or white-box test cases.

**2. Running and Observing Simulations**
- Launch a simulation run (demo, test, or persistent mode). Each run creates a uniquely named output directory, ensuring all results are traceable and never overwritten.
- Observe outputs: logs, summaries, timecourses, and visualizations (e.g., GIFs of grid evolution).
- Use these outputs to verify expected behaviors, detect anomalies, and validate test cases.

**3. Defect Reporting and Analysis**
- If unexpected results or errors are found, teams can use the isolated run directories to collect evidence, reproduce issues, and file detailed defect reports.
- The strict output versioning makes it easy to compare runs, track regressions, and audit fixes.

**4. Automation and Performance Testing**
- Use the batch/cluster script to run large numbers of simulations with varying parameters.
- Analyze aggregate results for performance, stability, or emergent behaviors.
- Integrate with test automation frameworks to practice CI/CD and automated regression testing.

**5. Teamwork, Role Rotation, and Learning**
- Rotate roles: one person configures the simulation, another designs tests, a third analyzes outputs, and so on.
- Practice communication, documentation, and feedback cycles in a safe, engaging environment.

**6. Experimentation and Exploration**
- Tweak parameters (e.g., illness rates, safe zone size) to explore edge cases and system limits.
- Use exploratory testing to discover unexpected behaviors or emergent phenomena.

This simulation provides a realistic, auditable playground for building both technical and soft skills in software testing, with every run preserved for learning and improvement.
