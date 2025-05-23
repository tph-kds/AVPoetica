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


"""Demonstration of Travel AI Conceirge using Agent Development Kit"""


from google.adk.agents import Agent 
from prompt import prompt 
from tools.memory import _load_precreated_itinerary

from configs import (
    configs,
    constant
)

root_agent = Agent(
    model = configs.BASE_MODEL_NAME,
    name = configs.AGENT_NAME,
    description = configs.AGENT_DESCRIPTION,
    instruction = prompt.ROOT_AGENT_INSTR, 
    sub_agents = [
        ...
    ],
    before_agent_callback=_load_precreated_itinerary
)