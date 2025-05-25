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


"""Demonstration of AVP Workflow using Agent Development Kit"""


from google.adk.agents import Agent 
from prompt import ROOT_AGENT_INSTR
from tools.memory import _load_precreated_itinerary

from configs import (
    configs,
    constant
)

from .sub_agents import (
    critic_agent,
    lt_agent,
    spa_agent,
)

root_agent = Agent(
    model = configs.BASE_MODEL_NAME,
    name = configs.ROOT_AGENT_NAME,
    description = configs.ROOT_AGENT_DESCRIPTION,
    instruction = ROOT_AGENT_INSTR, 
    sub_agents = [
        critic_agent,
        lt_agent,
        spa_agent
    ],
    before_agent_callback=_load_precreated_itinerary
)