from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union



# METRE CORRECTION AGENT SCHEMA
class MetreSchemaInput(BaseModel):
    poem_input: str = Field(
        description="A string containing the Vietnamese poem lines to be analyzed",
        # examples=["[poem lines]"]
    )
    ryhme_input: Optional[List[str]] = Field(
        description=" All values output from the rhyme refinement agent",
    )
    tone_input: Optional[List[str]] = Field(
        description=" All values output from the tone classification agent",
    )


class MetreSchemaOutput(BaseModel):
    poem_identifier: List[str] = Field(
        description="A string containing the Vietnamese poem lines to be analyzed",
        # examples=["[poem lines]"]
    )
    poetic_form: str = Field(
        description="The poetic form of the poem",
        # examples="Lục Bát"
    )
    line_numbers: int = Field(
        description="The number of lines in the poem",
        # examples=8
    )

    metre_issues: List[str] = Field(
        description="A list of metrical issues for each line",
    )
    metre_output: List[str] = Field(
        description="A list of improved poem lines with metrical corrections",
    )






# RHYME REFINEMENT AGENT SCHEMA
class RhymeSchemaInput(BaseModel):
    poem_input: str = Field(
        description="A string containing the Vietnamese poem lines to be analyzed",
        # examples=["[poem lines]"]
    )
    metre_input: Optional[List[str]] = Field(
        description=" All values output from the metre correction agent",
    )
    tone_input: Optional[List[str]] = Field(
        description=" All values output from the tone classification agent",
    )


class RhymeSchemaOutput(BaseModel):
    poem_identifier: str = Field(
        description="A string containing the Vietnamese poem lines to be analyzed",
        # examples=["[poem lines]"]
    )
    rhyme_issues: List[str] = Field(
        description="A list of rhyme issues which define the rhyming words in the poem",
    )
    rhyme_output: List[str] = Field(
        description="A list of rhyme issues which define the rhyming words in the poem",
        # examples=["[rhyme issues]"]
    )


# TONE CLASSIFICATION AGENT SCHEMA
class ToneSchemaInput(BaseModel):
    poem_input: str = Field(
        description="A string containing the Vietnamese poem lines to be analyzed",
        # examples=["[poem lines]"]
    )
    metre_input: Optional[List[str]] = Field(
        description=" All values output from the metre correction agent",
    )
    rhyme_input: Optional[List[str]] = Field(
        description=" All values output from the rhyme refinement agent",
    )

class ToneSchemaOutput(BaseModel):
    poem_identifier: str = Field(
        description="A string containing the Vietnamese poem lines to be analyzed",
        # examples=["[poem lines]"]
    )
    metre_output: List[str] = Field(
        description="A list of metre issues which define the rhyming words in the poem",
        # examples=["[metre issues]"]
    )
    rhyme_output: List[str] = Field(
        description="A list of rhyme issues which define the rhyming words in the poem",
        # examples=["[rhyme issues]"]
    )
    tone_output: List[str] = Field(
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
    # poem_output: str = Field(
    #     description="The normalized Vietnamese poem lines",
    #     # examples=["[poem lines]"]
    # )
    preprocessed_output: List[str] = Field(
        description="A list of tone issues which define the rhyming words in the poem",
        # examples=["[tone issues]"]
    )
    
    poetic_form: str = Field(   
        description="The poetic form of the poem",
        # examples="Lục Bát"
    )
    count_syllables: List[str] = Field(
        description="A list of tone issues which define the rhyming words in the poem",
        # examples=["[tone issues]"]
    )
    tone_pattern: List[str] = Field(
        description="A list of tone issues which define the rhyming words in the poem",
        # examples=["[tone issues]"]
    )


class ScoreCheckerSchemaInput(BaseModel):
    poem_input: str = Field(
        description="A string containing the Vietnamese poem lines to be analyzed",
        # examples=["[poem lines]"]
    )
    poetic_form: str = Field(
        description="The poetic form of the poem",
        # examples="Lục Bát"
    )

class ScoreCheckerSchemaOutput(BaseModel):
    poem_output: str = Field(
        description="The normalized Vietnamese poem lines",
        # examples=["[poem lines]"]
    )
    status : str = Field(
        description="The status of the poetic score tool",
        # examples=["[poem lines]"]
    )
    score: float = Field(
        description="The output of the poetic score tool",
        # examples=["[poem lines]"]
    )




