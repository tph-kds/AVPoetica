### Create Sequential Model Agent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from avp import root_agent

from google.genai import types
import os 
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

APP_NAME = os.getenv("APP_NAME", "PoemGenerator")
USER_ID = os.getenv("USER_ID", "user_developer")
SESSION_ID = os.getenv("SESSION_ID", "pipeline_session_1")


def create_agent(
        main_agent: SequentialAgent
):
    # Create an agent with a memory service
    session_service = InMemorySessionService()
    session_service.create_session(
        app_name = APP_NAME, 
        user_id = USER_ID,
        session_id = SESSION_ID
    )

    # main_agent = SequentialAgent(
    #     name = "PoemGenerationAgent", 
    #     sub_agents=[],
    #     description="An agent that generates poems based on user input."
    # )
    runner = Runner(
        agent=main_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    return runner, session_service

async def call_agent(
        runner: Runner, 
        query: str
    ) -> str:

    """Sends a query to the specified agent/runner and prints results."""
    print(f"\n>>> Calling Agent: '{runner.agent.name}' | Query: {query}")

    content = types.Content(
        role="USER",
        parts=[
            types.Part(
                text=query,
            )
        ]
    )

    events = runner.run_async(
        new_message=content,
        session_id=SESSION_ID,
        user_id=USER_ID
    )

    async for event in events:
        print(f"Event: {event}")
        # if event.type == types.EventType.RESPONSE:
        #     return event.content.parts[0].text
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print(f"Final response: {final_response}")
    

    # print(f"Final response: {final_response}")
    

    return final_response


async def main():
    runner, session_service = create_agent(main_agent=root_agent)
    while True:
        query = input("Enter a prompt: ")
        response = await call_agent(runner, query)
        print(response)
        current_session = session_service.get_session(app_name=APP_NAME,
                                                user_id=USER_ID,
                                                session_id=SESSION_ID)
        stored_output = current_session.state.get(root_agent.output_key)

        # Pretty print if the stored output looks like JSON (likely from output_schema)
        print(f"--- Session State ['{root_agent.output_key}']: ", end="")
        try:
            import json
            # Attempt to parse and pretty print if it's JSON
            parsed_output = json.loads(stored_output)
            print(json.dumps(parsed_output, indent=2))
        except (json.JSONDecodeError, TypeError):
            # Otherwise, print as string
            print(stored_output)
        print("-" * 30)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
