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

"""COnfigs used as Environment variables for Agent Development Kit Project."""

# Outer Project Configurations
BASE_MODEL_NAME = "gemini-2.0-flash-001"
SAMPLE_SCENARIO_PATH = "avp/avp/configs/sample_scenario.json"


# Agent configurations

ROOT_AGENT_NAME = "root_agent"
ROOT_AGENT_DESCRIPTION = (
    "managing the entire workflow of Vietnamese poetry refinement, "
    "from initial poem ingestion to final output, by intelligently dispatching tasks "
    "to specialized agents and synthesizing their findings."
)
ROOT_OUTPUT_KEY = "final_poem"


# ------ Sub-agent configurations ------
# ------
CRITIC_AGENT_NAME = "critic_agent"
CRITIC_AGENT_DESCRIPTION = (
    "focusing on implementing a critical review process for the poem, "
    "ensuring it meets quality standards and output's expectations, "
    "evaluating the poem's quality, coherence, and adherence to the desired poetic form."
)
# ------
POST_PROCESSING_AGENT_NAME = "post_processing_agent"
POST_PROCESSING_AGENT_DESCRIPTION = (
    "responsible for the final adjustments and enhancements to the poem, "
    "ensuring it is polished and ready for presentation, "
    "making final adjustments to the poem's structure, tone, and thematic elements, "
    "and ensuring it aligns with the desired poetic style and form."
)
# ------
FORMATTER_AGENT_NAME = "formatter_agent"
FORMATTER_AGENT_DESCRIPTION = (
    "responsible for formatting the poem according to the desired style, "
    "ensuring it adheres to the specified poetic form, "
    "and making necessary adjustments to the poem's structure and layout."
)
# ------
FEEDBACK_AGENT_NAME = "feedback_agent"
FEEDBACK_AGENT_DESCRIPTION = (
    "providing feedback on the poem's quality, coherence, and adherence to the desired poetic form, "
    "ensuring it meets the expectations of the intended audience, "
    "and making necessary adjustments to enhance the poem's overall impact."
)
# ------





# ------ Sub-agent configurations ------
# ------
SAP_AGENT_NAME = "spa_agent"
SAP_AGENT_DESCRIPTION = (
    "focysing on the poem's structure, tone, and thematic elements, "
    "figuring out the wrong aspects of the poem, "
    "and providing suggestions for improvement, "
    "ensuring it aligns with the desired poetic form and style."
)
SPA_OUTPUT_KEY = "spa_output"
# ------
INPUT_PREPROCESSOR_AGENT_NAME = "input_preprocessor_agent"
INPUT_PREPROCESSOR_AGENT_DESCRIPTION = (
    "responsible for cleaning, normalizing, and parsing the input poem text, "
    "ensuring it is ready for further analysis, adjustments, creation and refinement."
)
INPUT_PREPROCESSOR_OUTPUT_KEY = "preprocessed_output"
# ------
TONE_CLASSIFIER_AGENT_NAME = "tone_classifier_agent"
TONE_CLASSIFIER_AGENT_DESCRIPTION = (
    "analyzing the poem's tone, "
    "identifying its emotional and thematic elements, "
    "and providing insights into the poem's mood and atmosphere."
)
TONE_OUTPUT_KEY = "tone_output"
# ------
METRE_CORRECTION_AGENT_NAME = "metre_correction_agent"
METRE_CORRECTION_AGENT_DESCRIPTION = (
    "focusing on the poem's metrical structure, "
    "ensuring it adheres to the desired poetic form, "
    "and making necessary adjustments to the rhythm and meter."
)
METRE_OUTPUT_KEY = "metre_output"
# ------
RHYME_REFINEMENT_AGENT_NAME = "rhyme_refinement_agent"
RHYME_REFINEMENT_AGENT_DESCRIPTION = (
    "responsible for refining the poem's rhyme scheme, "
    "ensuring it aligns with the desired poetic form, "
    "and enhancing the musicality of the poem through effective rhyme."
)
RHYME_OUTPUT_KEY = "rhyme_output"
# ------


# ------ Sub-agent configurations ------
# ------
LAT_AGENT_NAME = "lexical_and_thematic_agent"
LAT_AGENT_DESCRIPTION = (
    "directly improving the poem's language and thematic elements, "
    "changing the poem's word choice or tone to better fit the desired style, "
    "ensuring it resonates with the intended audience and adheres to the desired poetic style, "
    "and enhancing the poem's overall impact through careful word choice and thematic depth."
)

# ------
LEXICAL_TUNING_AGENT_NAME = "lexical_tuning_agent"
LEXICAL_TUNING_AGENT_DESCRIPTION = (
    "poitioned to enhance the poem's language and word choice, "
    "ensuring it aligns with the desired poetic style, "
    "and making necessary adjustments to the vocabulary and word usage."
)
# ------
STYLE_CONFORMITY_AGENT_NAME = "style_conformity_agent"
STYLE_CONFORMITY_AGENT_DESCRIPTION = (
    "overseeing the poem's adherence to the desired poetic style, "
    "observing the poem's overall structure, tone, and thematic elements, "
    "ensuring it aligns with the intended poetic form and style, "
    "and making necessary adjustments to maintain stylistic consistency."
)
# ------
CULTURAL_CONTEXT_AGENT_NAME = "cultural_context_agent"
CULTURAL_CONTEXT_AGENT_DESCRIPTION = (
    "ensuring the poem's cultural relevance and appropriateness, "
    "considering the cultural context of the poem, "
    "and making necessary adjustments to ensure it resonates with the intended audience, "
    "and aligns with the desired poetic style."
)
# ------
SEMANTIC_CONSISTENCY_AGENT_NAME = "semantic_consistency_agent"
SEMANTIC_CONSISTENCY_AGENT_DESCRIPTION = (
    "ensuring the poem's semantic coherence and consistency, "
    "checking for logical flow, thematic consistency, and overall coherence, "
    "and making necessary adjustments to ensure the poem's meaning is clear and impactful."
)
# ------


