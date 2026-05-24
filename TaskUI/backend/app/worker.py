import asyncio
import os
from app import crud
from app.database import SessionLocal
from app.task_processor_router_agent import TaskProcessorRouterAgent

async def simulate_task(task_id: str, prompt: str, agent_type: str = "router") -> None:
    await _sleep_step(task_id, 0.4, lambda db: crud.update_task_status(db, task_id, "running"))
    await _append(task_id, 2, "status", "Processing started")

    try:
        # Initialize the appropriate agent based on agent_type
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "lmstudio")
        model_name = os.getenv("MODEL_NAME", "zai-org/glm-4.7-flash")
        base_url = os.getenv("BASE_URL", "http://localhost:1234/v1")

        agent = TaskProcessorRouterAgent(model_name=model_name, temperature=0, base_url=base_url)
        await _append(
            task_id,
            3,
            "llm",
            "Agent Initialization",
            f"Initialized TaskProcessorRouterAgent with tools: {', '.join(agent.get_tool_names())}",
            delay=0.3,
        )
        result = agent.run(prompt)  
        
        await _append(
            task_id,
            4,
            "agent_action",
            "Agent Execution",
            f"Executed query with {agent_type} agent",
            delay=0.3,
        )

        await _append(
            task_id,
            5,
            "llm",
            "Generating response",
            "Agent completed successfully",
            delay=0.3,
        )

        await _append(task_id, 6, "status", "Completed", delay=0.3)

        def _complete(db):
            crud.complete_task(db, task_id, result)

        await _run_db(_complete)

    except Exception as e:
        await _append(
            task_id,
            4,
            "error",
            "Execution failed",
            str(e),
            delay=0.3,
        )

        def _fail(db):
            crud.fail_task(db, task_id, str(e))

        await _run_db(_fail)


async def _sleep_step(task_id: str, seconds: float, fn) -> None:
    await asyncio.sleep(seconds)
    await _run_db(fn)


async def _append(
    task_id: str,
    sequence: int,
    step_type: str,
    title: str,
    detail: str | None = None,
    delay: float = 0,
) -> None:
    if delay:
        await asyncio.sleep(delay)

    def _add(db):
        crud.add_step(db, task_id, sequence, step_type, title, detail)
        db.commit()

    await _run_db(_add)


async def _run_db(fn) -> None:
    db = SessionLocal()
    try:
        fn(db)
    finally:
        db.close()
