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

""" Defines the SPA Critic Agent in the AVP ai agent. """

from google.adk.agents import Agent, LlmAgent, SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse


from . import prompt
from avp.avp.configs import configs




metre_agent = LlmAgent(
    model = configs.BASE_MODEL_NAME,
    name = configs.METRE_CORRECTION_AGENT_NAME,
    description = configs.METRE_CORRECTION_AGENT_DESCRIPTION,
    instruction = prompt.METRE_INSTR,
    # before_agent_callback=CallbackContext(
    #     invocation_context="spa_agent_before_callback",
    #     event_actions=lambda context: context.set("task", "SPA Agent Task")
    # ),
    # after_agent_callback=CallbackContext(
    #     invocation_context="spa_agent_after_callback",
    #     event_actions=lambda context: context.set("result", "SPA Agent Result")
    # )

)

rhyme_agent = LlmAgent(
    model = configs.BASE_MODEL_NAME,
    name = configs.RHYME_REFINEMENT_AGENT_NAME,
    description = configs.RHYME_REFINEMENT_AGENT_DESCRIPTION,
    instruction = prompt.RHYME_INSTR,
    # before_agent_callback=CallbackContext(
    #     invocation_context="spa_agent_before_callback",
    #     event_actions=lambda context: context.set("task", "SPA Agent Task")
    # ),
    # after_agent_callback=CallbackContext(
    #     invocation_context="spa_agent_after_callback",
    #     event_actions=lambda context: context.set("result", "SPA Agent Result")
    # )

)

tone_agent = LlmAgent(
    model = configs.BASE_MODEL_NAME,
    name = configs.TONE_CLASSIFIER_AGENT_NAME,
    description = configs.TONE_CLASSIFIER_AGENT_DESCRIPTION,
    instruction = prompt.TONE_INSTR,
    # before_agent_callback=CallbackContext(
    #     invocation_context="spa_agent_before_callback",
    #     event_actions=lambda context: context.set("task", "SPA Agent Task")
    # ),
    # after_agent_callback=CallbackContext(
    #     invocation_context="spa_agent_after_callback",
    #     event_actions=lambda context: context.set("result", "SPA Agent Result")
    # )

)

spa_agent = SequentialAgent(
    name = configs.SAP_AGENT_NAME,
    description = configs.SAP_AGENT_DESCRIPTION,
    sub_agents=[
        metre_agent, 
        rhyme_agent, 
        tone_agent
    ]

)
