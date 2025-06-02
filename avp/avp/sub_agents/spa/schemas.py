from pydantic import BaseModel, Field

# METRE CORRECTION AGENT SCHEMA
class MetreSchemaInput(BaseModel):
    poem_input: str = Field(
        description="A string containing the Vietnamese poem lines to be analyzed",
        # examples=["[poem lines]"]
    )

class MetreSchemaOutput(BaseModel):
    poem_identifier: str = Field(
        description="A string containing the Vietnamese poem lines to be analyzed",
        # examples=["[poem lines]"]
    )
    poetic_form: str = Field(
        description="The poetic form of the poem",
        # examples="Lực Bát"
    )
    line_numbers: int = Field(
        description="The number of lines in the poem",
        # examples=8
    )
    metrical_findings: list = Field(
        description="A list of metrical findings for each line",
        # examples=["[metrical findings]"]
    )




# RHYME REFINEMENT AGENT SCHEMA
class RhymeSchemaInput(BaseModel):
    poem_input: str = Field(
        description="A string containing the Vietnamese poem lines to be analyzed",
        # examples=["[poem lines]"]
    )
    metre_input: MetreSchemaOutput = Field(
        description=" All values output from the metre correction agent",
    )

class RhymeSchemaOutput(BaseModel):
    poem_identifier: str = Field(
        description="A string containing the Vietnamese poem lines to be analyzed",
        # examples=["[poem lines]"]
    )
    rhyme_output: list = Field(
        description="A list of rhyme issues which define the rhyming words in the poem",
        # examples=["[rhyme issues]"]
    )


# TONE CLASSIFICATION AGENT SCHEMA
class ToneSchemaInput(BaseModel):
    poem_input: str = Field(
        description="A string containing the Vietnamese poem lines to be analyzed",
        # examples=["[poem lines]"]
    )
    metre_input: MetreSchemaOutput = Field(
        description=" All values output from the metre correction agent",
    )
    rhyme_input: RhymeSchemaOutput = Field(
        description=" All values output from the rhyme refinement agent",
    )

class ToneSchemaOutput(BaseModel):
    poem_identifier: str = Field(
        description="A string containing the Vietnamese poem lines to be analyzed",
        # examples=["[poem lines]"]
    )
    metre_output: list = Field(
        description="A list of metre issues which define the rhyming words in the poem",
        # examples=["[metre issues]"]
    )
    rhyme_output: list = Field(
        description="A list of rhyme issues which define the rhyming words in the poem",
        # examples=["[rhyme issues]"]
    )
    tone_output: list = Field(
        description="A list of tone issues which define the rhyming words in the poem",
        # examples=["[tone issues]"]
    )


# INPUT PREPROCESSOR AGENT SCHEMA
class InputPreprocessorInput(BaseModel):
    poem_input: str = Field(
        description="A string containing the Vietnamese poem lines to be analyzed",
        # examples=["[poem lines]"]
    )

class InputPreprocessorOutput(BaseModel):
    poem_output: str = Field(
        description="The normalized Vietnamese poem lines",
        # examples=["[poem lines]"]
    )




