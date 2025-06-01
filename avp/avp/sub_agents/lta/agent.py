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

""" Defines the L&TA Critic Agent in the AVP ai agent. """

from google.adk.models import LlmResponse
from google.adk.agents import Agent, LlmAgent, SequentialAgent
from google.adk.agents.callback_context import CallbackContext


from . import prompt
# from avp.avp.configs import configs
from ...configs import configs


semantic_consistency_agent = LlmAgent(
    model = configs.BASE_MODEL_NAME,
    name = configs.SEMANTIC_CONSISTENCY_AGENT_NAME,
    description = configs.SEMANTIC_CONSISTENCY_AGENT_DESCRIPTION,
    instruction = prompt.SEMANTIC_CONSISTENCY_INSTR,
    # before_agent_callback=CallbackContext(
    #     invocation_context="critic_agent_before_callback",
    #     event_actions=lambda context: context.set("task", "L&TA Critic Agent Task")
    # ),
    # after_agent_callback=CallbackContext(
    #     invocation_context="critic_agent_after_callback",
    #     event_actions=lambda context: context.set("result", "L&TA Critic Agent Result")
    # )
)


cutural_context_agent = LlmAgent(
    model = configs.BASE_MODEL_NAME,
    name = configs.CULTURAL_CONTEXT_AGENT_NAME,
    description = configs.CULTURAL_CONTEXT_AGENT_DESCRIPTION,
    instruction = prompt.CULTURAL_CONTEXT_INSTR,
    # before_agent_callback=CallbackContext(
    #     invocation_context="critic_agent_before_callback",
    #     event_actions=lambda context: context.set("task", "L&TA Critic Agent Task")
    # ),
    # after_agent_callback=CallbackContext(
    #     invocation_context="critic_agent_after_callback",
    #     event_actions=lambda context: context.set("result", "L&TA Critic Agent Result")
    # )
)


style_conformity_agent = LlmAgent(
    model = configs.BASE_MODEL_NAME,
    name = configs.STYLE_CONFORMITY_AGENT_NAME,
    description = configs.STYLE_CONFORMITY_AGENT_DESCRIPTION,
    instruction = prompt.STYLE_CONFORMITY_INSTR,
    # before_agent_callback=CallbackContext(
    #     invocation_context="critic_agent_before_callback",
    #     event_actions=lambda context: context.set("task", "L&TA Critic Agent Task")
    # ),
    # after_agent_callback=CallbackContext(
    #     invocation_context="critic_agent_after_callback",
    #     event_actions=lambda context: context.set("result", "L&TA Critic Agent Result")
    # )
)


lt_agent = SequentialAgent(
    name = configs.LAT_AGENT_NAME,
    description = configs.LAT_AGENT_DESCRIPTION,
    sub_agents=[
        semantic_consistency_agent, 
        cutural_context_agent, 
        style_conformity_agent
    ]
)