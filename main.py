from client import MCPClient
from fastapi import FastAPI
import asyncio
import uvicorn
import json

app = FastAPI()

@app.post("/query")
async def query(query: str):
    """Process a query using the MCPClient"""
    client = MCPClient()
    final_tools=[]
    try:
        with open('config.json', 'r') as file:
            data = json.load(file)
        for name, details in data["mcpServers"].items():
            await client.connect_to_server(details)
            tools = await client.getTools()
            final_tools.append(tools)
        result = await client.process_query(query, final_tools)
        return {"response": result}
    finally:
        await client.cleanup()

async def run_fastapi():
    config = uvicorn.Config(app=app, host="127.0.0.1", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    # Run FastAPI as a task
    # task = asyncio.create_task(run_fastapi())
    # await asyncio.sleep(1000)  # run for 60 seconds, or any condition
    # task.cancel()
    await run_fastapi()

if __name__ == "__main__":
    asyncio.run(main())