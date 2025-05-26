### Create Sequential Model Agent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from google.genai import types
import os 
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

APP_NAME = os.getenv("APP_NAME", "PoemGenerator")
USER_ID = os.getenv("USER_ID", "user_developer")
SESSION_ID = os.getenv("SESSION_ID", "pipeline_session_1")


def create_agent():
    # Create an agent with a memory service
    session_service = InMemorySessionService()
    session = session_service.create_session(
        app_name = APP_NAME, 
        user_id = USER_ID,
        session_id = SESSION_ID
    )

    main_agent = SequentialAgent(
        name = "PoemGenerationAgent", 
        sub_agents=[],
        description="An agent that generates poems based on user input."
    )
    runner = Runner(
        agent=main_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    return runner

def call_agent(
        runner: Runner, 
        query: str
    ) -> str:
    content = types.Content(
        role=types.Role.USER,
        parts=[
            types.Part(
                text=query,
            )
        ]
    )

    events = runner.run(
        new_message=content,
        session_id=SESSION_ID,
        user_id=USER_ID
    )

    for event in events:
        if event.type == types.EventType.RESPONSE:
            return event.content.parts[0].text
        if event.is_final_response:
            final_response = event.content.parts[0].text
            print(f"Final response: {final_response}")

    return final_response