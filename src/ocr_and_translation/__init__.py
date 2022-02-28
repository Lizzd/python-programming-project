""" Init"""
import locale
from .ocr_and_translation import OCRAndTranslation
from .ocr import OCR
from .sign_translator import SignTranslator

__all__ = ['OCRAndTranslation',
           'OCR',
           'SignTranslator']
locale.setlocale(locale.LC_ALL, 'C')
