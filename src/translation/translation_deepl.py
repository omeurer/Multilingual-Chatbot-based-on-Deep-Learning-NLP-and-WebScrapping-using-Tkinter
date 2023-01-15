import deepl

auth_key = "YOUR_API_KEY"


def translate_to_french(sentence):
    ''' Function that translate in French '''

    translator = deepl.Translator(auth_key).translate_text(sentence, target_lang='fr')
    return translator.text


def translate_to_user_language(output, language):
    # We don't need to translate if it's already in French.
    if language == 'fr':
        return output
    else:
        if language == "en":
            language = "EN-US" #DeepL specificity
        translator = deepl.Translator(auth_key)

        return translator.translate_text(output, target_lang=language).text
