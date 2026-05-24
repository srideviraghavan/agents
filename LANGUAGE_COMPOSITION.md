# Repository Language Composition

## Language Distribution

```mermaid
pie title srideviraghavan/agents Language Composition
    "Python" : 53.6
    "TypeScript" : 29.7
    "CSS" : 14.4
    "JavaScript" : 1.4
    "HTML" : 0.9
```

## System Architecture - Request/Response Flow

```mermaid
sequenceDiagram
    participant User as User/Browser
    participant Frontend as React Frontend<br/>(localhost:5173)
    participant ViteProxy as Vite Proxy<br/>(/api → :8000)
    participant FastAPI as FastAPI Backend<br/>(localhost:8000)
    participant DB as SQLite<br/>Database
    participant BGTask as Background Task<br/>Worker
    participant Agent as Task Agent<br/>(LangChain/Router)

    rect rgb(200, 220, 255)
    note over User,Agent: 1. CREATE TASK - POST /api/tasks
    User->>Frontend: Enter prompt & select agent type
    Frontend->>Frontend: setInput(), setAgentType()
    Frontend->>ViteProxy: POST /api/tasks {prompt, agent_type}
    ViteProxy->>FastAPI: POST /api/tasks
    FastAPI->>DB: Create task record (pending state)
    DB-->>FastAPI: Task created (id, timestamp)
    FastAPI->>BGTask: add_task(_run_simulation)
    FastAPI-->>ViteProxy: 201 TaskResponse
    ViteProxy-->>Frontend: TaskResponse
    Frontend->>Frontend: setTasks(), setSelectedId()
    Frontend-->>User: Task appears in history
    end

    rect rgb(200, 255, 220)
    note over BGTask,Agent: 2. BACKGROUND EXECUTION
    BGTask->>BGTask: simulate_task(task_id, prompt, agent_type)
    BGTask->>Agent: Initialize agent with tools
    Agent->>Agent: Process prompt with LangChain
    BGTask->>DB: Append step (planning)
    BGTask->>DB: Append step (agent_action)
    BGTask->>DB: Append step (llm response)
    BGTask->>DB: Update task status (completed)
    DB-->>BGTask: Steps recorded
    end

    rect rgb(255, 220, 200)
    note over Frontend,FastAPI: 3. POLLING FOR UPDATES (every 1.5s)
    loop Until task completed or max attempts
        Frontend->>Frontend: Polling interval timer
        Frontend->>ViteProxy: GET /api/tasks (list)
        ViteProxy->>FastAPI: GET /api/tasks
        FastAPI->>DB: Query task summaries
        DB-->>FastAPI: TaskListItem[]
        FastAPI-->>ViteProxy: TaskListItem[]
        ViteProxy-->>Frontend: TaskListItem[]
        Frontend->>Frontend: setTasks() - update UI
        
        opt If selectedId exists
            Frontend->>ViteProxy: GET /api/tasks/{task_id}
            ViteProxy->>FastAPI: GET /api/tasks/{task_id}
            FastAPI->>DB: Query task with execution steps
            DB-->>FastAPI: TaskResponse (with steps)
            FastAPI-->>ViteProxy: TaskResponse
            ViteProxy-->>Frontend: TaskResponse
            Frontend->>Frontend: setSelectedTask()
            Frontend->>User: Display steps in timeline
        end
    end
    end

    rect rgb(255, 255, 200)
    note over Frontend,User: 4. DISPLAY RESULTS
    Frontend->>Frontend: Render TaskHistory (list)
    Frontend->>Frontend: Render StepTimeline (detail)
    Frontend->>Frontend: Show task status & execution steps
    Frontend-->>User: Display completed task with results
    end
```

## Summary

| Language | Percentage |
|----------|-----------|
| Python | 53.6% |
| TypeScript | 29.7% |
| CSS | 14.4% |
| JavaScript | 1.4% |
| HTML | 0.9% |

**Total: 100%**

The repository is primarily written in **Python** (over half the codebase), with a significant TypeScript component (nearly 30%). Styling is handled with CSS, and there are minimal JavaScript and HTML files.

## Architecture Notes

- **Frontend**: React + TypeScript + Vite (proxies `/api` to FastAPI)
- **Backend**: FastAPI + SQLite
- **Agent Layer**: LangChain with configurable agents (Router, Simple, Calculator, Text Processor)
- **Communication**: REST API with polling-based status updates (every 1.5s)
- **Task Execution**: FastAPI BackgroundTasks for async processing
