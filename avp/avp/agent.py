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


from google.adk.agents import Agent, LlmAgent, SequentialAgent
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

test_agent = spa_agent

# class CheckCondition(LlmAgent): # Custom agent to check state
#     async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
#         status = ctx.session.state.get("status", "pending")
#         score = ctx.session.state.get("score", 0.0)
#         is_done = (status == "completed" and score >= 0.95)
#         yield Event(author=self.name, actions=EventActions(escalate=is_done)) # Escalate if done

# score_checker_agent = CheckCondition(
#     name = configs.SCORE_CHECKER_AGENT_NAME,
#     description = configs.SCORE_CHECKER_AGENT_DESCRIPTION,
#     model = configs.BASE_MODEL_NAME,
#     instruction = prompt.SCORE_CHECKER_INSTR,
#     input_schema=ScoreCheckerSchemaInput, # Define the input schema Format
#     # output_schema=ScoreCheckerSchemaOutput, # Define the output schema Format
#     output_key=configs.SCORE_CHECKER_OUTPUT_KEY,
#     before_agent_callback=check_if_agent_should_run,
#     after_agent_callback=check_if_agent_should_run_after,
#     disallow_transfer_to_parent=constant.disallow_transfer_to_parent, 
#     disallow_transfer_to_peers=constant.disallow_transfer_to_peers,
#     tools=[poetic_score]
# )


root_agent = SequentialAgent(
    # model = configs.BASE_MODEL_NAME,
    name = configs.ROOT_AGENT_NAME,
    description = configs.ROOT_AGENT_DESCRIPTION,
    # instruction = ROOT_AGENT_INSTR, 
    # output_key=configs.ROOT_OUTPUT_KEY,
    sub_agents = [
        spa_agent,
        # critic_agent,
        # lt_agent,
    ],
    # max_iterations=constant.ROOT_MAX_ITERATIONS

)

# Example: 
# This is a original poem input: 
# cởi trời xanh cởi đất nâu\n 
# gió mây hờn dỗi bạc nâu nhớ nhung\n 
# bạc đầu tóc trắng da nhung\n 
# cõi tình thế giới ai nhung lưng sầu\n 
# nhớ quê hương nhớ nhuộm sầu\n 
# tóc thề vương vấn đôi sầu vai tròn\n 
# đêm buồn ngắm ánh trăng tròn\n 
# ngẩn ngơ ôm bóng mỏi tròn năm canh. 
# This is a type of poem: LỤC BÁT.
# Let's improve my poem input above about both how to use smooth sentence and suitable both in rhyme and in the setting of even or odd tones in the sentence.



#  This is a original poem input:  cởi trời xanh cởi đất nâu\n  gió mây hờn dỗi bạc nâu nhớ nhung\n  bạc đầu tóc trắng da nhung\n  cõi tình thế giới ai nhung lưng sầu\n  nhớ quê hương nhớ nhuộm sầu\n  tóc thề vương vấn đôi sầu vai tròn\n  đêm buồn ngắm ánh trăng tròn\n  ngẩn ngơ ôm bóng mỏi tròn năm canh.  This is a type of poem: LỤC BÁT. Let's improve my poem input above about both how to use smooth sentence and suitable both in rhyme and in the setting of even or odd tones in the sentence.
#  This is a original poem input:  Cởi trời xanh cởi đất nâu\n  Gió mây hờn dỗi bạc nâu nhớ nhung\n  Bạc đầu tóc trắng da nhung\n  Cõi tình thế giới ai nhung lưng sầu\n  Nhớ quê hương nhớ nhuộm sầu\n  Tóc thề vương vấn đôi sầu vai tròn\n  Đêm buồn ngắm ánh trăng tròn\n  Ngẩn ngơ ôm bóng mỏi tròn năm canh. You should defined yourself the poetic form of the poem before completing all tasks afterward. This is your targeted requirement: Let's improve my poem input above about both how to use smooth sentence and suitable both in rhyme and in the setting of even or odd tones in the sentence.
#  This is a original poem input:  cởi trời xanh cởi đất \n  gió mấy hờn dỗi bạc nâu nhớ nhùng\n  bạc đầu tóc trắng da nhung\n  cõi lửa thế giới ai nhung lưng sầu\n  nhớ quê hương thơ nhuộm sầu\n  tóc thể vương vương đôi sánh vai tròn\n  đêm buồn ngắm ánh trăng tròn\n  ngẩn ngơ ôm bóng mỏi tròn năm canh.  This is a type of poem: LỤC BÁT. Let's improve my poem input above about both how to use smooth sentence and suitable both in rhyme and in the setting of even or odd tones in the sentence.    
#                                                        |           |                        |                                         |                                                |                    |         |        |                   