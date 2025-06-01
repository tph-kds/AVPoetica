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

""" Defines the Critic Agent in the AVP ai agent. """

from google.adk.agents import Agent, LlmAgent, SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse


from . import prompt
# from avp.avp.configs import configs
from ...configs import configs

post_processing_agent = LlmAgent(
    model = configs.BASE_MODEL_NAME,
    name = configs.POST_PROCESSING_AGENT_NAME,
    description = configs.POST_PROCESSING_AGENT_DESCRIPTION,
    instruction = prompt.POST_PROCESSING_INSTR,
    # before_agent_callback=CallbackContext(
    #     invocation_context="critic_agent_before_callback",
    #     event_actions=lambda context: context.set("task", "L&TA Critic Agent Task")
    # ),
    # after_agent_callback=CallbackContext(
    #     invocation_context="critic_agent_after_callback",
    #     event_actions=lambda context: context.set("result", "L&TA Critic Agent Result")
    # )
)

formatter_agent = LlmAgent(
    model = configs.BASE_MODEL_NAME,
    name = configs.FORMATTER_AGENT_NAME,
    description = configs.FORMATTER_AGENT_DESCRIPTION,
    instruction = prompt.FORMATTER_INSTR,
    # before_agent_callback=CallbackContext(
    #     invocation_context="critic_agent_before_callback",
    #     event_actions=lambda context: context.set("task", "L&TA Critic Agent Task")
    # ),
    # after_agent_callback=CallbackContext(
    #     invocation_context="critic_agent_after_callback",
    #     event_actions=lambda context: context.set("result", "L&TA Critic Agent Result")
    # )
)

feedback_agent = LlmAgent(
    model = configs.BASE_MODEL_NAME,
    name = configs.FEEDBACK_AGENT_NAME,
    description = configs.FEEDBACK_AGENT_DESCRIPTION,
    instruction = prompt.FEEDBACK_INSTR,
    # before_agent_callback=CallbackContext(
    #     invocation_context="critic_agent_before_callback",
    #     event_actions=lambda context: context.set("task", "L&TA Critic Agent Task")
    # ),
    # after_agent_callback=CallbackContext(
    #     invocation_context="critic_agent_after_callback",
    #     event_actions=lambda context: context.set("result", "L&TA Critic Agent Result")
    # )
)

critic_agent = SequentialAgent(
    name = configs.CRITIC_AGENT_NAME,
    description = configs.CRITIC_AGENT_DESCRIPTION,
    sub_agents=[
        post_processing_agent, 
        formatter_agent, 
        feedback_agent
    ]
)
