import os 
import sys

from ..configs import (
    MaskErrorTokenizationConfig,
    CountSyllablePoemsConfig,
)
from .poetic_rule import PoeticRules
from .count_syllables import CountSyllablePoems

class MaskErrorTokenization:
    def __init__(
            self,
            met_config: MaskErrorTokenizationConfig):
        super(MaskErrorTokenization, self).__init__()



    def mask_error_tokenization(self):
        pass

