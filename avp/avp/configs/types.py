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

"""Constants used as keys into ADK's session state."""
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field



# POETIC SCORE TOOL CONFIGURATION
class PoeticScoreToolInput(BaseModel):
    key: str = Field(
        description="The key to store the poetic score tool in the session state.",
    )

class PoeticScoreToolOutput(BaseModel):
    status: str = Field(
        description="The status of the poetic score tool.",
    )
    state: Dict[str, Any] = Field(
        description="The updated session state.",
    )
    poetic_score: float = Field(
        description="The poetic score of the poem.",
    )

# 