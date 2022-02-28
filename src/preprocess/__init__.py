"""create path reference"""

from .preprocessor import Preprocessor
from .color_analyser import ColorAnalyser
from .mser import MSER
from .shapedetection import ShapeDetector

__all__ = [
    'Preprocessor',
    'ColorAnalyser',
    'MSER',
    'ShapeDetector',
]
