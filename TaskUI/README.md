# Task UI

## Phase 2: FastAPI + SQLite + REST API

### Backend

```bash
cd TaskUI/backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### Frontend

```bash
cd TaskUI/frontend
npm install
npm run dev
```

Open http://localhost:5173 (proxies `/api` to the backend).

### API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/tasks` | List tasks (summary) |
| GET | `/api/tasks/{id}` | Task with execution steps |
| POST | `/api/tasks` | Create task (`{"prompt":"..."}`) |

Task processing is simulated server-side until Phase 3 (LangChain agent). Include `fail` in a prompt to simulate an error.

### Phase 3 (next)

- LangChain agent with real execution steps via LM Studio

## Dependencies

### Backend
- Dependencies are managed via pyproject.toml

### Frontend
- React ^19.2.6
- React-DOM ^19.2.6
- Vite ^8.0.12
- TypeScript ~6.0.2
- ESLint ^10.3.0

### External Services
- OpenAI-compatible API endpoint
- Environment variables: `OPENAI_API_KEY`, `MODEL_NAME`, `BASE_URL`

## Assumptions and Tradeoffs

### Architecture Decisions
- **SQLite for persistence**: Chosen for simplicity and zero-configuration setup. Tradeoff: Not suitable for production-scale concurrent writes or distributed deployments.
- **FastAPI BackgroundTasks**: Used for async task execution instead of a proper job queue. Tradeoff: Tasks are lost if the server restarts during execution; no retry mechanism or distributed processing.
- **Polling-based frontend updates**: Frontend polls every 1.5s for task status. Tradeoff: Adds unnecessary network traffic and latency compared to WebSockets/SSE.
- **Synchronous agent execution**: Agent runs synchronously in background task. Tradeoff: Blocks a worker thread; no timeout enforcement at the framework level.
- **Hardcoded CORS origins**: Only allows localhost:5173. Tradeoff: Not flexible for different deployment environments.

### Agent Implementation
- **LangChain hub prompts**: Uses pre-built prompt from hub (`hwchase17/openai-tools-agent`). Tradeoff: Less control over prompt engineering; depends on external hub availability.
- **Tool-based architecture**: Uses TextProcessor, Calculator, and Weather tools. Tradeoff: Limited to predefined tools; no dynamic tool discovery.
- **Single LLM endpoint**: Configured for one model endpoint. Tradeoff: Cannot easily switch between multiple models or providers.

### Security & Reliability
- **No authentication**: API is completely open. Tradeoff: Not suitable for multi-user or production environments.
- **No rate limiting**: No protection against API abuse. Tradeoff: Vulnerable to DoS attacks.
- **Basic error handling**: Errors are caught and stored but not categorized or actionable. Tradeoff: Limited debugging insight.
- **No input validation beyond basic checks**: Minimal prompt validation. Tradeoff: Potential for injection attacks or malformed inputs.

## Future Improvements

- **Replace BackgroundTasks with Celery + Redis**: Add proper job queue with retry logic, distributed processing, and persistence across restarts.
- **Implement WebSockets**: Replace polling with real-time bidirectional communication for instant task updates.
- **Add authentication & authorization**: Implement user authentication (JWT/OAuth) and role-based access control.
- **Add comprehensive logging**: Structured logging with levels, correlation IDs, and log aggregation.
- **Switch to PostgreSQL**: Replace SQLite for production-grade concurrency and reliability.
- **Add rate limiting**: Implement per-user and per-IP rate limiting.
- **Add input validation & sanitization**: Comprehensive prompt validation and output sanitization.
- **Add unit and integration tests**: Test coverage for API endpoints, agent logic, and frontend components.
- **Add CI/CD pipeline**: Automated testing, linting, and deployment.
- **Add guardrails**: Implement content filtering and safety checks.
- **Dockerize the application**: Add Docker Compose for easy local development and deployment.
- **Add monitoring & metrics**: Integrate Prometheus/Grafana for performance monitoring.
- **Add task cancellation**: Allow users to cancel running tasks.
- **Support multiple agent types dynamically**: Plugin architecture for adding new agent types without code changes.
- **Add task scheduling**: Support for delayed or recurring task execution.
- **Improve UI/UX**: Add loading skeletons, better error states, and accessibility improvements.
- **Add export functionality**: Allow exporting task history and results (CSV, JSON).
- **Add task templates**: Pre-defined task templates for common operations.
