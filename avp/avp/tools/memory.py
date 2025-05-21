# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The 'memorize' tool for several agents to affect session states."""


from datetime import datetime
import json 
import os 
from typing import Dict, Any 

from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.adk.tools import ToolContext

from configs import (
    constant,
    configs
)


def memorize_list(
        key: str, 
        value: str, 
        tool_context: ToolContext
    ) -> Dict[str, Any]:

    """
        Memorize a list of key-value pairs.

        Args:
            key: The key to use for the list.
            value: The value to add to the list.
            tool_context: The tool context.

        Returns:
            A dictionary containing the updated state.
    """
    mem_dict = tool_context.state
    if key not in mem_dict:
        mem_dict[key] = []

    if value not in mem_dict[key]:
        mem_dict[key].append(value)

    outputs: Dict[str, Any] = {
        "status": f"Stored {value} in {key}",
        "state": mem_dict
    }
    return outputs


def memorize(
        key: str, 
        value: str, 
        tool_context: ToolContext
    ) -> Dict[str, Any]:
    """
        Memorize pieces of information, a key-value pair at a time.

        Args:
            key: The key to use for the list.
            value: The value to add to the list.
            tool_context: The tool context.

        Returns:
            A dictionary containing the updated state.
    """
    mem_dict = tool_context.state
    mem_dict[key] = value
    outputs: Dict[str, Any] = {
        "status": f"Stored {value} in {key}",
        "state": mem_dict
    }
    return outputs

def forget(
        key: str,
        value: str, 
        tool_context: ToolContext
) -> Dict[str, Any]:
    """
        Forget pieces of information, a key-value pair at a time.

        Args:
            key: The key to use for the list.
            value: The value to add to the list.
            tool_context: The tool context.

        Returns:
            A dictionary containing the updated state.
    """
    if tool_context.state[key] is None:
        tool_context.state[key] = []
    
    if value in tool_context.state[key]:
        tool_context.state[key].remove(value)

    outputs: Dict[str, Any] = {
        "status": f"Removed {value} in {key}",
        "state": tool_context.state
    }
    return outputs

def _set_initial_states(
        source: Dict[str, Any],
        target: State | Dict[str, Any]
):
    """
        Setting the initial session state given a JSON object of states.

        Args:
            source: The JSON object of states.
            target: The target session state.

    """

    if constant.SYSTEM_TIME not in target:
        target[constant.SYSTEM_TIME] = str(datetime.now())

    if constant.ITIN_INITIAL not in target:
        target[constant.ITIN_INITIAL] = True

        target.update(source)

        itinerary = source.get(constant.ITIN_KEY, {})
        if itinerary:
            target[constant.ITIN_START_DATE] = itinerary[constant.START_DATE]
            target[constant.ITIN_END_DATE] = itinerary[constant.END_DATE]
            target[constant.ITIN_DATETIME] = itinerary[constant.DATETIME]


def _load_precreated_itinerary(
        callback_context: CallbackContext
):
    """
        Setup the initial state for the session.
        Set this as a callback function as before_agent_call of the root_agent
        This gets called before the system instruction is contructed.

        Args:
            callback_context: The callback context.
    """

    data = {}

    with open(configs.SAMPLE_SCENARIO_PATH, "r") as file:
        data = json.load(file)

        print(f"\n Loading Initial State: {data}")

    _set_initial_states(data["state"], callback_context.state)
