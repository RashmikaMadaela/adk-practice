from __future__ import annotations

import dotenv
from google.adk.agents import Agent

dotenv.load_dotenv()


root_agent = Agent(
    name="simple_agent",
    model="gemini-2.5-flash",
    description="A basic ADK training assistant.",
    instruction="""
You are a helpful assistant for an ADK basics training session.

Keep answers clear, practical, and beginner-friendly.
When explaining code, use short examples.
""",
)