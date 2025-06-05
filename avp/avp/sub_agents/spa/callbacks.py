from typing import Optional

from google.genai import types
from google.adk.agents.callback_context import CallbackContext




# --- 1. Define the Callback Function ---
def check_if_agent_should_run(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Logs entry and checks 'skip_llm_agent' in session state.
    If True, returns Content to skip the agent's execution.
    If False or not present, returns None to allow execution.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n\n[INFO]{'****'*10} {agent_name.upper()} CALLBACKS {'****'*10}\n")
    print(f"\n[Callback] Entering agent: {agent_name.upper()} (Inv: {invocation_id})")
    print(f"[Callback] Current State: {current_state}")

    # Check the condition in session state dictionary
    if current_state.get("skip_llm_agent", False):
        print(f"[Callback] State condition 'skip_llm_agent=True' met: Skipping agent {agent_name.upper()}.")
        # Return Content to skip the agent's run
        return types.Content(
            parts=[types.Part(text=f"Agent {agent_name.upper()} skipped by before_agent_callback due to state.")],
            role="model" # Assign model role to the overriding response
        )
    else:
        print(f"\n\n[INFO] ******************* {agent_name.upper()} is running *******************")
        print(f"[Callback] State condition not met: Proceeding with agent {agent_name}.")
        # Return None to allow the LlmAgent's normal execution
        return None


def check_if_agent_should_run_after(callback_context: CallbackContext) -> None:
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n\n[Callback] Leaving agent: {agent_name.upper()} (Inv: {invocation_id})")
    print(f"[Callback] Current State: {current_state}")

    # Check the condition in session state dictionary
    if current_state.get("finished_llm_agent", True):
        print(f"[Callback] State condition 'finished_llm_agent=True' met: Finished agent {agent_name.upper()}.")
        # Return Content to skip the agent's run
        return types.Content(
            parts=[types.Part(text=f"Agent {agent_name.upper()} finished by after_agent_callback due to state.")],
            role="model" # Assign model role to the overriding response
        )
    else:
        print(f"\n[INFO] ******************* {agent_name.upper()} not finished yet *******************")
        print(f"[Callback] State condition not met: Proceeding with agent {agent_name.upper()}.")
        # Return None to allow the LlmAgent's normal execution        
        return None


def limit_request_rate(callback_context: CallbackContext) -> None:
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n\n[Callback] Leaving agent: {agent_name.upper()} (Inv: {invocation_id})")
    print(f"[Callback] Current State: {current_state}")

    callback_context.state["request_rate"] = callback_context.state.get("request_rate", 0) + 1
    print(f"[Callback] Request rate: {callback_context.state.get('request_rate', 0)}")
    import time
    if callback_context.state.get("request_rate", 0) >= 2:
        print(f"[Callback] Request rate limit exceeded: Skipping agent {callback_context.agent_name.upper()}.")
        time.sleep(10)
        # reset request rate
        callback_context.state.set("request_rate", 0)
        print(f"[Callback] Request rate reset: {callback_context.state.get('request_rate', 0)}")

        # Check the condition in session state dictionary
        if current_state.get("finished_llm_agent", True):
            print(f"[Callback] State condition 'finished_llm_agent=True' met: Finished agent {agent_name.upper()}.")
            # Return Content to skip the agent's run
            return types.Content(
                parts=[types.Part(text=f"Agent {agent_name.upper()} finished by after_agent_callback due to state.")],
                role="model" # Assign model role to the overriding response
            )
        else:
            print(f"\n[INFO] ******************* {agent_name.upper()} not finished yet *******************")
            print(f"[Callback] State condition not met: Proceeding with agent {agent_name.upper()}.")
            # Return None to allow the LlmAgent's normal execution        
            return None

    return None

    