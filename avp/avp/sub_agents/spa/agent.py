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
# from avp.avp.configs import configs
from ...configs import configs
from .schemas import (
    InputPreprocessorInput,
    InputPreprocessorOutput,
    MetreSchemaInput,
    MetreSchemaOutput,
    RhymeSchemaInput,
    RhymeSchemaOutput,
    ToneSchemaInput,
    ToneSchemaOutput
)
from  .callbacks import *




metre_agent = LlmAgent(
    model = configs.BASE_MODEL_NAME,
    name = configs.METRE_CORRECTION_AGENT_NAME,
    description = configs.METRE_CORRECTION_AGENT_DESCRIPTION,
    instruction = prompt.METRE_INSTR,
    input_schema=MetreSchemaInput, # Define the input schema Format
    output_schema=MetreSchemaOutput, # Define the output schema Format
    output_key=configs.METRE_OUTPUT_KEY, # Store the metre output (JSON response) in this key
    before_agent_callback=check_if_agent_should_run,
    # before_agent_callback=CallbackContext(
    #     invocation_context="spa_agent_before_callback",
    #     event_actions=lambda context: context.set("task", "SPA Agent Task")
    # ),
    after_agent_callback=check_if_agent_should_run_after,
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
    input_schema=RhymeSchemaInput, # Define the input schema Format
    output_schema=RhymeSchemaOutput, # Define the output schema Format
    output_key=configs.RHYME_OUTPUT_KEY,
    before_agent_callback=check_if_agent_should_run,
    # before_agent_callback=CallbackContext(
    #     invocation_context="spa_agent_before_callback",
    #     event_actions=lambda context: context.set("task", "SPA Agent Task")
    # ),
    after_agent_callback=check_if_agent_should_run_after,
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
    input_schema=ToneSchemaInput, # Define the input schema Format
    output_schema=ToneSchemaOutput, # Define the output schema Format
    output_key=configs.TONE_OUTPUT_KEY,
    before_agent_callback=check_if_agent_should_run,
    # before_agent_callback=CallbackContext(
    #     invocation_context="spa_agent_before_callback",
    #     event_actions=lambda context: context.set("task", "SPA Agent Task")
    # ),
    after_agent_callback=check_if_agent_should_run_after,
    # after_agent_callback=CallbackContext(
    #     invocation_context="spa_agent_after_callback",
    #     event_actions=lambda context: context.set("result", "SPA Agent Result")
    # )

)

preprocessor_agent = LlmAgent(
    model = configs.BASE_MODEL_NAME,
    name = configs.INPUT_PREPROCESSOR_AGENT_NAME,
    description = configs.INPUT_PREPROCESSOR_AGENT_DESCRIPTION,
    instruction = prompt.INPUT_PREPROCESSOR_INSTR,
    input_schema=InputPreprocessorInput, # Define the input schema Format
    output_schema=InputPreprocessorOutput, # Define the output schema Format
    output_key=configs.INPUT_PREPROCESSOR_OUTPUT_KEY,
    before_agent_callback=check_if_agent_should_run,
    # before_agent_callback=CallbackContext(
    #     invocation_context="spa_agent_before_callback",
    #     event_actions=lambda context: context.set("task", "SPA Agent Task")
    # ),
    after_agent_callback=check_if_agent_should_run_after,
    # after_agent_callback=CallbackContext(
    #     invocation_context="spa_agent_after_callback",
    #     event_actions=lambda context: context.set("result", "SPA Agent Result")
    # )

)

spa_agent = SequentialAgent(
    name = configs.SAP_AGENT_NAME,
    description = configs.SAP_AGENT_DESCRIPTION,
    sub_agents=[
        preprocessor_agent,
        metre_agent, 
        rhyme_agent, 
        tone_agent
    ]

)
