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


from google.adk.agents import Agent, LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse


from .prompt import ROOT_AGENT_INSTR
from .tools import _load_precreated_itinerary

from .configs import (
    configs,
    constant
)

from .sub_agents import (
    critic_agent,
    lt_agent,
    spa_agent,
)

root_agent = LlmAgent(
    model = configs.BASE_MODEL_NAME,
    name = configs.ROOT_AGENT_NAME,
    description = configs.ROOT_AGENT_DESCRIPTION,
    instruction = ROOT_AGENT_INSTR, 
    # output_key=configs.ROOT_OUTPUT_KEY,
    sub_agents = [
        critic_agent,
        lt_agent,
        spa_agent
    ],
    # before_agent_callback=_load_precreated_itinerary
    #     before_agent_callback=CallbackContext(
    #     invocation_context="poetry_agent_before_callback",
    #     event_actions=lambda context: context.set("task", "AVP Root Agent Task")
    # ),
    # after_agent_callback=CallbackContext(
    #     invocation_context="poetry_agent_after_callback",
    #     event_actions=lambda context: context.set("result", "AVP Root Agent Result")
    # )
)

# Example: This is a original poem input: cởi trời xanh cởi đất nâu\n gió mây hờn dỗi bạc nâu nhớ nhung\n bạc đầu tóc trắng da nhung\n cõi tình thế giới ai nhung lưng sầu\n nhớ quê hương nhớ nhuộm sầu\n tóc thề vương vấn đôi sầu vai tròn\n đêm buồn ngắm ánh trăng tròn\n ngẩn ngơ ôm bóng mỏi tròn năm canh. Let's improve my poem input above about both how to use smooth sentence and suitable both in rhyme and in the setting of even or odd tones in the sentence.