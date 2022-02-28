"test tranlation"
from ocr_and_translation import SignTranslator

test_texts = [('ausfahrt', 'exit'), ('ausfahrt', '出口'), ('机场', 'airport'), ('机场', 'Flughafen')]


def test_translator():
    "test translation"
    sign_translator = SignTranslator()
    for text in test_texts:
        sign_translator.language_detection(text[1])
        destination_language = sign_translator.source_language
        translated_text = sign_translator.add_translation_text(text[0], destination_language)

        assert translated_text == text[1]
