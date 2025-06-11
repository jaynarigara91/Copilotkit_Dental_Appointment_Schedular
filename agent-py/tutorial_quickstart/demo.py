"""Demo"""

import os
from dotenv import load_dotenv 
load_dotenv()

# pylint: disable=wrong-import-position
from tutorial_quickstart.Agents import Appointment
from fastapi import FastAPI
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitSDK, LangGraphAgent

app = FastAPI()
appointment = Appointment()
graph = appointment()
sdk = CopilotKitSDK(
    agents=[
        LangGraphAgent(
            name="quickstart_agent",
            description="Quickstart agent.",
            graph=graph,
        ),
    ],
)

add_fastapi_endpoint(app, sdk, "/copilotkit")

# add new route for health check
@app.get("/health")
def health():
    """Health check."""
    return {"status": "ok"}


def main():
    """Run the uvicorn server."""
    # port = int(os.getenv("PORT", "8000"))
    uvicorn.run("tutorial_quickstart.demo:app", host="0.0.0.0", port=8000)
