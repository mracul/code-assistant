from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from orchestrator.agent_state import AgentState
from orchestrator.prompt_parser import PromptParser
from orchestrator.command_handler import COMMAND_REGISTRY
from orchestrator.context_builder import ContextBuilder
from orchestrator.workflow_runner import WorkflowRunner
import json
import asyncio
import uuid

app = FastAPI()
active_connections = {}

class UserInput(BaseModel):
    text: str

@app.post("/api/v1/connect")
async def connect():
    """Generates a unique ID for a new client connection."""
    connection_id = str(uuid.uuid4())
    state = AgentState(connection_id)
    active_connections[connection_id] = state
    return {"connection_id": connection_id}

@app.websocket("/ws/{connection_id}")
async def websocket_endpoint(websocket: WebSocket, connection_id: str):
    if connection_id not in active_connections:
        await websocket.close(code=1008)
        return
    
    state = active_connections[connection_id]
    await state.connect(websocket)
    
    try:
        await state.send_message("connection_ready", {"connection_id": connection_id})
        while True:
            # This websocket is for broadcasting from the server.
            # Input is handled via the HTTP endpoint.
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        state.disconnect()
        if connection_id in active_connections:
            del active_connections[connection_id]

# ... (Models and WebSocket endpoint remain the same) ...

async def handle_user_input(state: AgentState, user_input: str):
    """
    Parses user input and dispatches it to the appropriate command handler or workflow.
    """
    parser = PromptParser(user_input)
    parsed = parser.parse()
    state.add_message("user", user_input)
    
    command = parsed["command"]
    args = parsed["args"]
    instruction = parsed["instruction"]

    # Dispatch to the command registry
    if command in COMMAND_REGISTRY:
        await COMMAND_REGISTRY[command](state, args)
    elif command == "prompt":
        # Handle natural language prompts by running the context builder and then a workflow
        state.user_request = instruction
        await state.send_log("Natural language prompt detected. Building context...")
        context_builder = ContextBuilder(state)
        await context_builder.run()
        
        await state.send_log("Context ready. Starting agentic workflow...")
        workflow_runner = WorkflowRunner(state)
        asyncio.create_task(workflow_runner.execute_workflow('NewFeatureDevelopment'))
    else:
        await state.send_log(f"Unknown command: /{command}. Available commands: {list(COMMAND_REGISTRY.keys())}")

@app.post("/api/v1/input/{connection_id}")
async def user_input_endpoint(connection_id: str, user_input: UserInput):
    if connection_id not in active_connections:
        return {"status": "error", "message": "Invalid connection ID."}
    state = active_connections[connection_id]
    asyncio.create_task(handle_user_input(state, user_input.text))
    return {"status": "ok"}

# ... (The rest of the file remains the same) ...
